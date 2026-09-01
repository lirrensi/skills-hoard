# Long Reads (Article-to-Audio)

Load this guide when the user wants to convert an article, document, report, or any long-form text into narrated audio — single voice, end to end.

**Prerequisite:** Read `long-read-principles.md` first for the editorial rules on making text ear-navigable. This file handles the technical pipeline; that file handles the rewriting.

## Workflow Overview

1. Extract text from the source (file, URL, or pasted content)
2. Clean the text for narration
3. Choose narration voice and pace
4. Chunk the text for TTS generation
5. Generate audio per chunk
6. Concatenate and post-process

## Step 1: Extract Text

### By source type

| Source | Tool | Command |
|--------|------|---------|
| Plain text / Markdown | Direct | Use as-is |
| PDF | `markitdown` | `python -m markitdown file.pdf > extracted.txt` |
| DOCX | `markitdown` | `python -m markitdown file.docx > extracted.txt` |
| HTML / webpage | `webfetch` or `BeautifulSoup` | Fetch and extract `<article>` or main content |
| URL | `webfetch` | Fetch as markdown, then clean |

### Extraction tips

- Prefer `markitdown` for documents — it handles structure well
- For web articles, extract only the article body, skip nav/ads/comments
- Preserve heading structure — it helps with chunking later

## Step 2: Clean for Narration

Raw text from documents doesn't sound good spoken. Clean it up.

**For the editorial principles** (why and how to restructure text for ears), see `long-read-principles.md`. Below are the mechanical fixes.

### What to fix

| Raw text | Narration-ready |
|----------|-----------------|
| `$5M` | `five million dollars` |
| `e.g.,` | `for example` |
| `i.e.,` | `that is` |
| `etc.` | `et cetera` |
| `Dr. Smith` | `Doctor Smith` |
| `COVID-19` | `COVID nineteen` |
| `2024-01-15` | `January fifteenth, twenty twenty-four` |
| `[1]`, `[Smith et al.]` | Remove entirely |
| `Figure 3 shows...` | `As shown in the data...` |
| `https://example.com/long-url` | Remove or say "link in the description" |
| `@username` | Remove or spell out |
| Bullet lists | Convert to flowing sentences |

### Cleaning helper (Python)

```python
import re

def clean_for_narration(text):
    # Remove citation brackets
    text = re.sub(r'\[[\d,\s]+\]', '', text)
    text = re.sub(r'\[[A-Z][a-z]+.*?\d{4}\]', '', text)  # [Smith et al. 2024]
    
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    
    # Remove figure/table references
    text = re.sub(r'(Figure|Table|Fig\.)\s*\d+', '', text)
    
    # Expand common abbreviations
    replacements = {
        'e.g.': 'for example',
        'i.e.': 'that is',
        'etc.': 'et cetera',
        'vs.': 'versus',
        'Dr.': 'Doctor',
        'Mr.': 'Mister',
        'Ms.': 'Miss',
        'Prof.': 'Professor',
    }
    for abbr, full in replacements.items():
        text = text.replace(abbr, full)
    
    # Clean up extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'  +', ' ', text)
    
    return text.strip()
```

## Step 3: Choose Narration Style

### Single narrator (default)

One voice, steady pace, slightly slower than conversational.

| Content type | Rate adjustment | Style needed |
|-------------|-----------------|--------------|
| News / analysis | Slightly slower | Clear, authoritative |
| Feature article | Slower | Warm, natural |
| Academic / technical | Slower | Measured, precise |
| Literary / narrative | Slower | Elegant, expressive |
| Casual blog post | Normal | Conversational, friendly |

Map these styles to your backend's voices. See `voices.md` for guidance, then check the backend file for specific voice codes.

### Dual narrator (optional)

Alternate voices by section for variety — useful for very long content (>30 min).

- Use heading boundaries as switch points
- Male voice for odd sections, female for even (or vice versa)
- Announce the switch: no need, the voice change is the signal

## Step 4: Chunk the Text

Split into chunks that your TTS backend can handle. Rules:

- **Max chunk size**: ~4,000–5,000 characters (varies by backend — check backend docs)
- **Split at**: paragraph boundaries, heading boundaries
- **Never split**: mid-sentence, mid-paragraph, mid-quote
- **Label chunks**: `chunk_001.txt`, `chunk_002.txt`, etc.

