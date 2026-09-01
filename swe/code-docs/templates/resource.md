---
node_type: resource
title: {Resource Name}
status: active
updated: YYYY-MM-DD
tags: []
resource: {path, URL, or identifier}
links:
  relates_to: []
---

# {Resource Name}

## What
{1-3 sentences: what is this thing? Describe it for someone who has never seen it.}

## Boundaries
**Handles:** {X, Y — what this resource is for}
**Explicitly does NOT:** {Z, W — the negative space. What this resource rejects or does not cover.}
**If it happens anyway:** {where Z/W goes instead — "[Other System]", "not supported", "handled by the team", etc.}

## Where
{Where is it? Use whatever makes the most sense — relative path, absolute path, URL, package identifier, or a narrative location.}

Examples of what `Where` can look like:

- **Relative path (inside project):** `./downloads/acme-docs-v2.3.zip` — file lives in the project repo or adjacent directory.
- **Absolute local path:** `C:\Users\rx\Documents\design-handbook.pdf` or `/home/rx/docs/process-manual.pdf` — file lives somewhere on the local system outside the repo.
- **URL:** `https://acme.example.com/docs/v2.3` — live online resource.
- **Package/tool reference:** `npm:acme-library` or `pip:acme-utils` — installed dependency whose docs or source are useful.
- **Narrative:** "On the shared drive at `\\company\teams\design\brand-guide.pdf`" or "Slack channel #design-system, pinned messages" — when there is no clean machine-readable location.

## Why
{Why does this matter for this project? What do we use it for? Under what circumstances would someone go looking for it?}

## How to Use
{How to access, open, or consume it. Be concrete — command lines, URLs, steps.}

## Metadata

| Field | Value |
|-------|-------|
| **Source** | {Where it originally came from — download URL, vendor, department} |
| **Format** | {File format or medium — PDF, ZIP, CSV, Slack channel, printed binder} |
| **Size** | {Rough size — file size, page count, etc.} |
| **Date Acquired** | {When we got it} |
| **Version** | {Version number, edition, or date of publication} |
| **License** | {Usage restrictions, if any} |
| **Expires** | {If it has a shelf life — e.g., "NDA expires 2027-03" or "Valid until next vendor refresh"} |

## Notes
{Anything else worth knowing — quirks, known issues, gotchas, related resources, who to ask if it's missing.}

---

## Roster
**REQUIRED:** add this resource to `docs/ROSTER.md` in the same change (see `../refs/roster.md`):

```markdown
- [{Resource Name}](/resources/{file-name}.md) — {one-line what/why} [🟢 active]
```

Validate with `python scripts/check-roster.py` — a resource doc with no roster entry is a lint failure.
