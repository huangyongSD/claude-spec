# PostToolUse Hook: Code file formatting reminder + config placeholder detection
# Usage: stdin receives JSON, output reminder to Host, exit code 0 allows

$stdin = [Console]::In.ReadToEnd()
if (-not $stdin) { echo 0; exit }

try { $j = $stdin | ConvertFrom-Json }
catch { echo 0; exit }

$f = $j.tool_input.file_path
if (-not $f) { echo 0; exit }

# Code file formatting reminder
$FILE_EXTENSIONS = "(java|xml|vue|js|sql)$"
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

echo 0
