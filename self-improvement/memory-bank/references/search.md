# Searching Memories (full)

> Companion to `SKILL.md` → Scripts (`get_mem.py`). Load this when `get_mem.py` isn't enough and you need surgical `rg` recipes. Bodies stay lazy: summary tells you if it's worth reading; reading gives you the actual context.

## Quick orientation (run this first when memories feel relevant)

```bash
rg --files ./memory | sort
```

This shows the files that exist across all memory types — a fast orientation to what's here.

## Read the index

```bash
cat ./memory/INDEX.md
```

## Search by memory type

```bash
rg "^memory_type: episodic$" ./memory/ --no-ignore
rg "^memory_type: semantic$" ./memory/ --no-ignore
rg "^memory_type: procedural$" ./memory/ --no-ignore
```

## Read summaries across all files

```bash
rg "^summary:" ./memory/ --no-ignore
```

## Search by keyword (full text)

```bash
rg "keyword" ./memory/ --no-ignore -i
```

## Search summaries only

```bash
rg "^summary:.*keyword" ./memory/ --no-ignore -i
```

## Search by tag

```bash
rg "^tags:.*keyword" ./memory/ --no-ignore -i
```

## Search by tag combination

```bash
rg "^tags:.*auth.*project-helios|^tags:.*project-helios.*auth" ./memory/ --no-ignore -i
```

## Search semantic memories for current state

```bash
rg "keyword" ./memory/semantic/ --no-ignore -i
```

## Search procedural memories for how-to guidance

```bash
rg "keyword" ./memory/procedural/ --no-ignore -i
```

## Search episodic memories for what happened

```bash
rg "keyword" ./memory/episodic/ --no-ignore -i
```

## Search archived episodic memories (deep dive)

```bash
rg "keyword" ./memory/archive/ --no-ignore -i
```

## Search weekly/monthly summaries (overview)

```bash
rg "keyword" ./memory/summaries/ --no-ignore -i
```

## Search everything at once (nuclear option)

```bash
rg "keyword" ./memory/ --no-ignore -i
```

## Related links

Use relative paths from `./memory/` root in `related:` fields. Filenames are unique across the whole memory space, so a simple filename is enough:

```yaml
related: [semantic/auth_constraints.md, episodic/2026_05_14_auth_bug.md]
```
