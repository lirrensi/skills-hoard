#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Scout a git repository and output a structured JSON project profile.
.DESCRIPTION
    Phase 1 automation for git-to-skill. Analyzes a repo's structure, metadata,
    language, and category signals. Outputs a JSON profile consumed by Phase 2.
.PARAMETER Path
    Path to the local repository (cloned already).
.PARAMETER OutputFile
    Where to write the JSON profile. Defaults to stdout.
.EXAMPLE
    .\scout.ps1 -Path "C:\temp\git-to-skill-12345\repo"
#>

param(
    [Parameter(Mandatory)]
    [string]$Path,

    [string]$OutputFile
)

# Resolve to absolute path
$repoPath = Resolve-Path -LiteralPath $Path -ErrorAction Stop

# --- Helper functions ---

function Test-FileExists($relativePath) {
    Test-Path -LiteralPath (Join-Path $repoPath $relativePath) -PathType Leaf
}

function Test-DirExists($relativePath) {
    Test-Path -LiteralPath (Join-Path $repoPath $relativePath) -PathType Container
}

function Get-FileContent($relativePath) {
    $fullPath = Join-Path $repoPath $relativePath
    if (Test-Path -LiteralPath $fullPath) {
        return Get-Content -LiteralPath $fullPath -Raw -ErrorAction SilentlyContinue
    }
    return $null
}

function Get-ReadmeSummary($filePath) {
    $content = Get-Content -LiteralPath $filePath -TotalCount 200 -ErrorAction SilentlyContinue
    if (-not $content) { return "" }
    # Extract first meaningful paragraph
    $inParagraph = $false
    $lines = @()
    foreach ($line in $content) {
        $trimmed = $line.Trim()
        if ($trimmed -and -not $trimmed.StartsWith('#') -and -not $trimmed.StartsWith('[')) {
            $inParagraph = $true
            $lines += $trimmed
        } elseif ($inParagraph -and -not $trimmed) {
            break
        }
    }
    return ($lines -join " ").Substring(0, [Math]::Min(300, ($lines -join " ").Length))
}

function Get-RelevantFiles($root, $patterns) {
    $results = @()
    foreach ($pattern in $patterns) {
        $files = Get-ChildItem -LiteralPath $root -Filter $pattern -Depth 0 -ErrorAction SilentlyContinue
        foreach ($file in $files) {
            $results += $file.Name
        }
    }
    return ($results | Select-Object -Unique)
}

# --- Primary probes ---

$profile = [PSCustomObject]@{
    metadata  = [PSCustomObject]@{
        name           = (Split-Path -Leaf $repoPath)
        fullPath       = $repoPath
        isGitRepo      = (Test-Path -LiteralPath (Join-Path $repoPath ".git") -PathType Container)
        remoteUrl      = $null
        defaultBranch  = $null
        description    = ""
        license        = $null
    }
    structure = [PSCustomObject]@{
        topLevelDirs   = @()
        topLevelFiles  = @()
        hasSrc         = (Test-DirExists "src")
        hasLib         = (Test-DirExists "lib")
        hasDocs        = (Test-DirExists "docs")
        hasExamples    = (Test-DirExists "examples") -or (Test-DirExists "example")
        hasTests       = (Test-DirExists "tests") -or (Test-DirExists "test") -or (Test-DirExists "__tests__")
        hasGithubDir   = (Test-DirExists ".github")
        hasDocker      = (Test-FileExists "Dockerfile") -or (Test-FileExists "docker-compose.yml")
    }
    languages = [PSCustomObject]@{
        detected       = @()
        primary        = $null
        frameworks     = @()
    }
    category  = [PSCustomObject]@{
        primary         = "unknown"
        confidence      = 0.0
        alternatives    = @()
        signals         = @()
    }
    build     = [PSCustomObject]@{
        system          = $null
        testFramework   = $null
        packageManager  = $null
        scripts         = @{}
    }
    existingCli = [PSCustomObject]@{
        hasCli          = $false
        entryPoints     = @()
        names           = @()
    }
    complexity = "unknown"
}

# --- Git remote ---
try {
    $remote = git -C $repoPath remote get-url origin 2>$null
    if ($remote) { $profile.metadata.remoteUrl = $remote.Trim() }

    $branch = git -C $repoPath branch --show-current 2>$null
    if ($branch) { $profile.metadata.defaultBranch = $branch.Trim() }

    $description = Get-ReadmeSummary (Join-Path $repoPath "README.md")
    if (-not $description) { $description = Get-ReadmeSummary (Join-Path $repoPath "README") }
    $profile.metadata.description = $description
}
catch { }

