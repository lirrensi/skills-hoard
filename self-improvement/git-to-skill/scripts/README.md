# git-to-skill Scripts

## scout.ps1 (Windows / PowerShell)

Automated repo scouting for Phase 1. Produces a structured JSON project profile.

```powershell
.\scout.ps1 -Path "C:\path\to\cloned\repo"
.\scout.ps1 -Path "C:\path\to\cloned\repo" -OutputFile "profile.json"
```

## scout.sh (Unix / Linux / macOS / WSL)

Same functionality, POSIX-compatible. Auto-detects if `jq` is available for richer
package.json parsing; degrades gracefully with `grep` fallback.

```bash
chmod +x scout.sh
./scout.sh /path/to/cloned/repo
./scout.sh /path/to/cloned/repo -o profile.json
```

**What both extract:**
| Field | Source |
|-------|--------|
| Git remote & branch | `git remote` / `git branch` |
| Description | First 15 lines of README (stripped headers) |
| License | LICENSE file first line |
| Top-level structure | `find` / `Get-ChildItem` at depth 1 |
| Language breakdown | File extension frequency analysis |
| Build system | package.json, pyproject.toml, Cargo.toml, go.mod, Makefile |
| Framework hints | Dependencies analysis |
| Category signals | CLI/app/library/monorepo/plugin heuristics |
| Complexity | File count thresholds (<20=simple, <100=moderate, 100+=complex) |

**JSON output format:**
```json
{
  "metadata": { "name": "...", "description": "...", "isGitRepo": true, "remoteUrl": "..." },
  "structure": { "topLevelDirs": "src, tests, docs", "topLevelFiles": "README.md, package.json", ... },
  "languages": { "detected": [...], "primary": "TypeScript", "frameworks": ["Node.js", "Express"] },
  "category": { "primary": "cli-tool", "confidence": 0.8, "signals": ["package.json:bin"] },
  "build": { "system": "pnpm", "scripts": { "build": "tsc", "test": "vitest" } },
  "complexity": "moderate"
}
```
