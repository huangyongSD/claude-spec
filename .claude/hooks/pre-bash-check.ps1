# PreToolUse Hook: Long-running command detection
# Usage: stdin receives JSON, output reminder to Host, exit code 0 allows

$stdin = [Console]::In.ReadToEnd()
if (-not $stdin) { echo 0; exit }

try { $j = $stdin | ConvertFrom-Json }
catch { echo 0; exit }

$PACKAGE_MANAGER = "mvn|yarn"
if ($j.command -and $j.command -match "^($PACKAGE_MANAGER)\s+(install|i|package|clean|compile|test)") {
  Write-Host "[Hook] Long-running command detected. Consider running in background."
}

echo 0
