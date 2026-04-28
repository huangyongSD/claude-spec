# PostToolUse hook: sensitive-scan
# When Edit/Write tools write content, check for sensitive values

param(
    [string]$InputJson
)

# Read stdin if no argument provided
if (-not $InputJson) {
    $InputJson = [System.Console]::In.ReadToEnd()
}

try {
    $data = $InputJson | ConvertFrom-Json
} catch {
    exit 0
}

# Determine the content to check and file path
$filePath = ""
$content = ""

if ($data.PSObject.Properties['tool_input']) {
    $toolInput = $data.tool_input
    if ($toolInput.PSObject.Properties['file_path']) {
        $filePath = $toolInput.file_path
    }
    # Edit tool uses new_string
    if ($toolInput.PSObject.Properties['new_string']) {
        $content = $toolInput.new_string
    }
    # Write tool uses content
    if ($toolInput.PSObject.Properties['content']) {
        $content = $toolInput.content
    }
}

if (-not $content) {
    exit 0
}

# Read secrets.json to get real values
$secretsPath = Join-Path $PSScriptRoot "..\tools\secrets.json"
$foundSensitive = @()

if (Test-Path $secretsPath) {
    try {
        $secrets = Get-Content $secretsPath -Raw | ConvertFrom-Json
        $realValues = $secrets.real_values

        # Check each real value against content
        # Skip empty values and common non-sensitive ones
        $sensitiveKeys = @(
            'db_master_password', 'db_master_host', 'db_master_url',
            'db_slave_password', 'db_slave_host', 'db_slave_url',
            'redis_password', 'redis_host'
        )

        foreach ($key in $sensitiveKeys) {
            if ($realValues.PSObject.Properties[$key]) {
                $value = $realValues.($key)
                if ($value -and $value.ToString().Trim() -ne "" -and $content -match [regex]::Escape($value.ToString())) {
                    $foundSensitive += $key
                }
            }
        }
    } catch {
        # If secrets.json parsing fails, skip real-value check
    }
}

# Also check for common password patterns
# Pattern: password: followed by a non-placeholder value
$passwordPattern = [regex]::new('password:\s*[^\s{][^\n]*', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
$matches = $passwordPattern.Matches($content)
foreach ($m in $matches) {
    $matchValue = $m.Value
    # Skip if it contains a placeholder like {{...}}
    if ($matchValue -notmatch '\{\{.*\}\}') {
        $foundSensitive += "password-pattern: $matchValue"
    }
}

if ($foundSensitive.Count -gt 0) {
    Write-Output "[Hook] Sensitive information detected in file $filePath. Use placeholders instead. Run 'python .claude/tools/secrets-sync.py --scan-configs' for replacement suggestions."
}

# Always exit 0 (reminder only, not blocking)
exit 0