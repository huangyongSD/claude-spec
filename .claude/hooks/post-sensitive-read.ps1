# PostToolUse hook: sensitive-read
# When Read tool accesses files that may contain sensitive info, remind about safe handling
# Robustness: null-safe access, stdin fallback, encoding handling
# Security: comprehensive sensitive file pattern detection

param(
    [string]$InputJson
)

# Read stdin if no argument provided
if (-not $InputJson) {
    try {
        $InputJson = [System.Console]::In.ReadToEnd()
    } catch {
        exit 0
    }
}

if (-not $InputJson -or $InputJson.Trim() -eq "") {
    exit 0
}

try {
    $data = $InputJson | ConvertFrom-Json
} catch {
    Write-Host "[Hook] WARNING: Failed to parse hook input JSON. Skipping sensitive-read check."
    exit 0
}

# Null-safe access to tool_input and file_path
$filePath = ""
if ($data.PSObject.Properties['tool_input']) {
    $toolInput = $data.tool_input
    if ($toolInput.PSObject.Properties['file_path']) {
        $filePath = $toolInput.file_path
    }
}

if (-not $filePath -or $filePath.Trim() -eq "") {
    exit 0
}

# --- Sensitive file pattern detection ---
$warnings = @()

# Application YAML configs (database, redis, mq credentials)
if ($filePath -match 'application-.*\.ya?ml$') {
    $warnings += "Application YAML file detected. May contain passwords/host IPs. Do not use real values in subsequent operations."
}

# .env files (environment variables with secrets)
if ($filePath -match '\.env($|\.|-)') {
    $warnings += ".env file detected. May contain API keys, passwords, and secrets. Do not use real values in subsequent operations."
}

# Properties files (Java config with credentials)
if ($filePath -match '\.properties$') {
    $warnings += "Properties file detected. May contain database passwords and connection strings. Do not use real values in subsequent operations."
}

# secrets.json itself
if ($filePath -match 'secrets\.json$') {
    $warnings += "secrets.json file detected. Contains real credentials. Never pass these values to AI models or log them."
}

# Docker/K8s secret files
if ($filePath -match '(?:docker-compose|k8s|kubernetes).*\.ya?ml$') {
    $warnings += "Container orchestration file detected. May contain environment variables with secrets. Do not use real values in subsequent operations."
}

# SSL/TLS certificate files
if ($filePath -match '\.(?:pem|key|p12|jks|pfx|cert)$') {
    $warnings += "Certificate/key file detected. Never expose private keys or pass them to AI models."
}

# Shell scripts that may source secrets
if ($filePath -match '\.(?:sh|bash|ps1)$' -and $filePath -notmatch '\.claude[/\\]hooks') {
    # Only warn for scripts outside .claude/hooks
    if ($filePath -match '(?:deploy|setup|init|config|secret)') {
        $warnings += "Deployment/setup script detected. May contain hardcoded credentials. Do not use real values in subsequent operations."
    }
}

# Output all warnings
foreach ($warning in $warnings) {
    Write-Host ("[Hook] WARNING: " + $warning + " For database operations, use /sds-dbquery or 'python .claude/tools/db-query.py'.")
}

# Always exit 0 (reminder only, not blocking)
exit 0