# artify.ps1 — launcher for the standalone artify CLI via uv.
# Run without a global install: resolves the CLI's own requirements on demand.
#   .\artify.ps1 open FILE.html
#   .\artify.ps1 serve FILE.html [--webview]
#   .\artify.ps1 list | kill PORT | restart PORT | snapshot PORT [--timeout N]

$ErrorActionPreference = "Stop"

# This script lives in <skill>/scripts/, and the CLI project is <skill>/cli/.
$skillRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$cliDir = Join-Path $skillRoot "cli"

if (-not (Test-Path -LiteralPath $cliDir)) {
    Write-Error "artify: standalone CLI not found at $cliDir"
    exit 1
}

# Allow overriding uv if it's not on PATH.
$uv = if ($env:ARTIFY_UV) { $env:ARTIFY_UV } else { "uv" }

try {
    & $uv run --project $cliDir --quiet artify @args
    exit $LASTEXITCODE
}
catch {
    if ($_.Exception.Message -match "not recognized|not found") {
        Write-Error "artify: could not find 'uv' on PATH. Install it (https://docs.astral.sh/uv/) or set ARTIFY_UV to its path."
        exit 1
    }
    throw
}
