# CLI Tool Extraction Patterns

Patterns for extracting command-line interface structures from different language
ecosystems and frameworks. Used in Phase 3A of the git-to-skill pipeline.

---

## Detection by Framework

### Node.js / TypeScript (commander, yargs, oclif, meow)

**Look for:**
- `package.json` `bin` field → the entry point
- `program.command(...)`, `yargs.command(...)`, `oclif` commands directory
- `--help` output patterns in tests or README

**Extraction commands:**
```bash
# If the tool can be run without building:
npx <package> --help
npx <package> <command> --help

# From source:
node bin/cli.js --help
```

**Parsing strategy:**
- For `commander`: parse `.command()`, `.option()`, `.argument()` chains
- For `yargs`: parse `.command()`, `.option()`, `.positional()` chains
- For `oclif`: read the commands directory structure
- For raw `process.argv`: extract from `--help` output

### Python (argparse, click, typer, rich)

**Look for:**
- `pyproject.toml` `[project.scripts]` section → the entry point
- `setup.py` / `setup.cfg` `console_scripts` entry point
- `@click.command()`, `@click.option()`, `@app.command()` decorators
- `argparse.ArgumentParser()` instances
- `typer.Typer()` app creation

**Extraction commands:**
```bash
# If installed:
<command> --help

# From source with uv:
uv run <module> --help

# From source with pip:
python -m <module> --help
```

**Parsing strategy:**
- For `click`: extract decorators: `@click.option('--name', help='...')`
- For `typer`: extract function signatures (params become CLI args)
- For `argparse`: read `.add_argument()` and `.add_subparsers()` calls
- Fallback: run `--help` and `--help-commands` and parse the output

### Rust (clap, structopt)

**Look for:**
- `Cargo.toml` `[[bin]]` section
- `#[derive(Parser)]`, `#[derive(Args)]`, `#[command()]` attributes
- `Command::new()`, `App::new()` in clap v3 patterns
- `src/cli.rs`, `src/args.rs`, `src/opts.rs`

**Extraction commands:**
```bash
cargo run -- --help
cargo build && ./target/debug/<name> --help
```

**Parsing strategy:**
- For `clap` derive: parse `#[arg()]` attributes for short/long flags, help text
- For `clap` builder: parse `.arg()`, `.subcommand()` chains
- Read `--help` output as fallback

### Go (cobra, urfave/cli)

**Look for:**
- `cmd/` directory with `main.go` per command
- `cobra.Command{}` struct literals
- `app.Commands[]`, `app.Flags` in urfave/cli
- `rootCmd.AddCommand()` calls

**Extraction commands:**
```bash
go run . --help
go build -o /dev/null . && ./<name> --help
```

**Parsing strategy:**
- For `cobra`: extract `Use:`, `Short:`, `Long:` fields from command structs
- For `urfave/cli`: extract `Name:`, `Usage:`, `Flags:` from app/command structs
- Walk the command tree via `AddCommand()` calls

---

## Universal CLI Structure

Regardless of framework, every CLI tool can be decomposed into:

```
<command> [global flags] <subcommand> [subcommand flags] [arguments]
```

Extract and document these for each command:

| Field          | Description                                      | Source                     |
| -------------- | ------------------------------------------------ | -------------------------- |
| Name           | The command name (e.g., `build`, `deploy`)       | Framework definition       |
| Usage          | Usage line (e.g., `build [options] <path>`)      | Framework definition / URL |
| Description    | Short description of the command                 | Framework help text        |
| Arguments      | Positional arguments with types                  | Framework definition       |
| Flags/Options  | Named flags (--flag, -f) with types and defaults | Framework definition       |
| Subcommands    | Child commands if any                            | Framework command tree     |
| Examples       | Usage examples from docs or help text            | README / help output       |
| Env Vars       | Environment variables that affect the command    | Docs / source search       |
| Exit Codes     | Non-zero exit code meanings                      | Docs / source              |

---

## Generating the CLI Reference

For each command in the tree, produce a structured markdown section:

```markdown
## `command subcommand`

**Usage:** `tool subcommand [options] <required-arg> [optional-arg]`

**Description:** Brief description of what this command does.

**Arguments:**
| Name     | Required | Type   | Description            |
| -------- | -------- | ------ | ---------------------- |
| `<path>` | yes      | string | Path to the target     |
| `[name]` | no       | string | Optional output name   |

**Flags:**
| Flag              | Type    | Default | Description                  |
| ----------------- | ------- | ------- | ---------------------------- |
| `--output, -o`    | string  | `./out` | Output directory             |
| `--verbose, -v`   | boolean | `false` | Enable verbose logging       |
| `--config, -c`    | string  | —       | Path to config file          |

**Environment Variables:**
| Variable          | Description                            |
| ----------------- | -------------------------------------- |
| `TOOL_HOME`       | Data directory (default: `~/.tool`)    |
| `TOOL_DEBUG`      | Enable debug output (`1` or `true`)    |

**Examples:**
```bash
# Basic usage
tool build <path>

# With options
tool build <path> --output ./dist --verbose

# Using config
tool build --config ./my-config.yaml
```
```

If the CLI has a deep command tree (3+ levels), generate a navigation index:

```markdown
## Command Tree

- `tool`
  - `tool init` — Initialize a new project
  - `tool build` — Build the project
    - `tool build full` — Full production build
    - `tool build quick` — Quick development build
  - `tool deploy` — Deploy the project
    - `tool deploy staging` — Deploy to staging
    - `tool deploy prod` — Deploy to production
  - `tool config` — Manage configuration
    - `tool config set` — Set a config value
    - `tool config get` — Get a config value
```

---

## Shell Completions

If the project does NOT ship shell completions and the user asked for scripts,
generate completion stubs:

### Bash
```bash
_tool_completions() {
  local cur prev words cword
  _init_completion || return
  COMPREPLY=($(compgen -W "$(tool __complete --bash "${words[@]:1}" 2>/dev/null)" -- "$cur"))
}
complete -F _tool_completions tool
```

### Zsh
```zsh
#compdef tool
_tool() {
  local -a commands
  commands=(
    'init:Initialize a new project'
    'build:Build the project'
    'deploy:Deploy the project'
    'config:Manage configuration'
  )
  _describe 'command' commands
}
compdef _tool tool
```

### Fish
```fish
complete -c tool -f -a init -d "Initialize a new project"
complete -c tool -f -a build -d "Build the project"
complete -c tool -f -a deploy -d "Deploy the project"
complete -c tool -f -a config -d "Manage configuration"
```

Derive the completions from the extracted command tree. Save to
`scripts/completions/bash.sh`, `scripts/completions/zsh.sh`, `scripts/completions/fish.fish`.

---

## Common Pitfalls

| Pitfall                               | Detection                                     | Fix                                              |
| -------------------------------------- | --------------------------------------------- | ------------------------------------------------ |
| Confusing build steps with CLI usage   | Skill focuses on `npm install` not `tool run` | Shift focus to the CLI commands, not setup      |
| Missing subcommand depth              | Only top-level commands documented            | Walk the full command tree with --help recursion |
| Stale --help output                   | Flags mismatch with source code               | Prefer source-code parsing over runtime --help   |
| Platform-specific paths               | Scripts use `~/` or `/usr/local` hard-coded   | Use `$HOME`, document platform assumptions       |
| Ignoring config file formats          | No mention of YAML/JSON/TOML config           | Check for `--config` flag and document format    |
| Missing environment variables         | Skill doesn't mention ENV overrides           | Grep source for `process.env`, `os.getenv`, `std::env` |
