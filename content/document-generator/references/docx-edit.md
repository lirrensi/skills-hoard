# DOCX Editing

## Workflow (3 Steps)

### Step 1: Unpack
```bash
python scripts/office/unpack.py document.docx unpacked/
```

### Step 2: Edit XML
Edit files in `unpacked/word/` directly.

**Use Edit tool** — not Python scripts. Shows exactly what's being replaced.

#### Smart Quotes (Required)
Use XML entities for apostrophes/quotes:
```xml
<w:t>Here&#x2019;s a quote: &#x201C;Hello&#x201D;</w:t>
```

| Entity | Character |
|--------|-----------|
| `&#x2018;` | ' (left single) |
| `&#x2019;` | ' (right single) |
| `&#x201C;` | " (left double) |
| `&#x201D;` | " (right double) |

#### Tracked Changes
```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>inserted text</w:t></w:r>
</w:ins>

<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
```

**Inside `<w:del>`**: Use `<w:delText>` instead of `<w:t>`.

#### Comments
```bash
python scripts/comment.py unpacked/ 0 "Comment text"
```
Then add markers in document.xml:
```xml
<w:commentRangeStart w:id="0"/>
<w:r><w:t>commented text</w:t></w:r>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>
```

### Step 3: Pack
```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```

## XML Schema Rules

- **Order in `<w:pPr>`**: `<w:pStyle>`, `<w:numPr>`, `<w:spacing>`, `<w:ind>`, `<w:jc>`, `<w:rPr>` last
- **Whitespace**: Add `xml:space="preserve"` to `<w:t>` with spaces
- **RSIDs**: Must be 8-digit hex

## Common Pitfalls

1. Replace entire `<w:r>` elements, not just text inside
2. Preserve `<w:rPr>` when modifying runs
3. When deleting paragraphs with lists, also delete the `<w:numPr>` or empty paragraphs remain
