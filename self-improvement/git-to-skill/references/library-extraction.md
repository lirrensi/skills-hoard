# Library Extraction Patterns

Patterns for extracting API surfaces, integration points, and usage patterns from
library-style repositories. Used in Phase 3B of the git-to-skill pipeline.

---

## Detection by Ecosystem

### Node.js / TypeScript Libraries

**Entry point detection:**
```bash
# Check package.json for main/exports
cat package.json | Select-String -Pattern '"main"|"exports"|"module"|"types"'

# Common entry points:
# - index.js, index.ts, index.mjs
# - src/index.ts, lib/index.js
# - dist/index.js (compiled output)
```

**API surface extraction:**
- Read the main entry point file
- For TypeScript: read `.d.ts` types or source `.ts` files for exported types
- Extract all `export` statements (named + default)
- Document each exported symbol with its signature

**Framework-specific detection:**
| Signal                     | Framework      |
| -------------------------- | -------------- |
| `@nestjs/` imports         | NestJS         |
| `express.Router()`         | Express        |
| `React.FC`, `JSX.Element`  | React          |
| `Vue.extend()`, `defineComponent` | Vue    |
| `SvelteComponent`          | Svelte         |
| `createStore`, `createSlice` | Redux / Zustand |

### Python Libraries

**Entry point detection:**
```bash
# Find the package directory (matches repo name)
Get-ChildItem -Path . -Filter "__init__.py" -Recurse -Depth 2

# Check pyproject.toml for [project.entry-points]
# Check setup.py for entry_points
```

**API surface extraction:**
- Read `__init__.py` — check `__all__` and imports
- Read public modules (no leading underscore)
- Extract function signatures, class definitions, decorators
- Document parameters with their type annotations and defaults

**Framework-specific detection:**
| Signal                          | Framework        |
| ------------------------------- | ---------------- |
| `@app.route()`, `Flask`         | Flask            |
| `FastAPI()`, `@app.get()`       | FastAPI          |
| `click.Group()`, `@click.command()` | Click (treat as CLI? flag in Phase 2) |
| `pytest.fixture`, `@pytest`     | Pytest (plugin)  |
| `jupyter-` prefix               | Jupyter          |
| `django.apps.AppConfig`         | Django           |

### Rust Libraries

**Entry point detection:**
```bash
# Check Cargo.toml for [lib] section
Select-String -Path "Cargo.toml" -Pattern '\[lib\]'

# lib.rs is the crate root
Test-Path "src/lib.rs"
```

**API surface extraction:**
- Read `src/lib.rs` for `pub fn`, `pub struct`, `pub trait`, `pub enum`, `pub mod`
- Walk `pub mod` declarations into their files
- Document generics, trait bounds, lifetime parameters
- Extract `#[derive()]`, `#[must_use]`, `#[deprecated]` annotations

### Go Libraries

**Entry point detection:**
```bash
# The module root is the entry point
Select-String -Path "go.mod" -Pattern '^module '
```

**API surface extraction:**
- Read top-level `.go` files (except `*_test.go`)
- Extract exported identifiers (capitalized): `func`, `type`, `struct`, `interface`, `const`, `var`
- Document function signatures with parameter names and return types
- Extract interface definitions (the set of expected methods)
- Note: in Go, the `main` package is not a library

---

## Universal API Structure

Every library can be decomposed into these categories:

```yaml
api_surface:
  classes:
    - name
    - constructor parameters
    - methods (name, params, return)
    - properties
  functions:
    - name
    - parameters (name, type, default, required)
    - return type
    - description
  types/interfaces:
    - name
    - fields/properties
    - methods (if interface type)
  constants:
    - name
    - value
    - description
  exports:
    - name
    - kind (class, fn, type, const)
    - public API? (yes/no)
```

---

## Generating the API Reference

Format each major API component:

### Functions

```markdown
### `functionName(param1: Type, param2?: Type): ReturnType`

Description of what this function does.

**Parameters:**
| Name    | Type     | Required | Default     | Description             |
| ------- | -------- | -------- | ----------- | ----------------------- |
| param1  | `string` | yes      | —           | Description of param1   |
| param2  | `number` | no       | `42`        | Description of param2   |

**Returns:** Description of the return value.

**Example:**
```typescript
import { functionName } from 'package-name'
const result = functionName('hello', 42)
```
```

### Classes

```markdown
### `ClassName`

Description of the class.

**Constructor:**
| Parameter | Type     | Required | Default | Description |
| --------- | -------- | -------- | ------- | ----------- |
| options   | `Config` | yes      | —       | Config obj  |

**Methods:**
| Method                      | Returns      | Description              |
| --------------------------- | ------------ | ------------------------ |
| `methodA(param: string)`    | `Result`     | Does something           |
| `methodB()`                 | `Promise<>`  | Async operation          |

**Example:**
```typescript
const instance = new ClassName({ key: 'value' })
await instance.methodB()
```
```

### Integration Patterns

Document 3-5 canonical ways the library is used:

```markdown
## Common Patterns

### Pattern 1: Basic Usage

```python
from package import Client

client = Client(api_key="...")
result = client.query("data")
print(result)
```

### Pattern 2: With Middleware

```python
from package import Client, LoggingMiddleware

client = Client(api_key="...")
client.use(LoggingMiddleware())
result = client.query("data")
```
```

Extract these patterns from:
- README examples (usually the first code block)
- `examples/` directory
- Test files (the most reliable source of real usage)
- Documentation / tutorials

---

## Quick Reference Card

For the generated skill's main SKILL.md, produce a condensed quick reference:

```markdown
## Quick Reference

### Install
```bash
pip install <package>
# or
pnpm add <package>
```

### Import
```python
from package import Client
```

### Initialize
```python
client = Client(timeout=30)
```

### Common Operations
| Operation          | Code                              |
| ------------------ | --------------------------------- |
| Basic query        | `client.query("...")`            |
| With filters       | `client.query("...", filters={})` |
| Async query        | `await client.aquery("...")`     |
```

---

## Common Pitfalls

| Pitfall                            | Detection                                    | Fix                                          |
| ---------------------------------- | -------------------------------------------- | -------------------------------------------- |
| Extracting internal/private API    | `_prefixed` or non-exported symbols included | Only include `__all__`, `pub`, `export`-ed   |
| Missing async variants             | Only sync methods documented                 | Check for `async`/`await`/`Promise` variants |
| Over-documenting trivial helpers   | Internal utility functions in reference      | Focus on user-facing API only                |
| No example preservation            | Reference has signatures but no examples     | Always include at least one example per API  |
| Ignoring type generics             | `List[str]` becomes `list`                   | Preserve full type signatures with generics  |
| Framework-specific patterns lost   | Express middleware treated as regular func   | Identify and label framework patterns        |
