# Literature Phase (01)

Search academic literature and conduct comprehensive reviews.

## Skills Consolidated

- **literature-search**: Search Semantic Scholar, arXiv, OpenAlex
- **literature-review**: Multi-perspective dialogue-based review synthesis

## Quick Actions

### Search for Papers
```bash
# Semantic Scholar (peer-reviewed focus)
python scripts/literature/search_semantic_scholar.py \
  --query "transformer attention mechanisms" \
  --top-conferences --min-citations 5 -o results_ss.jsonl

# OpenAlex (broader coverage)
python scripts/literature/search_openalex.py \
  --query "neural attention" \
  --min-citations 10 -o results_openalex.jsonl

# Download PDFs (sorted by citations)
python scripts/literature/download_papers.py \
  --jsonl results_ss.jsonl \
  --output-dir papers/ \
  --sort-by-citations --max-downloads 15
```

### Conduct Literature Review
See `refs/00-pipeline-overview.md` for the full dialogue-based review workflow.

**Key principle**: Every claim must be supported by a citation.

## Search Strategies

### Source Priority (highest to lowest)
1. **Peer-reviewed conference papers** (NeurIPS, ICML, ACL, CVPR)
2. **Peer-reviewed journals** (JMLR, TMLR, Nature, Science)
3. **arXiv preprints with high citations** (≥10 citations)
4. **Recent arXiv preprints** (<6 months, mark as `(preprint)`)

### Query Construction
- Start broad, then narrow with filters
- Use `--venue NeurIPS ICML` for top conferences only
- Use `--min-citations N` to filter by impact
- Use `--year-min 2020` for recency

### Ranking Formula
```
score = 0.3*citations + 0.3*recency + 0.2*venue_quality + 0.2*relevance
```

## Output Format

### JSONL Schema (per paper)
```json
{
  "title": "...",
  "authors": ["...", "..."],
  "abstract": "...",
  "year": 2023,
  "venue": "NeurIPS 2023",
  "venue_normalized": "neurips",
  "peer_reviewed": true,
  "citationCount": 45,
  "paperId": "paper_id",
  "arxiv_id": "2301.12345",
  "pdf_url": "https://...",
  "tags": ["transformer", "attention"],
  "source": "semantic_scholar"
}
```

### BibTeX Citation Keys
Format: `firstAuthorYearKeyword` (e.g., `vaswani2017attention`)

## Literature Review Workflow

### Step 1: Generate Expert Personas
Create diverse expert perspectives (e.g., critic, optimist, domain specialist).

### Step 2: Grounded Q&A Dialogue
Each persona asks questions → Ground answers in retrieved papers with citations.

### Step 3: Synthesize Findings
Produce structured review with:
- Thematic organization
- Compare/contrast analysis
- Gap identification
- Every claim cited

### Step 4: Output Format
```markdown
# Literature Review: [Topic]

## Theme 1: [Name]
Smith et al. [1] propose... Johnson et al. [2] argue...

**Gap identified**: No work addresses X under Y conditions.

## Theme 2: [Name]
...

## Summary
- Key finding 1
- Key finding 2
- Open questions
```

## Validation

- **Minimum papers**: ≥15 for comprehensive review
- **Venue diversity**: ≥3 different venues
- **Recency**: ≥3 papers from last 2 years
- **Citation check**: Run `validate_citations.py` before writing

## Scripts

| Script | Purpose | Key Flags |
|--------|---------|-----------|
| `search_semantic_scholar.py` | Search Semantic Scholar API | `--peer-reviewed-only`, `--top-conferences`, `--min-citations N` |
| `search_openalex.py` | Search OpenAlex API | `--min-citations N`, `--year-min Y` |
| `search_crossref.py` | Search Crossref API | `--types article-journal` |
| `download_arxiv_source.py` | Download from arXiv | `--arxiv-id`, `--output-dir` |
| `download_papers.py` | Batch download PDFs | `--jsonl`, `--sort-by-citations`, `--max-downloads` |

## Downstream

- **Feeds into**: Phase 02 (novelty assessment), Phase 05 (related work writing)
- **Reference files**: `refs/02-ideation-phase.md`, `refs/05-writing-phase.md`