# --- Top-level structure ---
$rootItems = Get-ChildItem -LiteralPath $repoPath -Depth 0 -ErrorAction SilentlyContinue
$profile.structure.topLevelDirs = ($rootItems | Where-Object { $_.PSIsContainer } | ForEach-Object { $_.Name }) -join ", "
$profile.structure.topLevelFiles = ($rootItems | Where-Object { -not $_.PSIsContainer } | ForEach-Object { $_.Name }) -join ", "

# --- License ---
$licenseFiles = @("LICENSE", "LICENSE.txt", "LICENSE.md", "LICENSE.mit")
foreach ($lf in $licenseFiles) {
    $lfp = Join-Path $repoPath $lf
    if (Test-Path -LiteralPath $lfp) {
        $firstLine = Get-Content -LiteralPath $lfp -TotalCount 1 -ErrorAction SilentlyContinue
        if ($firstLine) { $profile.metadata.license = $firstLine.Trim() }
        break
    }
}

# --- Language detection ---
$extCounts = @{}
$trackedFiles = git -C $repoPath ls-files 2>$null
if (-not $trackedFiles) {
    $trackedFiles = Get-ChildItem -LiteralPath $repoPath -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object { $_.FullName.Substring($repoPath.Length + 1) }
}

foreach ($file in $trackedFiles) {
    $ext = [System.IO.Path]::GetExtension($file).ToLower()
    if ($ext -and $ext -ne '') { $extCounts[$ext] = ($extCounts[$ext] + 1) }
}

$extLangMap = @{
    '.py' = 'Python'; '.rs' = 'Rust'; '.go' = 'Go'; '.ts' = 'TypeScript'
    '.js' = 'JavaScript'; '.tsx' = 'TypeScript'; '.jsx' = 'JavaScript'
    '.rb' = 'Ruby'; '.java' = 'Java'; '.kt' = 'Kotlin'; '.swift' = 'Swift'
    '.c' = 'C'; '.cpp' = 'C++'; '.h' = 'C'; '.hpp' = 'C++'
    '.cs' = 'C#'; '.php' = 'PHP'; '.r' = 'R'; '.m' = 'MATLAB'
    '.scala' = 'Scala'; '.zig' = 'Zig'; '.nim' = 'Nim'; '.ex' = 'Elixir'
    '.exs' = 'Elixir'; '.clj' = 'Clojure'; '.hs' = 'Haskell'
    '.lua' = 'Lua'; '.sh' = 'Shell'; '.bash' = 'Shell'; '.ps1' = 'PowerShell'
    '.sql' = 'SQL'; '.vue' = 'Vue'; '.svelte' = 'Svelte'; '.astro' = 'Astro'
    '.dart' = 'Dart'; '.ml' = 'OCaml'
}

$sortedExts = $extCounts.GetEnumerator() | Sort-Object Value -Descending
$profile.languages.detected = $sortedExts | ForEach-Object {
    $lang = $extLangMap[$_.Name]
    if ($lang) {
        [PSCustomObject]@{ extension = $_.Name; count = $_.Value; language = $lang }
    } else {
        [PSCustomObject]@{ extension = $_.Name; count = $_.Value; language = "Unknown" }
    }
} | Where-Object { $_.language -ne "Unknown" }

if ($profile.languages.detected.Count -gt 0) {
    $topLang = $profile.languages.detected | Sort-Object count -Descending | Select-Object -First 1
    $profile.languages.primary = $topLang.language
}

# --- Framework detection ---
$frameworks = @()

# Node.js / npm
if (Test-FileExists "package.json") {
    $pkg = Get-FileContent "package.json" | ConvertFrom-Json -ErrorAction SilentlyContinue
    if ($pkg) {
        $frameworks += "Node.js"
        if ($pkg.bin) { $profile.category.signals += "package.json:bin" }
        if ($pkg.workspaces) { $profile.category.signals += "package.json:workspaces" }
        $profile.build.system = if ($pkg.scripts) { "npm/pnpm" } else { $profile.build.system }
        if ($pkg.scripts) {
            $profile.build.scripts = $pkg.scripts
        }
        # Detect framework from deps
        $allDeps = @{}
        if ($pkg.dependencies) { $pkg.dependencies.PSObject.Properties | ForEach-Object { $allDeps[$_.Name] = $_.Value } }
        if ($pkg.devDependencies) { $pkg.devDependencies.PSObject.Properties | ForEach-Object { $allDeps[$_.Name] = $_.Value } }
        $allDeps.Keys | ForEach-Object {
            if ($_ -match '^@nestjs/') { $frameworks += "NestJS" }
            elseif ($_ -eq 'express') { $frameworks += "Express" }
            elseif ($_ -eq 'react' -or $_ -eq 'next') { $frameworks += "React" }
            elseif ($_ -eq 'vue') { $frameworks += "Vue" }
            elseif ($_ -eq 'svelte') { $frameworks += "Svelte" }
        }
        # Package manager detection
        if (Test-FileExists "pnpm-lock.yaml") { $profile.build.packageManager = "pnpm" }
        elseif (Test-FileExists "yarn.lock") { $profile.build.packageManager = "yarn" }
        elseif (Test-FileExists "package-lock.json") { $profile.build.packageManager = "npm" }
    }
}

