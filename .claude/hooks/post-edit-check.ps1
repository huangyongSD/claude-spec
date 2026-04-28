# PostToolUse Hook: Code file formatting reminder + config placeholder detection + sensitive info detection
# Robustness: null-safe property access, encoding handling, error boundaries
# Security: comprehensive sensitive pattern detection, credential-in-URL, API keys, private keys

$stdin = [Console]::In.ReadToEnd()
if (-not $stdin) { exit 0 }

try { $j = $stdin | ConvertFrom-Json }
catch { exit 0 }

# Null-safe access to tool_input and file_path
if (-not $j.PSObject.Properties['tool_input']) { exit 0 }
$toolInput = $j.tool_input
if (-not $toolInput.PSObject.Properties['file_path']) { exit 0 }
$f = $toolInput.file_path
if (-not $f) { exit 0 }

# --- 1. Code file formatting reminder ---
$FILE_EXTENSIONS = "(java|xml|vue|js|yaml|scss|sql)$"
if ($f -match $FILE_EXTENSIONS) {
  Write-Host ("[Hook] " + $j.tool_name + " file: " + $f + " - Format: backend 'mvn spotless:apply', frontend 'yarn lint'")
}

# --- 2. Config file placeholder detection ---
if ($f -match '^\.claude/' -and (Test-Path $f)) {
  try {
    $content = Get-Content $f -Raw -Encoding UTF8 -ErrorAction Stop
    if ($content -match '\{\{[A-Z][A-Z_]+\}\}') {
      Write-Host ("[Hook] Config file " + $f + " contains unreplaced placeholders (e.g. {{PROJECT_NAME}}), please replace with actual values.")
    }
  } catch {
    # File read failed, skip placeholder check
  }
}

# --- 3. Sensitive info detection for .claude/ config files ---
if ($f -match '^\.claude/') {
  $editContent = ""
  if ($toolInput.PSObject.Properties['new_string']) {
    $editContent = $toolInput.new_string
  }
  if ($toolInput.PSObject.Properties['content']) {
    $editContent = $toolInput.content
  }
  if ($editContent) {

    # 3a. Check against secrets.json real values
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
              if ($value -and $value.ToString().Trim() -ne "" -and $editContent -match [regex]::Escape($value.ToString())) {
                Write-Host ("[Hook] WARNING: Config file " + $f + " contains real sensitive value for '" + $key + "'. Use placeholder instead (e.g. {{" + $key.ToUpper() + "}}).")
              }
            }
          }
        }
      } catch {
        # secrets.json parsing failed, skip real-value check
      }
    }

    # 3b. Pattern-based sensitive detection
    $patternWarnings = @()

    # Credential in URL: mysql://user:pass@host, redis://:pass@host, etc.
    if ($editContent -match '[a-z]+://[^\s:]+:[^\s@]+@[^\s]+') {
      $patternWarnings += "Credential in URL detected (e.g. mysql://user:pass@host). Use placeholder instead."
    }

    # Hardcoded JWT secret / API key patterns
    if ($editContent -match '(?:jwt[_-]?secret|api[_-]?key|secret[_-]?key|access[_-]?token)\s*[=:]\s*[''"][A-Za-z0-9]{16,}[''"]') {
      $patternWarnings += "Hardcoded JWT secret/API key detected. Use placeholder instead."
    }

    # Private key content (BEGIN RSA/PRIVATE KEY)
    if ($editContent -match '-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----') {
      $patternWarnings += "Private key content detected. Store in secrets.json, use placeholder in config."
    }

    # Password in config without placeholder (password: value without {{...}})
    if ($editContent -match '(?:password|passwd|pwd)\s*[=:]\s*[''"][^{}'']{4,}[''"]') {
      $patternWarnings += "Hardcoded password detected. Use {{PLACEHOLDER}} format instead."
    }

    # AWS / cloud access key patterns
    if ($editContent -match '(?:AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16}') {
      $patternWarnings += "AWS access key detected. Store in secrets.json, use placeholder in config."
    }

    # Database connection string with credentials
    if ($editContent -match 'jdbc:[a-z]+://[^\s:]+:[^\s@]+@[^\s]+') {
      $patternWarnings += "JDBC URL with credentials detected. Use placeholder for password."
    }

    foreach ($warning in $patternWarnings) {
      Write-Host ("[Hook] WARNING: " + $warning)
    }
  }
}

exit 0
