# make-offline.ps1 — PowerShell wrapper for make-offline.py
# Usage:
#   .\make-offline.ps1 input.html
#   .\make-offline.ps1 input.html --backup
#   .\make-offline.ps1 input.html -o output.html
#   .\make-offline.ps1 input.html --dry-run
#   .\make-offline.ps1 input.html --clear-cache

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "make-offline.py"

# Check if python is available
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $python) {
    Write-Error "Python not found. Install Python 3.7+ and ensure it's on PATH."
    exit 1
}

& $python.Source $pythonScript @args
