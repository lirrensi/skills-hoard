---
name: video-creator
description: Use this skill whenever the user wants to create, edit, automate, or package videos with Remotion, MoviePy, or a hybrid pipeline. Trigger for motion-graphics templates, animated title cards, lower thirds, data-driven scenes, stitched footage, subtitles, aspect-ratio variants, audio swaps, batch exports, or Python-orchestrated pipelines where Remotion renders designed segments and MoviePy assembles final deliverables.
---

# Video Creator

## Mental Model

- **Remotion** is the authoring and motion-graphics brain. Use it for scenes, timing, layout, animated UI, reusable templates, and data-driven visuals.
- **MoviePy** is the post-processing and assembly belt. Use it for trimming, concatenation, fades, audio swaps, resizing, cropping, transcoding, and batch exports.
- **Hybrid** is often the production sweet spot: Remotion renders the polished segments, then MoviePy stitches those renders with footage, voiceover, music, and variants.

## Route First

| User need | Primary tool | Why | Read next |
|---|---|---|---|
| Animated title cards, lower thirds, charts, branded scenes, reusable motion templates | Remotion | React-driven timeline and component model are better for designed motion | `references/remotion.md` |
| Trim clips, merge videos, add music, fade audio, crop, resize, transcode, batch-process outputs | MoviePy | Python plus FFmpeg is better for clip operations and automation | `references/moviepy.md` |
| Render branded segments, then combine them with real footage, narration, or many export variants | Hybrid | Clean split: Remotion designs, MoviePy packages | `references/hybrid-pipeline.md` |

## Core Rule

Let **one tool own creative timing**.

- Default: Remotion owns composition, animation, and timing.
- MoviePy owns ingestion, assembly, utility transforms, final packaging, and bulk exports.
- If the task is simple and already fits one stack, stay in that stack instead of forcing a hybrid pipeline.

## If-Then Routing

- If the user wants an animated explainer, social promo, title sequence, branded outro, dashboard video, or reusable visual template, start with Remotion.
- If the user wants to merge clips, trim footage, attach music, normalize durations, add fades, crop for vertical, or export many variants, start with MoviePy.
- If the user wants both designed motion and real-world footage in one deliverable, use the hybrid approach.
- If Python is already the orchestration layer, let Python decide what to render, call Remotion as a subprocess or service, then use MoviePy for final assembly.
- If an existing codebase already uses Remotion or MoviePy, preserve that choice unless the missing capability clearly belongs in the other tool.

## Working Procedure

1. Inspect the inputs: footage, audio, data, aspect ratios, output formats, and whether the user needs reusable templates or one-off edits.
2. Decide the timeline owner before writing code.
3. Build the designed segments in Remotion when motion design matters.
4. Use MoviePy for file manipulation, assembly, and export utilities.
5. Verify duration, fps, resolution, aspect ratio, and audio sync at the end.

## Hybrid Default

When the request mixes motion graphics and video operations, prefer this split:

1. Remotion renders the hero clips.
2. MoviePy loads those renders plus user footage and audio.
3. MoviePy applies light transitions, trims, sequencing, and export packaging.

Do not let both tools fight over the same timeline unless there is a strong reason.

## Output Expectations

When using this skill, make the implementation choice explicit:

- say which tool owns timing
- say which tool handles final assembly
- keep asset handoffs simple and file-based
- avoid moving layout logic into Python if React should own it
- avoid rebuilding basic clip surgery in Remotion if MoviePy already solves it cleanly

## Bundled Material

- `references/remotion.md` - Remotion setup, composition model, rendering, and motion-design patterns
- `references/moviepy.md` - MoviePy v2 editing patterns, clip operations, and template usage
- `references/hybrid-pipeline.md` - how to combine both stacks without timeline spaghetti
- `moviepy-templates/` - ready-to-run MoviePy utility scripts for common post-processing tasks
- `remotion-templates/README.md` - a single Remotion primitive catalog for building scenes and combining blocks
