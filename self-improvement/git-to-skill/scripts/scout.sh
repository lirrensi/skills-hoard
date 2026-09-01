#!/usr/bin/env bash
# Scout a git repository and output a structured JSON project profile.
# Phase 1 automation for git-to-skill.
#
# Usage:
#   ./scout.sh /path/to/repo            # outputs JSON to stdout
#   ./scout.sh /path/to/repo -o profile.json

set -euo pipefail

REPO_PATH=""
OUTPUT_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--output) OUTPUT_FILE="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: $0 <repo-path> [-o output.json]"
      exit 0 ;;
    *) REPO_PATH="$1"; shift ;;
  esac
done

if [[ -z "$REPO_PATH" ]]; then
  echo '{"error":"No repo path provided","usage":"scout.sh <repo-path> [-o output.json]"}' >&2
  exit 1
fi

if [[ ! -d "$REPO_PATH" ]]; then
  echo '{"error":"Path does not exist or is not a directory","path":"'"$REPO_PATH"'"}' >&2
  exit 1
fi

# Resolve to absolute path
REPO_PATH="$(cd "$REPO_PATH" && pwd)"
REPO_NAME="$(basename "$REPO_PATH")"

# --- Helper: check file/dir existence ---
has_file() { [[ -f "$REPO_PATH/$1" ]]; }
has_dir()  { [[ -d "$REPO_PATH/$1" ]]; }

# --- Helper: read first N lines of a file, strip markdown headers ---
read_first_lines() {
  local file="$REPO_PATH/$1" max_lines="${2:-10}"
  if [[ ! -f "$file" ]]; then echo ""; return; fi
  head -n "$max_lines" "$file" 2>/dev/null | sed '/^#/d' | tr '\n' ' ' | sed 's/  */ /g' | cut -c1-300
}

# --- Git metadata ---
GIT_REPO=false
REMOTE_URL=null
DEFAULT_BRANCH=null
if has_dir ".git"; then
  GIT_REPO=true
  REMOTE_URL=$(git -C "$REPO_PATH" remote get-url origin 2>/dev/null || echo null)
  DEFAULT_BRANCH=$(git -C "$REPO_PATH" branch --show-current 2>/dev/null || echo null)
fi

DESCRIPTION=$(read_first_lines "README.md" 15)
[[ -z "$DESCRIPTION" ]] && DESCRIPTION=$(read_first_lines "README" 15)
[[ -z "$DESCRIPTION" ]] && DESCRIPTION=""

# --- License ---
LICENSE=null
for lf in LICENSE LICENSE.txt LICENSE.md LICENSE.mit; do
  if has_file "$lf"; then
    LICENSE=$(head -1 "$REPO_PATH/$lf" 2>/dev/null | sed 's/"/\\"/g')
    break
  fi
done

# --- Top-level structure ---
TOP_DIRS=$(find "$REPO_PATH" -maxdepth 1 -type d ! -name ".git" ! -path "$REPO_PATH" -printf '%f\n' 2>/dev/null | sort | tr '\n' ',' | sed 's/,$//')
TOP_FILES=$(find "$REPO_PATH" -maxdepth 1 -type f -printf '%f\n' 2>/dev/null | sort | tr '\n' ',' | sed 's/,$//')

# --- Structure booleans ---
HAS_SRC=$(has_dir "src" && echo true || echo false)
HAS_LIB=$(has_dir "lib" && echo true || echo false)
HAS_DOCS=$(has_dir "docs" && echo true || echo false)
HAS_EXAMPLES=$({ has_dir "examples" || has_dir "example"; } && echo true || echo false)
HAS_TESTS=$({ has_dir "tests" || has_dir "test" || has_dir "__tests__"; } && echo true || echo false)
HAS_CI=$(has_dir ".github" && echo true || echo false)
HAS_DOCKER=$({ has_file "Dockerfile" || has_file "docker-compose.yml"; } && echo true || echo false)