# Python
if (Test-FileExists "pyproject.toml") {
    $pyproject = Get-FileContent "pyproject.toml"
    if ($pyproject) {
        $frameworks += "Python"
        $profile.build.system = "pyproject.toml"
        if ($pyproject -match '\[project\.scripts\]') { $profile.category.signals += "pyproject.toml:scripts" }
        if ($pyproject -match 'ui|web|app|server') { $frameworks += "Web App" }
    }
}
if (Test-FileExists "setup.py") {
    $frameworks += "Python"
    $profile.build.system = "setup.py"
    $setupContent = Get-FileContent "setup.py"
    if ($setupContent -and $setupContent -match 'console_scripts') { $profile.category.signals += "setup.py:console_scripts" }
}
if (Test-FileExists "setup.cfg") {
    $frameworks += "Python"
    if (-not $profile.build.system) { $profile.build.system = "setup.cfg" }
}

# Rust
if (Test-FileExists "Cargo.toml") {
    $frameworks += "Rust"
    $profile.build.system = "Cargo"
    $cargo = Get-FileContent "Cargo.toml"
    if ($cargo) {
        if ($cargo -match '\[\[bin\]\]') { $profile.category.signals += "Cargo.toml:bin" }
        if ($cargo -match '\[lib\]') { $profile.category.signals += "Cargo.toml:lib" }
        if ($cargo -match '\[workspace\]') { $profile.category.signals += "Cargo.toml:workspace" }
    }
    if (Test-FileExists "rust-toolchain") { $frameworks += "Rust Toolchain" }
}

# Go
if (Test-FileExists "go.mod") {
    $frameworks += "Go"
    $profile.build.system = "go mod"
    if (Test-DirExists "cmd") { $profile.category.signals += "cmd/" }
}

# Makefile
if (Test-FileExists "Makefile") {
    $profile.build.system = if ($profile.build.system) { "$($profile.build.system), Makefile" } else { "Makefile" }
}

# --- Category detection ---
$signals = $profile.category.signals

# Monorepo
if (Test-FileExists "pnpm-workspace.yaml") { $signals += "pnpm-workspace.yaml" }
if (Test-FileExists "lerna.json") { $signals += "lerna.json" }
if (Test-FileExists "turbo.json") { $signals += "turbo.json" }
if (Test-FileExists "go.work") { $signals += "go.work" }

# --- Existing CLI detection ---
$cliSignalPatterns = @("package.json:bin", "pyproject.toml:scripts", "setup.py:console_scripts", "Cargo.toml:bin", "cmd/")
$cliSignals = $signals | Where-Object { $_ -in $cliSignalPatterns }
if ($cliSignals.Count -gt 0) {
    $profile.existingCli.hasCli = $true
    $profile.existingCli.entryPoints = $cliSignals
    # Extract CLI names from signals
    $cliNames = @()
    if ($signals -contains "package.json:bin") {
        try {
            $pkg = Get-FileContent "package.json" | ConvertFrom-Json
            if ($pkg.bin -is [string]) { $cliNames += $pkg.bin }
            elseif ($pkg.bin -is [PSObject]) { $cliNames += $pkg.bin.PSObject.Properties.Name }
        } catch {}
    }
    if ($signals -contains "pyproject.toml:scripts") {
        $content = Get-FileContent "pyproject.toml"
        $lines = $content -split "`n"
        $inScripts = $false
        foreach ($line in $lines) {
            if ($line -match '^\[project\.scripts\]') { $inScripts = $true; continue }
            if ($inScripts -and $line -match '^\[') { break }
            if ($inScripts -and $line -match '^\s*(\S+)\s*=') { $cliNames += $Matches[1] }
        }
    }
    if ($signals -contains "setup.py:console_scripts") {
        $content = Get-FileContent "setup.py"
        if ($content -match "console_scripts\s*=\s*\[([^\]]+)\]") {
            $scriptsBlock = $Matches[1]
            $scriptsBlock -split ',' | ForEach-Object {
                if ($_ -match "'([^']+)'") { $cliNames += $Matches[1] }
            }
        }
    }
    if ($signals -contains "Cargo.toml:bin") {
        $content = Get-FileContent "Cargo.toml"
        $lines = $content -split "`n"
        $inBin = $false
        foreach ($line in $lines) {
            if ($line -match '^\[\[bin\]\]') { $inBin = $true; continue }
            if ($inBin -and $line -match '^\[') { break }
            if ($inBin -and $line -match 'name\s*=\s*"([^"]+)"') { $cliNames += $Matches[1] }
        }
    }
    $profile.existingCli.names = ($cliNames | Where-Object { $_ -ne "" }) -join ", "
}

