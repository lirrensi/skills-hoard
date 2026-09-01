# Remotion Primitives

This file is the single compact map of the main Remotion building blocks.

Use it when someone needs to understand what parts Remotion gives you, how those parts combine, and which primitives usually own scene structure, layout, timing, and media.

The guidance below is based on the Remotion source and docs in the upstream repo, especially the exported core API and docs for `Composition`, `AbsoluteFill`, `Sequence`, `Series`, `useCurrentFrame`, `useVideoConfig`, `interpolate`, `spring`, media tags, and `staticFile()`.

## The Block Families

### 1. Renderable entry points

- `Composition` registers a renderable video with an `id`, `width`, `height`, `fps`, `durationInFrames`, and optional `defaultProps`.
- `registerRoot()` wires the root tree into Remotion.
- `Folder` helps organize many compositions in the studio sidebar.

Think of `Composition` as the top-level contract: what can be rendered, how long it is, and which props drive it.

## 2. Layout blocks

- `AbsoluteFill` is the default full-frame layer wrapper. It is the basic block for stacking backgrounds, text, overlays, and masks.
- Plain React components still do most of the real layout work. Remotion gives you timing and media awareness, not a separate layout language.

Use `AbsoluteFill` when you want layers on top of each other.

## 3. Time and sequencing blocks

- `Sequence` shifts a block in time with `from` and can trim mounting with `durationInFrames`.
- `Series` is the easiest way to place scenes one after another without calculating every offset by hand.
- `Loop` repeats a block.
- Nested `Sequence` blocks cascade, so inner timing stays relative to the outer timing.

Use `Sequence` for offsets and overlays.
Use `Series` for scene chains.

## 4. Frame and config hooks

- `useCurrentFrame()` returns the current frame.
- `useVideoConfig()` returns `width`, `height`, `fps`, `durationInFrames`, the composition `id`, and resolved props.

These two are the heart of most Remotion components:

- `useCurrentFrame()` answers "where am I in time?"
- `useVideoConfig()` answers "what canvas and timing contract am I inside?"

## 5. Motion drivers

- `interpolate()` maps one range to another. It is great for opacity, transforms, color progress, and multi-stop timing.
- `spring()` gives you physics-based motion and can be stretched with `durationInFrames` or delayed.
- `Easing` exists for curve shaping when a spring is not the right feel.
- `interpolateColors()` maps progress into color changes.
- `random()` is available when controlled variation is needed.

Good mental model:

- use `interpolate()` for direct mapping
- use `spring()` for physical entrance and settle behavior
- combine them when a spring should drive a value range like `0 -> 200px`

## 6. Media and asset blocks

- `Img` renders images cleanly inside the pipeline.
- `staticFile()` turns a file in `public/` into a stable URL for images, audio, video, and fonts.
- `OffthreadVideo` is the usual recommendation for video playback in Remotion's docs.
- `Html5Video` and `Html5Audio` are the HTML-media-backed options.
- `Audio` and `Video` from `@remotion/media` are the newer media components when that package is in play.

Use `staticFile()` rather than hardcoded asset strings when the asset belongs to the project.

## 7. Async and environment helpers

- `delayRender()` and `continueRender()` help when data or assets must load before rendering.
- `useDelayRender()` wraps that pattern in hook form.
- `useRemotionEnvironment()` lets you branch between preview and render environments when needed.

These are support blocks, not the main storytelling blocks.

## Common Combination Patterns

### Layer stack

Use nested `AbsoluteFill` blocks:

1. background layer
2. media layer
3. typography layer
4. accent or logo layer

This is the standard title-card and lower-third pattern.

### Timed entrance

Use:

1. `const frame = useCurrentFrame()`
2. `const opacity = interpolate(frame, [0, 15], [0, 1], {extrapolateRight: 'clamp'})`
3. apply the value to style

Use this for fades, slides, reveals, and scale ramps.

### Scene chain

Use `Series` when scenes should play in strict sequence:

```tsx
<Series>
  <Series.Sequence durationInFrames={45}>
    <Intro />
  </Series.Sequence>
  <Series.Sequence durationInFrames={120}>
    <MainSection />
  </Series.Sequence>
  <Series.Sequence durationInFrames={45}>
    <Outro />
  </Series.Sequence>
</Series>
```

Use this when each scene is conceptually separate.

### Overlay on top of a base video

Use `AbsoluteFill` for layering and `Sequence` for when overlays appear:

```tsx
<AbsoluteFill>
  <OffthreadVideo src={staticFile('/footage.mp4')} />
  <Sequence from={20} durationInFrames={60}>
    <AbsoluteFill style={{justifyContent: 'flex-end', padding: 80}}>
      <LowerThird />
    </AbsoluteFill>
  </Sequence>
</AbsoluteFill>
```

### Staggered repeated elements

Map over items and wrap each one in a `Sequence` with a progressive `from` value.

This is the clean way to build bullet reveals, card cascades, or chart labels.

### Data-driven template

Use `defaultProps` or render props on `Composition`, then pass structured data into reusable scene components.

That keeps the template stable while content changes.

## Practical Starter Set

If someone is new to Remotion, the smallest useful toolkit is:

- `Composition`
- `AbsoluteFill`
- `Sequence`
- `useCurrentFrame()`
- `useVideoConfig()`
- `interpolate()`
- `spring()`
- `Img`
- `staticFile()`
- `OffthreadVideo`

With just those, you can build title cards, lower thirds, intros, quote cards, simple explainers, and timed overlays.

## Rules of Thumb

- Reach for `Series` when you are sequencing scenes; reach for `Sequence` when you are offsetting or trimming a block.
- Keep layout and motion logic in React components, not in downstream Python code.
- Use props to vary scenes instead of duplicating compositions.
- Keep dimensions, fps, and duration intentional so MoviePy can ingest the output without surprises.
- If the task turns into trimming, stitching, audio replacement, or export variants, hand off to MoviePy after Remotion renders.
