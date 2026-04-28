# PostToolUse Hook: Code file formatting reminder + config placeholder detection + sensitive info detection
# Usage: stdin receives JSON, output reminder to Host, exit code 0 allows

$stdin = [Console]::In.ReadToEnd()
if (-not $stdin) { echo 0; exit }

try { $j = $stdin | ConvertFrom-Json }
catch { echo 0; exit }

$f = $j.tool_input.file_path
if (-not $f) { echo 0; exit }

# Code file formatting reminder
$FILE_EXTENSIONS = "(java|xml|vue|js|yaml|scss|sql)$"
if ($f -match $FILE_EXTENSIONS) {
  Write-Host ("[Hook] " + $j.tool_name + " file: " + $f + " - Format: backend 'mvn spotless:apply', frontend 'yarn lint'")
}

# Config file placeholder detection (only uppercase {{PLACEHOLDER}} format)
if ($f -match '^\.claude/' -and (Test-Path $f)) {
  $content = Get-Content $f -Raw
  if ($content -match '\{\{[A-Z][A-Z_]+\}\}') {
    Write-Host ("[Hook] Config file " + $f + " contains unreplaced placeholders (e.g. {{PROJECT_NAME}}), please replace with actual values.")
  }
}

# Sensitive info detection for .claude/ config files
if ($f -match '^\.claude/') {
  $editContent = ""
  if ($j.tool_input.PSObject.Properties['new_string']) {
    $editContent = $j.tool_input.new_string
  }
  if ($j.tool_input.PSObject.Properties['content']) {
    $editContent = $j.tool_input.content
  }
  if ($editContent) {
    $secretsPath = Join-Path $PSScriptRoot "..\tools\secrets.json"
    if (Test-Path $secretsPath) {
      try {
        $secrets = Get-Content $secretsPath -Raw | ConvertFrom-Json
        $realValues = $secrets.real_values
        $sensitiveKeys = @(
          'db_master_password', 'db_master_host',
          'db_slave_password', 'db_slave_host',
          'redis_password', 'redis_host'
        )
        foreach ($key in $sensitiveKeys) {
          if ($realValues.PSObject.Properties[$key]) {
            $value = $realValues.($key)
            if ($value -and $value.ToString().Trim() -ne "" -and $editContent -match [regex]::Escape($value.ToString())) {
              Write-Host ("[Hook] Config file " + $f + " contains real sensitive value for '" + $key + "'. Use placeholder instead (e.g. {{" + $key.ToUpper() + "}}).")
            }
          }
        }
      } catch {
        # If secrets.json parsing fails, skip
      }
    }
  }
}

echo 0
