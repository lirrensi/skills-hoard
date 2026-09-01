# Hybrid Pipeline Guide

Load this guide when the request needs both designed motion graphics and practical video assembly.

## Recommended Split

| Responsibility | Tool |
|---|---|
| scene design and animation | Remotion |
| reusable templates and data visuals | Remotion |
| render hero segments | Remotion |
| ingest user footage and external clips | MoviePy |
| fades, audio swaps, packaging, and variants | MoviePy |
| final batch export automation | MoviePy |

## Preferred Pipeline Shapes

### Option A: JS-first

`data -> Remotion -> final mp4`

Use this when the whole deliverable is basically motion graphics.

### Option B: Hybrid

`data/assets -> Remotion segments -> MoviePy assembly -> deliverables`

Use this when branded sequences need to sit beside footage, screen recordings, narration, or multiple export variants.

### Option C: Python orchestrates everything

`Python job -> Remotion renders -> MoviePy assembly -> outputs`

Use this when a backend or automation system already lives in Python.

## Default Rule

Pick one source of truth for the creative timeline.

- Usually Remotion owns timing and visual sequencing.
- MoviePy may still do trims, fades, and assembly, but should not become a second creative timeline unless the task clearly requires it.

## Handoff Contract

Keep the handoff between tools boring and predictable:

- render fixed mp4 files from Remotion
- keep fps and resolution explicit
- pass props or manifests, not hidden state
- use clear output file names per segment
- let MoviePy treat Remotion renders as standard input clips

## Example Orchestration

```python
import json
import subprocess

props = json.dumps({
    "title": "Q4 Wrap",
    "points": ["Revenue up", "Costs down", "Launch on track"],
})

subprocess.run([
    "npx",
    "remotion",
    "render",
    "src/index.ts",
    "SummaryScene",
    "renders/summary.mp4",
    "--props",
    props,
], check=True)
```

After rendering, load `renders/summary.mp4` in MoviePy alongside footage, audio, and outro assets.

## Good Use Cases

- branded intro + user footage + branded outro
- chart sequence + screen recording + narration
- templated social clips rendered from data, then packaged into many sizes
- Python automation that needs polished motion graphics without abandoning the existing stack

## Anti-Patterns

- designing animation timing in Remotion, then heavily re-timing the same segment in MoviePy
- splitting text layout between React and Python
- using MoviePy to fake a component-based motion system
- using Remotion to perform bulk file surgery that belongs in Python
