# PreToolUse Hook: Command safety check
# Robustness: null-safe access, stdin fallback, error prompts
# Security: dangerous command detection, sensitive data exposure, privilege escalation

$stdin = ""
try {
    $stdin = [Console]::In.ReadToEnd()
} catch {
    exit 0
}

if (-not $stdin -or $stdin.Trim() -eq "") {
    exit 0
}

try {
    $j = $stdin | ConvertFrom-Json
} catch {
    Write-Host "[Hook] WARNING: Failed to parse hook input JSON. Skipping pre-bash check."
    exit 0
}

# Null-safe access to command
$command = ""
if ($j.PSObject.Properties['command']) {
    $command = $j.command
}

if (-not $command -or $command.Trim() -eq "") {
    exit 0
}

$warnings = @()
$blocked = @()

# --- 1. Long-running command detection ---
$PACKAGE_MANAGER = "mvn|yarn|npm|pip|gradle"
if ($command -match "^($PACKAGE_MANAGER)\s+(install|i|package|clean|compile|test|build)") {
    $warnings += "Long-running command detected. Consider running in background."
}

# --- 2. Dangerous command detection ---

# Destructive file operations
if ($command -match '(?:rm\s+-rf|rmdir\s+/[sq]|del\s+/[fq]|Remove-Item\s+.*-Recurse\s+.*-Force)') {
    $warnings += "Destructive file deletion detected. Verify target path before execution."
}

# Database write operations (BLOCKED - should use dedicated tools)
if ($command -match '(?:mysql|psql|sqlplus)\s+.*(?:-e|--execute)\s+.*(?:INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE)') {
    $blocked += "Database write operation detected. Use /sds-dbquery or 'python .claude/tools/db-query.py' for read-only queries. Write operations must go through proper review."
}
# Database write via pipe (echo "SQL" | mysql)
if ($command -match '(?:INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE)\s+.*\|\s*(?:mysql|psql|sqlplus)') {
    $blocked += "Database write operation via pipe detected. Use /sds-dbquery or 'python .claude/tools/db-query.py' for read-only queries. Write operations must go through proper review."
}
# Database write via file redirect (mysql < file.sql)
if ($command -match '(?:mysql|psql|sqlplus)\s+.*<\s+\S+\.sql') {
    $blocked += "Database write operation via SQL file detected. Use /sds-dbquery or 'python .claude/tools/db-query.py' for read-only queries. Write operations must go through proper review."
}
# Redis/MongoDB dangerous operations
if ($command -match 'redis-cli\s+(?:FLUSHALL|FLUSHDB|CONFIG\s+SET|SHUTDOWN)') {
    $blocked += "Redis destructive operation detected. This operation is not allowed."
}
if ($command -match 'mongo.*--eval.*(?:dropDatabase|drop\(|deleteMany|remove\()') {
    $blocked += "MongoDB destructive operation detected. This operation is not allowed."
}

# Direct password/credential on command line
if ($command -match '(?:--password|-p|--passwd|--secret|--token|--api-key)\s+\S+') {
    $warnings += "Credential on command line detected. Use environment variables or config files instead."
}

# Credential in URL on command line
if ($command -match '[a-z]+://[^\s:]+:[^\s@]+@[^\s]+') {
    $warnings += "Credential in URL detected. Use environment variables or config files instead."
}

# Privilege escalation
if ($command -match '(?:sudo|runas|su\s+-)') {
    $warnings += "Privilege escalation detected. Avoid running commands with elevated privileges."
}

# Pipe to shell execution
if ($command -match '\|\s*(?:sh|bash|powershell|cmd)') {
    $warnings += "Pipe to shell execution detected. Verify the piped content is trusted."
}

# Curl/wget pipe to shell (common attack vector)
if ($command -match '(?:curl|wget|Invoke-WebRequest)\s+.*\|\s*(?:sh|bash|powershell)') {
    $warnings += "Remote script execution detected (curl|wget to shell). This is a security risk."
}

# Git force push
if ($command -match 'git\s+push\s+.*--force') {
    $warnings += "Git force push detected. This may overwrite remote history. Use with caution."
}

# Git clean (removes untracked files)
if ($command -match 'git\s+clean\s+.*-fd') {
    $warnings += "Git clean with force detected. This will remove untracked files and directories."
}

# --- 3. Output results ---
foreach ($warning in $warnings) {
    Write-Host ("[Hook] WARNING: " + $warning)
}

# Blocked items: exit with error code to prevent execution
if ($blocked.Count -gt 0) {
    foreach ($item in $blocked) {
        Write-Host ("[Hook] BLOCKED: " + $item)
    }
    Write-Host "[Hook] Command execution blocked due to security policy. Resolve the above issues before retrying."
    exit 1
}

# Always exit 0 (reminder only, not blocking)
exit 0