### Chunking helper (Python)

```python
def chunk_text(text, max_chars=4500):
    """Split text into chunks at paragraph boundaries."""
    paragraphs = text.split('\n\n')
    chunks = []
    current = ''
    
    for para in paragraphs:
        if len(current) + len(para) + 2 > max_chars and current:
            chunks.append(current.strip())
            current = para + '\n\n'
        else:
            current += para + '\n\n'
    
    if current.strip():
        chunks.append(current.strip())
    
    return chunks

# Usage
text = open('cleaned_article.txt').read()
chunks = chunk_text(text)
for i, chunk in enumerate(chunks, 1):
    open(f'chunk_{i:03d}.txt', 'w').write(chunk)
print(f"Split into {len(chunks)} chunks")
```

## Step 5: Generate Audio

Generate each chunk with your chosen backend. See the backend file for its specific command:

- **edge-tts**: `edge-tts --file chunk_001.txt --voice en-US-AriaNeural --rate="-10%" --write-media chunk_001.mp3`
- **Kokoro**: Python API — see `backends/kokoro.md`
- **Pocket TTS**: Python API — see `backends/pocket-tts.md`
- **MeloTTS**: Python API — see `backends/melotts.md`
- **Piper**: `cat chunk_001.txt | piper --model en_US-lessac-medium --length_scale 1.1 --output_file chunk_001.wav`

The concatenation and post-processing steps below are the same regardless of backend.

## Step 6: Concatenate and Post-Process

### Generate pause files

```bash
# Brief pause between chunks (0.8s) — natural paragraph break
ffmpeg -f lavfi -i anullsrc=r=24000:cl=mono -t 0.8 -q:a 9 pause.mp3

# Section separator (short tone) — for major heading breaks
ffmpeg -f lavfi -i sine=frequency=800:duration=0.3 \
  -af "afade=t=in:d=0.05,afade=t=out:d=0.2" separator.mp3
```

### Build file list and concatenate

```bash
# Simple: just chunks with pauses
echo "file 'chunk_001.mp3'" > filelist.txt
for f in chunk_0{02..99}.mp3 chunk_0{100..999}.mp3; do
  [ -f "$f" ] || continue
  echo "file 'pause.mp3'" >> filelist.txt
  echo "file '$f'" >> filelist.txt
done

# Concatenate
ffmpeg -f concat -safe 0 -i filelist.txt -c copy narration_raw.mp3
```

### Post-processing

```bash
# Normalize loudness
ffmpeg -i narration_raw.mp3 -af loudnorm narration_normalized.mp3

# Add fade in/out (2 second fades)
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 narration_normalized.mp3)
FADE_OUT_START=$(echo "$DURATION - 2" | bc)
ffmpeg -i narration_normalized.mp3 \
  -af "afade=t=in:st=0:d=2,afade=t=out:st=$FADE_OUT_START:d=2" \
  narration_final.mp3
```

### For very long content (>10,000 words)

Add a spoken intro listing the sections. Generate the TOC intro with your backend, then insert at the beginning of the filelist.

## Quality Checks

- [ ] No mid-sentence breaks (chunking split correctly)
- [ ] Abbreviations are expanded (no "e.g." spoken as "e dot g dot")
- [ ] Numbers sound natural (not "one thousand nine hundred and eighty-four")
- [ ] Consistent volume throughout
- [ ] Pauses feel natural at paragraph breaks

```bash
# Check total duration
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 narration_final.mp3

# Check for volume spikes
ffmpeg -i narration_final.mp3 -af volumedetect -f null /dev/null 2>&1 | grep max_volume
```

## Common Patterns

### Academic paper narration
Clean aggressively — remove citations, figure references, equation numbering. Use `-15%` rate. Consider adding "Section:" before each heading.

### News article narration
Light cleaning. Use `-5%` rate. Keep the journalistic tone — don't add commentary.

### Blog post narration
Minimal cleaning. Use `+0%` rate. The conversational tone of blogs translates well to TTS.

### Report / whitepaper narration
Heavy cleaning needed. Add section intros. Use `-10%` rate. Consider dual narrator for variety over long duration.