# Application signals
if (Test-FileExists "Dockerfile") { $signals += "Dockerfile" }
if (Test-FileExists "docker-compose.yml") { $signals += "docker-compose.yml" }
if (Test-FileExists ".env.example") { $signals += ".env.example" }
if (Test-FileExists "Procfile") { $signals += "Procfile" }
if (Test-FileExists "fly.toml") { $signals += "fly.toml" }
if (Test-FileExists "vercel.json") { $signals += "vercel.json" }

# Template signals
if (Test-FileExists "cookiecutter.json") { $signals += "cookiecutter.json" }

# Plugin signals
if (Test-FileExists "plugin.json") { $signals += "plugin.json" }
if (Test-FileExists "extension.json") { $signals += "extension.json" }

# --- Categorization logic ---
$clisignals = @("package.json:bin", "pyproject.toml:scripts", "setup.py:console_scripts", "Cargo.toml:bin", "cmd/")
$libsignals = @("Cargo.toml:lib")
$appsignals = @("Dockerfile", "docker-compose.yml", ".env.example", "Procfile", "fly.toml", "vercel.json")
$monosignals = @("pnpm-workspace.yaml", "lerna.json", "turbo.json", "go.work", "package.json:workspaces", "Cargo.toml:workspace")
$pluginsignals = @("plugin.json", "extension.json")

$cliMatch = $signals | Where-Object { $_ -in $clisignals } | Measure-Object
$libMatch = $signals | Where-Object { $_ -in $libsignals } | Measure-Object
$appMatch = $signals | Where-Object { $_ -in $appsignals } | Measure-Object
$monoMatch = $signals | Where-Object { $_ -in $monosignals } | Measure-Object
$pluginMatch = $signals | Where-Object { $_ -in $pluginsignals } | Measure-Object

# Prioritize: mono > CLI > app > plugin > lib > unknown
if ($monoMatch.Count -gt 0) {
    $profile.category.primary = "monorepo"
    $profile.category.confidence = [Math]::Min(1.0, $monoMatch.Count * 0.35)
} elseif ($cliMatch.Count -gt 0) {
    $profile.category.primary = "cli-tool"
    $profile.category.confidence = [Math]::Min(1.0, $cliMatch.Count * 0.35)
} elseif ($appMatch.Count -gt 0) {
    $profile.category.primary = "application"
    $profile.category.confidence = [Math]::Min(1.0, $appMatch.Count * 0.35)
} elseif ($pluginMatch.Count -gt 0) {
    $profile.category.primary = "plugin"
    $profile.category.confidence = [Math]::Min(1.0, $pluginMatch.Count * 0.35)
} elseif ($libMatch.Count -gt 0) {
    $profile.category.primary = "library"
    $profile.category.confidence = [Math]::Min(1.0, $libMatch.Count * 0.35)
} else {
    # Guess from directory structure
    if ($profile.structure.hasTests -or $profile.languages.primary) {
        $profile.category.primary = "application"
        $profile.category.confidence = 0.3
    } else {
        $profile.category.primary = "unknown"
        $profile.category.confidence = 0.1
    }
}

if ($frameworks.Count -gt 0) {
    $profile.languages.frameworks = $frameworks | Select-Object -Unique
}

# --- Complexity ---
$totalFiles = $trackedFiles.Count
if ($totalFiles -lt 20) { $profile.complexity = "simple" }
elseif ($totalFiles -lt 100) { $profile.complexity = "moderate" }
else { $profile.complexity = "complex" }

# --- Write output ---
$json = $profile | ConvertTo-Json -Depth 5
if ($OutputFile) {
    $json | Out-File -LiteralPath $OutputFile -Encoding utf8
    Write-Host "Profile written to $OutputFile"
} else {
    $json
}