# --- Language detection (by extension count) ---
declare -A EXT_LANG=(
  [py]=Python [rs]=Rust [go]=Go [ts]=TypeScript [js]=JavaScript
  [tsx]=TypeScript [jsx]=JavaScript [rb]=Ruby [java]=Java [kt]=Kotlin
  [swift]=Swift [c]=C [cpp]="C++" [h]=C [hpp]="C++" [cs]="C#"
  [php]=PHP [r]=R [scala]=Scala [zig]=Zig [lua]=Lua [sh]=Shell
  [bash]=Shell [ps1]=PowerShell [sql]=SQL [vue]=Vue [svelte]=Svelte
  [dart]=Dart [ex]=Elixir [exs]=Elixir [hs]=Haskell [ml]=OCaml
  [clj]=Clojure [nim]=Nim
)

EXT_COUNTS=$(mktemp)
# Count file extensions from git-tracked files, or all files if not a git repo
if $GIT_REPO; then
  git -C "$REPO_PATH" ls-files 2>/dev/null | while IFS= read -r f; do
    ext="${f##*.}"
    [[ "$ext" != "$f" && -n "$ext" ]] && echo "$ext"
  done | sort | uniq -c | sort -rn > "$EXT_COUNTS"
else
  find "$REPO_PATH" -type f 2>/dev/null | while IFS= read -r f; do
    ext="${f##*.}"
    [[ "$ext" != "$(basename "$f")" && -n "$ext" ]] && echo "$ext"
  done | sort | uniq -c | sort -rn > "$EXT_COUNTS"
fi

# Build languages JSON array
LANG_DETECTED="["
FIRST_LANG=true
PRIMARY_LANG=""
MAX_COUNT=0
while read -r count ext; do
  lang="${EXT_LANG[$ext]:-}"
  [[ -z "$lang" ]] && continue
  $FIRST_LANG || LANG_DETECTED+=","
  FIRST_LANG=false
  LANG_DETECTED+='{"extension":".'"$ext"'","count":'"$count"',"language":"'"$lang"'"}'
  if [[ "$count" -gt "$MAX_COUNT" ]]; then
    MAX_COUNT="$count"
    PRIMARY_LANG="$lang"
  fi
done < "$EXT_COUNTS"
LANG_DETECTED+="]"
rm -f "$EXT_COUNTS"
[[ -z "$PRIMARY_LANG" ]] && PRIMARY_LANG="Unknown"

# --- Framework detection ---
FRAMEWORKS=()
CAT_SIGNALS=()
BUILD_SYSTEM=""

# Node.js
if has_file "package.json"; then
  FRAMEWORKS+=("Node.js")
  BUILD_SYSTEM="npm/pnpm"
  if command -v jq &>/dev/null; then
    HAS_BIN=$(jq '.bin // empty' "$REPO_PATH/package.json" 2>/dev/null && echo true || echo false)
    HAS_WORKSPACES=$(jq '.workspaces // empty' "$REPO_PATH/package.json" 2>/dev/null && echo true || echo false)
    [[ "$HAS_BIN" == true ]] && CAT_SIGNALS+=("package.json:bin")
    [[ "$HAS_WORKSPACES" == true ]] && CAT_SIGNALS+=("package.json:workspaces")
  else
    grep -q '"bin"' "$REPO_PATH/package.json" 2>/dev/null && CAT_SIGNALS+=("package.json:bin")
    grep -q '"workspaces"' "$REPO_PATH/package.json" 2>/dev/null && CAT_SIGNALS+=("package.json:workspaces")
  fi
  if has_file "pnpm-lock.yaml"; then BUILD_SYSTEM="pnpm"
  elif has_file "yarn.lock"; then BUILD_SYSTEM="yarn"
  elif has_file "package-lock.json"; then BUILD_SYSTEM="npm"; fi
fi

# Python
if has_file "pyproject.toml"; then
  FRAMEWORKS+=("Python")
  BUILD_SYSTEM="${BUILD_SYSTEM:+$BUILD_SYSTEM, }pyproject.toml"
  grep -q '\[project\.scripts\]' "$REPO_PATH/pyproject.toml" 2>/dev/null && CAT_SIGNALS+=("pyproject.toml:scripts")
