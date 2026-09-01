# MarkItDown Feature Groups

Use this file when the user wants only the dependencies needed for specific formats instead of `markitdown[all]`.

## Install Patterns

Prefer `uv`:

```powershell
uv tool install markitdown
uv tool install 'markitdown[pdf]'
uv tool install 'markitdown[pdf,docx,pptx]'
uv tool install 'markitdown[all]'
```

Fall back to `pipx`:

```powershell
pipx install markitdown
pipx install 'markitdown[pdf]'
pipx install 'markitdown[pdf,docx,pptx]'
pipx install 'markitdown[all]'
```

If the wrong extras were installed, uninstall and reinstall with the exact extras set you need.

## Feature Groups

| Extra | Install when you need | Notes |
|---|---|---|
| `all` | broad format coverage | easiest option, heaviest dependency set |
| `pptx` | PowerPoint files | `.pptx` |
| `docx` | Word files | `.docx` |
| `xlsx` | modern Excel files | `.xlsx` |
| `xls` | legacy Excel files | `.xls` |
| `pdf` | PDF files | `.pdf` |
| `outlook` | Outlook messages | `.msg` style workflows |
| `az-doc-intel` | Azure Document Intelligence extraction | requires Azure endpoint |
| `audio-transcription` | speech transcription from audio | wav/mp3 workflows |
| `youtube-transcription` | YouTube transcript fetching | URL-based transcript workflows |

## Practical Defaults

- Use base `markitdown` first for HTML, CSV, JSON, XML, plain text, and quick experiments.
- Use `markitdown[pdf,docx,pptx]` for common document extraction.
- Use `markitdown[pdf,docx,pptx,xlsx]` for a typical office-document bundle.
- Use `markitdown[all]` only when setup speed matters more than dependency size.

## Upstream References

- Repository: `https://github.com/microsoft/markitdown/tree/main`
- README: `https://raw.githubusercontent.com/microsoft/markitdown/main/README.md`
- PyPI: `https://pypi.org/project/markitdown/`
