---
name: document-extractor
description: >
  Convert hard-to-read files into clear Markdown with MarkItDown. Use for PDF, Word,
  PowerPoint, Excel, images, audio, HTML, CSV, JSON, XML, ZIP, EPUB, Outlook, and
  YouTube inputs. Check whether `markitdown` is installed first, prefer `uv tool install`,
  fall back to `pipx`, and use the upstream docs when needed.
---

# DocumentExtractor

Use `markitdown` to convert supported inputs into Markdown that is easier to inspect, search, and feed into LLM workflows.

## Check And Install

Check whether the CLI already exists:

```powershell
Get-Command markitdown -ErrorAction SilentlyContinue
markitdown --version
```

Install with `uv` first:

```powershell
uv tool install markitdown
uv tool install 'markitdown[pdf,docx,pptx]'
uv tool install 'markitdown[all]'
```

Fall back to `pipx` if `uv` is unavailable:

```powershell
pipx install markitdown
pipx install 'markitdown[pdf,docx,pptx]'
pipx install 'markitdown[all]'
```

If the tool is installed without the feature group you need, reinstall it with the narrower or broader extras set you actually want.

Read [references/feature-groups.md](references/feature-groups.md) before installing extras when the user only needs a subset of formats.

## Use The CLI

Convert a file and print Markdown to stdout:

```powershell
markitdown .\report.pdf
```

Write to a file:

```powershell
markitdown .\report.pdf -o .\report.md
```

Pipe binary input and give MarkItDown an extension hint:

```powershell
Get-Content .\report.pdf -AsByteStream | markitdown -x .pdf -o .\report.md
```

Use MIME or charset hints when the input source is ambiguous:

```powershell
markitdown -x .html -m text/html .\page.bin
markitdown -x .csv -c utf-8 .\data.txt
```

Keep inline `data:` URIs instead of truncating them:

```powershell
markitdown --keep-data-uris .\page.html -o .\page.md
```

## Choose Extras Deliberately

- Install base `markitdown` for lightweight text-like inputs and general conversion.
- Install targeted extras when the user only needs specific formats.
- Install `[all]` only when broad coverage matters more than dependency size.
- Reinstall with `az-doc-intel` when using Azure Document Intelligence.
- Reinstall with `audio-transcription` or `youtube-transcription` only for transcription workflows.

The current extras list and format mapping lives in [references/feature-groups.md](references/feature-groups.md).

## Common Workflows

Convert Office or PDF documents:

```powershell
markitdown .\slides.pptx -o .\slides.md
markitdown .\notes.docx -o .\notes.md
markitdown .\table.xlsx -o .\table.md
markitdown .\scan.pdf -o .\scan.md
```

Convert a YouTube URL or archive when the relevant support is installed:

```powershell
markitdown "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o .\video.md
markitdown .\bundle.zip -o .\bundle.md
```

Use Azure Document Intelligence for extraction:

```powershell
markitdown .\scan.pdf -d -e "https://<resource>.cognitiveservices.azure.com/" -o .\scan.md
```

List installed third-party plugins:

```powershell
markitdown --list-plugins
markitdown --use-plugins .\input.pdf -o .\input.md
```

## Use The Python API

Use the Python API when the user needs MarkItDown inside a script instead of as a standalone command:

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False)
result = md.convert("report.pdf")
print(result.markdown)
```

Use a configured endpoint for Document Intelligence:

```python
from markitdown import MarkItDown

md = MarkItDown(docintel_endpoint="https://<resource>.cognitiveservices.azure.com/")
result = md.convert("scan.pdf")
print(result.markdown)
```

## Troubleshoot Quickly

- If `markitdown` is missing, install it with `uv tool install ...` or `pipx install ...`.
- If a format is unsupported, check whether the right extra was installed first.
- If stdin conversion looks wrong, add `-x`, `-m`, or `-c` hints.
- If `-d` fails, verify the endpoint and that `az-doc-intel` support is installed.
- If plugin behavior is expected, run `markitdown --list-plugins` and then add `--use-plugins`.
- If output details are unclear, run `markitdown --help` and then check the upstream docs.

## Last Resort

Use these sources when local behavior is unclear or the package changes:

- CLI help: `markitdown --help`
- Main docs: `https://github.com/microsoft/markitdown/tree/main`
- README: `https://raw.githubusercontent.com/microsoft/markitdown/main/README.md`