fi
if has_file "setup.py"; then
  FRAMEWORKS+=("Python")
  BUILD_SYSTEM="${BUILD_SYSTEM:+$BUILD_SYSTEM, }setup.py"
  grep -q 'console_scripts' "$REPO_PATH/setup.py" 2>/dev/null && CAT_SIGNALS+=("setup.py:console_scripts")
fi
if has_file "setup.cfg"; then
  FRAMEWORKS+=("Python")
  BUILD_SYSTEM="${BUILD_SYSTEM:+$BUILD_SYSTEM, }setup.cfg"
fi

# Rust
if has_file "Cargo.toml"; then
  FRAMEWORKS+=("Rust")
  BUILD_SYSTEM="${BUILD_SYSTEM:+$BUILD_SYSTEM, }Cargo"
  grep -q '\[\[bin\]\]' "$REPO_PATH/Cargo.toml" 2>/dev/null && CAT_SIGNALS+=("Cargo.toml:bin")
  grep -q '\[lib\]' "$REPO_PATH/Cargo.toml" 2>/dev/null && CAT_SIGNALS+=("Cargo.toml:lib")
  grep -q '\[workspace\]' "$REPO_PATH/Cargo.toml" 2>/dev/null && CAT_SIGNALS+=("Cargo.toml:workspace")
fi

# Go
if has_file "go.mod"; then
  FRAMEWORKS+=("Go")
  BUILD_SYSTEM="${BUILD_SYSTEM:+$BUILD_SYSTEM, }go mod"
  has_dir "cmd" && CAT_SIGNALS+=("cmd/")
fi

# Makefile
has_file "Makefile" && BUILD_SYSTEM="${BUILD_SYSTEM:+$BUILD_SYSTEM, }Makefile"

# Monorepo signals
has_file "pnpm-workspace.yaml" && CAT_SIGNALS+=("pnpm-workspace.yaml")
has_file "lerna.json" && CAT_SIGNALS+=("lerna.json")
has_file "turbo.json" && CAT_SIGNALS+=("turbo.json")
has_file "go.work" && CAT_SIGNALS+=("go.work")

# App signals
has_file "Dockerfile" && CAT_SIGNALS+=("Dockerfile")
has_file "docker-compose.yml" && CAT_SIGNALS+=("docker-compose.yml")
has_file ".env.example" && CAT_SIGNALS+=(".env.example")
has_file "Procfile" && CAT_SIGNALS+=("Procfile")
has_file "fly.toml" && CAT_SIGNALS+=("fly.toml")
has_file "vercel.json" && CAT_SIGNALS+=("vercel.json")

# Plugin signals
has_file "plugin.json" && CAT_SIGNALS+=("plugin.json")
has_file "extension.json" && CAT_SIGNALS+=("extension.json")

# Template signals
has_file "cookiecutter.json" && CAT_SIGNALS+=("cookiecutter.json")

# --- Existing CLI detection ---
EXISTING_CLI_NAMES=""
CLI_ENTRY_SIGNALS=()
for s in "${CAT_SIGNALS[@]}"; do
  case "$s" in
    package.json:bin|pyproject.toml:scripts|setup.py:console_scripts|Cargo.toml:bin|cmd/)
      CLI_ENTRY_SIGNALS+=("$s") ;;
  esac
done

