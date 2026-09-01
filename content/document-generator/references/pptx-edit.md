# PPTX Editing (Template-Based)

## Workflow

### 1. Analyze Template
```bash
python scripts/thumbnail.py template.pptx
python -m markitdown template.pptx
```

### 2. Unpack
```bash
python scripts/office/unpack.py template.pptx unpacked/
```

### 3. Structural Changes (before content)
- Delete slides: Remove from `<p:sldIdLst>`
- Reorder: Rearrange `<p:sldId>` elements
- Duplicate: Use `python scripts/add_slide.py unpacked/ slide2.xml`

### 4. Edit Content
Edit `ppt/slides/slide{N}.xml` files directly.

**Use Edit tool** — not sed/scripts.

### 5. Clean
```bash
python scripts/clean.py unpacked/
```

### 6. Pack
```bash
python scripts/office/pack.py unpacked/ output.pptx --original template.pptx
```

## Content Editing Rules

- **Bold headers**: Add `b="1"` to `<a:rPr>`
- **Never unicode bullets**: Use `<a:buChar>` or inherit from layout
- **Multi-item content**: Separate `<a:p>` elements, don't concatenate
- **Smart quotes**: Use XML entities
  ```xml
  <a:t>Quote: &#x201C;text&#x201D;</a:t>
  ```

## Layout Variety

⚠️ **Don't repeat same layout** — use varied layouts:
- Multi-column
- Image + text
- Full-bleed with overlay
- Quote/callout
- Stat callouts
- Icon grids

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `unpack.py` | Extract and pretty-print |
| `add_slide.py` | Duplicate slide or create from layout |
| `clean.py` | Remove orphaned files |
| `pack.py` | Repack with validation |
| `thumbnail.py` | Create visual grid |
