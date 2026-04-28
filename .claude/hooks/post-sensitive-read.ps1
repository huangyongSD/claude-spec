# PostToolUse hook: sensitive-read
# When Read tool accesses application YAML files, remind about sensitive info

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
    # If JSON parsing fails, just exit
    exit 0
}

# Get file_path from hook data
$filePath = ""
if ($data.PSObject.Properties['tool_input']) {
    $toolInput = $data.tool_input
    if ($toolInput.PSObject.Properties['file_path']) {
        $filePath = $toolInput.file_path
    }
}

# Check if the file_path matches application YAML patterns
if ($filePath -match 'application-.*\.ya?ml$') {
    Write-Output "[Hook] This file contains sensitive information (passwords/host IPs). Do not use real values in subsequent operations. For database operations, use /sdc-dbquery or 'python .claude/tools/db-query.py'."
}

# Always exit 0 (reminder only, not blocking)
exit 0