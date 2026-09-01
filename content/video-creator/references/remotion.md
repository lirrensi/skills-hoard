# Remotion Guide

Load this guide when the request is about designed motion, reusable scene templates, animated typography, charts, lower thirds, or data-driven video visuals.

## What Remotion Should Own

- scene structure
- frame-accurate timing
- animated text and UI
- reusable branded templates
- data-to-visual rendering

## Setup

```bash
npx create-video@latest
npm run dev
```

If the project already exists, preserve its package manager and folder layout.

## Core Primitives

- `Composition` defines a renderable video entry point.
- `useCurrentFrame()` gives the current frame.
- `useVideoConfig()` gives width, height, fps, and duration.
- `interpolate()` maps frame progress to animated values.
- `Sequence` offsets sections on the timeline.
- `AbsoluteFill` is the common full-frame layout wrapper.

## Minimal Composition

```tsx
import {AbsoluteFill, Composition, interpolate, useCurrentFrame} from 'remotion';
import {registerRoot} from 'remotion';

const TitleCard = ({title}: {title: string}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 15], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#0f172a',
        color: 'white',
        fontSize: 96,
        opacity,
      }}
    >
      {title}
    </AbsoluteFill>
  );
};

const Root = () => (
  <Composition
    id="TitleCard"
    component={TitleCard}
    width={1920}
    height={1080}
    fps={30}
    durationInFrames={90}
    defaultProps={{title: 'Launch Day'}}
  />
);

registerRoot(Root);
```

## Rendering

```bash
npx remotion render src/index.ts TitleCard out/title-card.mp4 --props='{"title":"Quarterly Review"}'
```

Use props to keep templates data-driven instead of hardcoding content.

## Good Fits

- title cards and intros
- lower thirds and callouts
- chart or dashboard sequences
- branded social clips
- reusable templates fed by JSON or API data

## Primitive Catalog

For a compact field guide to the main Remotion building blocks and how to combine them, read `remotion-templates/README.md`.

## Best Practices

- Keep visual timing in Remotion instead of trying to re-time the same animation later in MoviePy.
- Build reusable scene components, then vary them through props.
- Lock fps, dimensions, and durations intentionally so downstream assembly stays predictable.
- Prefer compositions for renderable outputs and components for reusable scene parts.

## Common Pitfalls

- Mixing layout logic across too many files before the composition shape is clear.
- Rendering with ad hoc fps or dimensions that do not match the downstream pipeline.
- Using Remotion for basic bulk file manipulation that MoviePy can do more simply.
