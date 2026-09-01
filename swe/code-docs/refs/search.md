# How to Search Documentation

The documentation is a **graph**, not a flat pile. You find things by walking the graph — starting at INDEX.md nodes, following links to leaves, using tags as signposts.

---

## The Graph-Walking Method

This is the primary, intended way to find anything:

### Step 1: Start at the root
Read `docs/INDEX.md`. It tells you what each top-level folder contains.

If `docs/ROSTER.md` exists, read it **before or alongside** the root index. The roster is the curated map of what the project has and why it matters — one scan and you know the whole world. Then INDEX.md tells you where the detail lives.

For any question about whether the system works, its test tooling, or release confidence, open `docs/verification/strategy.md` immediately after the root index. Treat it as the map from documented intent to executable checks and evidence.

### Step 2: Drill into the relevant folder INDEX.md
Each folder's INDEX.md lists every document and subfolder with one-line summaries. Start with the root folder registry to understand the complete directory structure and generated file totals, then read the relevant summaries — don't open files at random.

### Step 3: Follow links to leaves
When you find a promising document, open it. Check its frontmatter `links:` — `depends_on` tells you what to read first for context. `documents` tells you what code it describes.

### Step 4: Walk sideways via tags
If you need related docs in other folders, check the tags section of the INDEX.md. Tags are cross-cutting — `auth` might appear in `spec/`, `architecture/`, and `guides/`.

### Step 5: Navigate up via `part_of`
If a document feels too narrow, check if it has `links: part_of` pointing to a parent index or overview doc.

```
INDEX.md (map)
  └─ summary: "Authentication — login, sessions, 2FA [auth, security]"
       └─ open file
            └─ links.depends_on: [/overview/product.md]
            └─ links.documents: [/src/auth/]
            └─ body links: "See [Session Management](sessions.md)"
```

---

## Tag-Based Search

Tags are the fastest cross-cutting search. Every document declares tags in frontmatter:

```yaml
tags: [auth, security, api, sessions]
```

### Finding by tag from INDEX.md
Every INDEX.md has a tags section at the bottom. Scan it to find which documents share a tag:
```
## Tags
`auth` `security` `api` `sessions` `rate-limiting`
```
If you see the tag you want, the documents above tagged with it are your targets.

### Finding by tag via ripgrep
```bash
# Find all docs with a specific tag
rg "^tags:.*auth" docs/ --no-ignore

# Find docs with multiple tags (AND)
rg "^tags:.*auth.*api|^tags:.*api.*auth" docs/ --no-ignore
```

---

## Full-Text Search (when graph-walking isn't enough)

When you need to find something by keyword across ALL docs:

### Search frontmatter (titles, summaries)
```bash
# All document titles
rg "^title:" docs/ --no-ignore

# Titles containing a keyword
rg "^title:.*auth" docs/ --no-ignore -i
```

### Search body text
```bash
# Search all docs for a keyword
rg "session timeout" docs/ --no-ignore -i

# Search only spec files
rg "MUST" docs/spec/ --no-ignore

# Search only architecture files
rg "component" docs/architecture/ --no-ignore
```

### Search by node_type
```bash
# All specs
rg "^node_type: spec$" docs/ --no-ignore

# All ADRs
rg "^node_type: adr$" docs/ --no-ignore

# All active docs
rg "^status: active$" docs/ --no-ignore
```

### Query from doc to code and back (map.py)

The graph has two directions, and `map.py` can walk both:

```bash
# doc → code: what does this doc point at?
python scripts/map.py docs/spec/features/auth.md

# code → doc: which docs touch this code? (reverse lookup)
python scripts/map.py --code src/auth/index.ts
python scripts/map.py --code /src/billing/calc.ts        # leading-/ form works too

# taxonomy slice: everything tagged one way
python scripts/map.py --tag payments
```

`--code` matches both `links:` typed targets (`documents`, `implemented_by`, …) and the `resource:` frontmatter field — so a resource doc pointing at a dashboard or service is found from the code side too.

---

## When to Use Each Method

| Method | Best for | When |
|--------|---------|------|
| **INDEX.md graph-walking** | Finding where something lives, exploring structure | Always start here. Read INDEX.md before opening files. |
| **Tag scanning** | Cross-cutting topics that span multiple folders | When you need everything about "auth" or "security" |
| **Frontmatter search** | Finding docs by type, status, or title | When you know the doc type but not the exact file |
| **Full-text ripgrep** | Finding a specific term or phrase across all docs | Last resort — when graph-walking didn't find it |

---

## The Golden Rule

**Read INDEX.md before opening individual files.** The index is the map. It tells you what exists, where it is, and what it's about — all without opening a single document. Treat opening a file without checking its INDEX.md first as a navigation failure.