if [[ ${#CLI_ENTRY_SIGNALS[@]} -gt 0 ]]; then
  # Extract CLI names from signals
  for s in "${CLI_ENTRY_SIGNALS[@]}"; do
    case "$s" in
      package.json:bin)
        if command -v jq &>/dev/null; then
          BIN_NAMES=$(jq -r '.bin | if type == "string" then . else keys[] end' "$REPO_PATH/package.json" 2>/dev/null | tr '\n' ', ')
          EXISTING_CLI_NAMES="${EXISTING_CLI_NAMES}${BIN_NAMES}"
        fi ;;
      pyproject.toml:scripts)
        SCRIPTS_NAMES=$(sed -n '/^\[project\.scripts\]/,/^\[/p' "$REPO_PATH/pyproject.toml" 2>/dev/null | head -n -1 | tail -n +2 | sed 's/ *=.*//' | tr '\n' ', ')
        EXISTING_CLI_NAMES="${EXISTING_CLI_NAMES}${SCRIPTS_NAMES}"
        ;;
      setup.py:console_scripts)
        CMD_NAMES=$(grep -oP "'\K[^']+(?='\s*=>)" "$REPO_PATH/setup.py" 2>/dev/null | tr '\n' ', ')
        EXISTING_CLI_NAMES="${EXISTING_CLI_NAMES}${CMD_NAMES}"
        ;;
      Cargo.toml:bin)
        BIN_CRATES=$(sed -n '/^\[\[bin\]\]/,/^\[/p' "$REPO_PATH/Cargo.toml" 2>/dev/null | grep '^name' | sed 's/.*= *"\(.*\)"/\1/' | tr '\n' ', ')
        EXISTING_CLI_NAMES="${EXISTING_CLI_NAMES}${BIN_CRATES}"
        ;;
    esac
  done
  EXISTING_CLI_NAMES=$(echo "$EXISTING_CLI_NAMES" | sed 's/, *$//' | sed 's/^ *//')
fi

# --- Category detection ---
CLI_MATCH=0
LIB_MATCH=0
APP_MATCH=0
MONO_MATCH=0
PLUGIN_MATCH=0

for s in "${CAT_SIGNALS[@]}"; do
  case "$s" in
    package.json:bin|pyproject.toml:scripts|setup.py:console_scripts|Cargo.toml:bin|cmd/) CLI_MATCH=$((CLI_MATCH+1)) ;;
    Cargo.toml:lib) LIB_MATCH=$((LIB_MATCH+1)) ;;
    Dockerfile|docker-compose.yml|.env.example|Procfile|fly.toml|vercel.json) APP_MATCH=$((APP_MATCH+1)) ;;
    pnpm-workspace.yaml|lerna.json|turbo.json|go.work|package.json:workspaces|Cargo.toml:workspace) MONO_MATCH=$((MONO_MATCH+1)) ;;
    plugin.json|extension.json) PLUGIN_MATCH=$((PLUGIN_MATCH+1)) ;;
  esac
done

CATEGORY="unknown"
CONFIDENCE=0.0
CAT_ALTERNATIVES=()

pick_category() {
  local name="$1" score="$2"
  CATEGORY="$name"
  # cap confidence at 1.0: each signal adds 0.3, maxed at 1.0
  CONFIDENCE=$(awk "BEGIN { v = 0.3 * $score; if (v > 1.0) v = 1.0; print v }")
}

if [[ "$MONO_MATCH" -gt 0 ]]; then
  pick_category "monorepo" "$MONO_MATCH"
elif [[ "$CLI_MATCH" -gt 0 ]]; then
  pick_category "cli-tool" "$CLI_MATCH"
elif [[ "$APP_MATCH" -gt 0 ]]; then
  pick_category "application" "$APP_MATCH"
elif [[ "$PLUGIN_MATCH" -gt 0 ]]; then
  pick_category "plugin" "$PLUGIN_MATCH"
elif [[ "$LIB_MATCH" -gt 0 ]]; then
  pick_category "library" "$LIB_MATCH"
else
  # Fallback heuristic
  if $HAS_TESTS || [[ -n "$PRIMARY_LANG" && "$PRIMARY_LANG" != "Unknown" ]]; then
    CATEGORY="application"
    CONFIDENCE=0.3
  else
    CATEGORY="unknown"
    CONFIDENCE=0.1
  fi
fi

# --- Complexity ---
TOTAL_FILES=$(find "$REPO_PATH" -type f 2>/dev/null | wc -l)
if [[ "$TOTAL_FILES" -lt 20 ]]; then
  COMPLEXITY="simple"
