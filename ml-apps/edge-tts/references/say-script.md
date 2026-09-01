# Complete Say.ps1 Script

When the user wants a full CLI wrapper script, generate this:

```powershell
<#
.SYNOPSIS
    TTS CLI wrapper around edge-tts / edge-playback.

.DESCRIPTION
    Speaks text aloud or saves to MP3. Supports pipeline input,
    voice selection, rate/volume/pitch control, and voice listing/search.

.EXAMPLE
    .\Say.ps1 "Hello world"
    .\Say.ps1 -Text "Hello" -Voice "en-US-AriaNeural" -Rate "+20%"
    .\Say.ps1 -Text "Hello" -OutFile speech.mp3
    .\Say.ps1 -List
    .\Say.ps1 -Search "en-GB"
    "Hello from pipeline" | .\Say.ps1
#>

[CmdletBinding(DefaultParameterSetName = 'Speak')]
param(
    [Parameter(ParameterSetName='Speak', Position=0, ValueFromPipeline=$true)]
    [string]$Text,

    [Parameter(ParameterSetName='Speak')]
    [string]$Voice = 'en-US-AriaNeural',

    [Parameter(ParameterSetName='Speak')]
    [string]$Rate = '+0%',

    [Parameter(ParameterSetName='Speak')]
    [string]$Volume = '+0%',

    [Parameter(ParameterSetName='Speak')]
    [string]$Pitch = '+0Hz',

    [Parameter(ParameterSetName='Speak')]
    [string]$OutFile,

    [Parameter(ParameterSetName='Speak')]
    [switch]$Also,

    [Parameter(ParameterSetName='List', Mandatory)]
    [switch]$List,

    [Parameter(ParameterSetName='Search', Mandatory)]
    [string]$Search
)

begin {
    if (-not (Get-Command edge-tts -ErrorAction SilentlyContinue)) {
        Write-Error "edge-tts not found. Install with: uv tool install edge-tts"
        exit 1
    }
    if ($PSCmdlet.ParameterSetName -eq 'List') {
        edge-tts --list-voices
        return
    }
    if ($PSCmdlet.ParameterSetName -eq 'Search') {
        Write-Host "Voices matching '$Search':" -ForegroundColor Cyan
        edge-tts --list-voices | Select-String $Search
        return
    }
}

process {
    if ($PSCmdlet.ParameterSetName -ne 'Speak') { return }
    if (-not $Text) { return }

    $baseArgs = @(
        '--voice',  $Voice,
        '--rate',   $Rate,
        '--volume', $Volume,
        '--pitch',  $Pitch,
        '--text',   $Text
    )

    if ($OutFile) {
        & edge-tts @baseArgs --write-media $OutFile
        Write-Host "Saved to: $OutFile" -ForegroundColor Green
        if ($Also) { & edge-playback @baseArgs }
    } else {
        & edge-playback @baseArgs
    }
}
```

## Pipeline Examples

```powershell
# Simple string
"Good morning!" | .\Say.ps1

# From file
Get-Content notes.txt | .\Say.ps1 -Voice "en-GB-SoniaNeural"

# Command output
(Get-Date -Format "dddd, MMMM d") | .\Say.ps1

# Save to file
"Hello" | .\Say.ps1 -OutFile hello.mp3

# Speak AND save
.\Say.ps1 -Text "Hello" -OutFile hello.mp3 -Also
```
