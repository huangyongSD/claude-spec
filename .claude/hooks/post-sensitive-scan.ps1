# PostToolUse hook: sensitive-scan
# When Edit/Write tools write content, check for sensitive values
# Robustness: null-safe access, stdin fallback, encoding handling, error prompts
# Security: comprehensive sensitive pattern detection (credentials, keys, URLs, certificates)

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
    Write-Host "[Hook] WARNING: Failed to parse hook input JSON. Skipping sensitive-scan check."
    exit 0
}

# Null-safe access to tool_input, file_path, and content
$filePath = ""
$content = ""

if ($data.PSObject.Properties['tool_input']) {
    $toolInput = $data.tool_input
    if ($toolInput.PSObject.Properties['file_path']) {
        $filePath = $toolInput.file_path
    }
    if ($toolInput.PSObject.Properties['new_string']) {
        $content = $toolInput.new_string
    }
    if ($toolInput.PSObject.Properties['content']) {
        $content = $toolInput.content
    }
}

if (-not $content -or $content.Trim() -eq "") {
    exit 0
}

$foundSensitive = @()

# --- 1. Check against secrets.json real values ---
$secretsPath = Join-Path $PSScriptRoot "..\tools\secrets.json"

if (Test-Path $secretsPath) {
    try {
        $secrets = Get-Content $secretsPath -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($secrets.PSObject.Properties['real_values']) {
            $realValues = $secrets.real_values
            $sensitiveKeys = @(
                'db_master_password', 'db_master_host', 'db_master_url',
                'db_slave_password', 'db_slave_host', 'db_slave_url',
                'redis_password', 'redis_host', 'redis_url',
                'mq_password', 'mq_host',
                'jwt_secret', 'encrypt_key'
            )

            foreach ($key in $sensitiveKeys) {
                if ($realValues.PSObject.Properties[$key]) {
                    $value = $realValues.($key)
                    if ($value -and $value.ToString().Trim() -ne "" -and $content -match [regex]::Escape($value.ToString())) {
                        $foundSensitive += "real-value: $key"
                    }
                }
            }
        }
    } catch {
        Write-Host "[Hook] WARNING: Failed to parse secrets.json. Skipping real-value check. Error: $($_.Exception.Message)"
    }
}

# --- 2. Pattern-based sensitive detection ---

# 2a. Password in config without placeholder
$passwordPattern = [regex]::new('(?:password|passwd|pwd)\s*[=:]\s*[^\s{][^\n]*', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
$passwordMatches = $passwordPattern.Matches($content)
foreach ($m in $passwordMatches) {
    $matchValue = $m.Value
    if ($matchValue -notmatch '\{\{.*\}\}') {
        $foundSensitive += "password-pattern: $matchValue"
    }
}

# 2b. Credential in URL (mysql://user:pass@host, redis://:pass@host, etc.)
if ($content -match '[a-z]+://[^\s:]+:[^\s@]+@[^\s]+') {
    $foundSensitive += "credential-in-url"
}

# 2c. JDBC URL with credentials
if ($content -match 'jdbc:[a-z]+://[^\s:]+:[^\s@]+@[^\s]+') {
    $foundSensitive += "jdbc-credential"
}

# 2d. Hardcoded JWT secret / API key
if ($content -match '(?:jwt[_-]?secret|api[_-]?key|secret[_-]?key|access[_-]?token)\s*[=:]\s*[''"][A-Za-z0-9]{16,}[''"]') {
    $foundSensitive += "hardcoded-api-key"
}

# 2e. Private key content
if ($content -match '-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----') {
    $foundSensitive += "private-key-content"
}

# 2f. AWS / cloud access key
if ($content -match '(?:AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16}') {
    $foundSensitive += "aws-access-key"
}

# --- 3. Output results ---
if ($foundSensitive.Count -gt 0) {
    $uniqueFindings = $foundSensitive | Select-Object -Unique
    Write-Host ("[Hook] WARNING: Sensitive information detected in file " + $filePath + ". Findings: " + ($uniqueFindings -join ", ") + ". Use placeholders instead. Run 'python .claude/tools/secrets-sync.py --scan-configs' for replacement suggestions.")
}

# Always exit 0 (reminder only, not blocking)
exit 0