elif [[ "$TOTAL_FILES" -lt 100 ]]; then
  COMPLEXITY="moderate"
else
  COMPLEXITY="complex"
fi

# --- Build scripts (from package.json) ---
BUILD_SCRIPTS="{"
if has_file "package.json" && command -v jq &>/dev/null; then
  SCRIPTS=$(jq -c '.scripts // {}' "$REPO_PATH/package.json" 2>/dev/null)
  BUILD_SCRIPTS="${SCRIPTS:-{}}"
else
  BUILD_SCRIPTS+="}"
fi

# --- Existing CLI output ---
HAS_CLI=${CLI_ENTRY_SIGNALS[@]:+:true}
HAS_CLI=${HAS_CLI:-false}

CLI_ENTRY_JSON="["
FIRST=true
for s in "${CLI_ENTRY_SIGNALS[@]}"; do
  $FIRST || CLI_ENTRY_JSON+=","
  FIRST=false
  CLI_ENTRY_JSON+="\"$s\""
done
CLI_ENTRY_JSON+="]"

# --- Assemble JSON ---
SIGNALS_JSON="["
FIRST=true
for s in "${CAT_SIGNALS[@]}"; do
  $FIRST || SIGNALS_JSON+=","
  FIRST=false
  SIGNALS_JSON+="\"$s\""
done
SIGNALS_JSON+="]"

FRAMEWORKS_JSON="["
FIRST=true
for f in "${FRAMEWORKS[@]}"; do
  $FIRST || FRAMEWORKS_JSON+=","
  FIRST=false
  FRAMEWORKS_JSON+="\"$f\""
done
FRAMEWORKS_JSON+="]"

# Escape strings for JSON
escape_json() { echo "$1" | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g'; }
DESC_ESC=$(escape_json "$DESCRIPTION")
LICENSE_ESC=$(escape_json "${LICENSE:-null}")
BUILD_SYSTEM_ESC=$(escape_json "${BUILD_SYSTEM:-null}")

OUTPUT=$(cat <<JSON
{
  "metadata": {
    "name": "$REPO_NAME",
    "fullPath": "$REPO_PATH",
    "isGitRepo": $GIT_REPO,
    "remoteUrl": $REMOTE_URL,
    "defaultBranch": $DEFAULT_BRANCH,
    "description": "$DESC_ESC",
    "license": $LICENSE_ESC
  },
  "structure": {
    "topLevelDirs": "${TOP_DIRS:-}",
    "topLevelFiles": "${TOP_FILES:-}",
    "hasSrc": $HAS_SRC,
    "hasLib": $HAS_LIB,
    "hasDocs": $HAS_DOCS,
    "hasExamples": $HAS_EXAMPLES,
    "hasTests": $HAS_TESTS,
    "hasGithubDir": $HAS_CI,
    "hasDocker": $HAS_DOCKER
  },
  "languages": {
    "detected": $LANG_DETECTED,
    "primary": "$PRIMARY_LANG",
    "frameworks": $FRAMEWORKS_JSON
  },
  "category": {
    "primary": "$CATEGORY",
    "confidence": $CONFIDENCE,
    "alternatives": [],
    "signals": $SIGNALS_JSON
  },
  "build": {
    "system": "$BUILD_SYSTEM_ESC",
    "testFramework": null,
    "packageManager": null,
    "scripts": $BUILD_SCRIPTS
  },
  "existingCli": {
    "hasCli": $HAS_CLI,
    "entryPoints": $CLI_ENTRY_JSON,
    "names": "$EXISTING_CLI_NAMES"
  },
  "complexity": "$COMPLEXITY"
}
JSON
)

if [[ -n "$OUTPUT_FILE" ]]; then
  echo "$OUTPUT" > "$OUTPUT_FILE"
  echo "Profile written to $OUTPUT_FILE" >&2
else
  echo "$OUTPUT"
fi
