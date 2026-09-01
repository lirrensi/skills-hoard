---
name: scrollytelling-page-generator
description: Build self-contained, single-file HTML long-form reading article. Transforming long texts like a book or very long papers, essays, complex long material into a single interactive page.
---
# 📖 The Scrollytelling Book Playbook

## Turning any book summary into a beautiful, scrollable reading experience.

No clicking to read. No hidden content. Just scroll and absorb.

---

## Step 0: Before You Start — User Preferences

Before building anything, ask the user these questions.
Get this wrong and the entire output feels off. Get it right and it just *fits*.

### The Questions

**1. Language & Tone**
```
How should the text feel?

A) Formal / Academic      — "The research suggests that..."
B) Conversational         — "Here's the thing most people miss..."
C) Casual / Sassy         — "Okay so basically this is wild but..."
D) Poetic / Reflective    — "There is a quiet truth hidden in..."
```

**2. Content Focus**
```
What matters most to the reader?

A) Key lessons & takeaways    — "What can I apply tomorrow?"
B) Core content & ideas       — "Give me the full picture"
C) Memorable highlights       — "What will I remember in a year?"
D) Balanced overview          — Mix of all three
```

**3. Complexity Level**
```
How deep should it go?

A) Light & digestible    — Short paragraphs, lots of visuals, quick read
B) Medium depth          — Some detail, good balance of text and visuals
C) Deep & thorough       — Longer explanations, fewer visuals, more nuance
```

**4. Visual Richness**
```
How much visual variety?

A) Minimal       — Clean text, subtle animations, maybe one canvas per book
B) Moderate      — Canvas animations per chapter, stats, comparisons
C) Rich          — Multiple animations, interactive scroll elements, full visual suite
```

**5. Book Genre** (affects default color mood)
```
What kind of book?

A) Self-help / Relationships    — Warm tones, approachable
B) Business / Productivity      — Clean, professional, structured
C) Science / Philosophy         — Cool tones, contemplative
D) Creative / Narrative         — Flexible, expressive
E) Technical / How-to           — Clear, organized, practical
```

### How Preferences Affect Output

| Preference | Effect |
|-----------|--------|
| Formal | Serif fonts, longer paragraphs, fewer emojis, measured pacing |
| Casual | System fonts, short paragraphs, conversational asides, faster pacing |
| Lessons-focused | Extra emphasis on key ideas section, actionable do/don't lists |
| Content-focused | Fuller summaries, more comparison sections, detailed explanations |
| Memorable | More pull quotes, larger visual statements, fewer but bigger ideas |
| Light | Shorter chapters, more visual breathing room, simpler canvas |
| Deep | Longer text blocks, more stat details, fewer but more impactful visuals |
| Rich canvas | Multiple canvas animations, scroll-synced effects, animated transitions |

### Output Format

Save these preferences as the **config block** at the top of every build:

```yaml
preferences:
  tone: conversational
  focus: key_lessons
  depth: medium
  visual_richness: moderate
  genre: self-help
  themes:
    primary: "#e85d44"
    secondary: "#7b68ee"
```

---

## Part 1: The Content Recipe

Before writing code, extract this data from the book.
This is the **input** to the system.

### Book-Level Data

```
book:
  title: "[Book Title]"
  author: "[Author Name]"
  tagline: "[One sentence that captures the book's promise]"
  language: "[ru | en | es | ...]"        # for lang attribute
  chapter_count: "[any number]"
```

### Per-Chapter Data

For each chapter, extract the following.
Adapt quantity to the book — some chapters have 3 key ideas, some have 8. That's fine.

```
chapter:
  number: [N]
  title: "[Chapter Title]"

  # 1-2 sentences. The hook that makes someone want to read this chapter.
  hook: "[Why this chapter matters — punchy, one breath]"

  # The meat. 2-5 paragraphs depending on depth preference.
  # Match the tone from Step 0.
  summary:
    - "[First paragraph — sets up the concept or problem]"
    - "[Second paragraph — explains the mechanism or insight]"
    - "[Third paragraph — the 'so what' — why it matters]"

  # Short, punchy, visible immediately. NO hidden cards.
  # 3-8 ideas per chapter, depending on chapter richness.
  key_ideas:
    - label: "[Short label — e.g. 'The Core Insight' or '01']"
      text: "[One clear sentence that captures the idea]"

  # 0-2 per chapter. Only genuinely powerful quotes.
  quotes:
    - text: "[The quote]"
      source: "[Who said it, or where it's from]"

  # Only if the chapter has meaningful numbers.
  stats:
    - number: "[e.g. 73%]"
      label: "[What this number means in plain language]"

  # Only if the chapter contrasts two or more approaches/perspectives.
  comparison:
    - label: "[Perspective A name]"
      heading: "[Short heading]"
      points:
        - "[Point 1]"
        - "[Point 2]"
    - label: "[Perspective B name]"
      heading: "[Short heading]"
      points:
        - "[Point 1]"
        - "[Point 2]"

  # Practical takeaways. Visible immediately, no clicking.
  actions:
    dos:
      - "[Imperative sentence — what TO do]"
    donts:
      - "[Imperative sentence — what NOT to do]"

  # Which canvas animation fits this chapter's concept.
  # Pick from the animation catalog (Part 5).
  animation: "[wave | orbit | pulse | particles | well | timeline | seasons | none]"
```

### Content Quality Rules

1. **Summary is king.** Reading only the summary should give 70% of the chapter's value.
2. **Key ideas fit in one breath.** If you can't say it in one sentence, it's two ideas.
3. **Quotes hit hard or don't include them.** No filler quotes.
4. **Stats need context.** "73%" alone is meaningless. "73% of remote workers report..." is information.
5. **Comparisons are parallel.** Same structure, different content, both sides.
6. **Actions are imperative.** "Ask before offering advice" not "One might consider asking..."
7. **No "In conclusion" paragraphs.** End chapters on a punchy note. The Key Ideas section serves as the summary.
8. **Tone matching over verbatim.** Rewrite concepts in the user's requested tone. Only the Quote section preserves original wording.
9. **Actions start with verbs.** "Wake up earlier" not "It is beneficial to wake up earlier."

### LLM Extraction Rules

When extracting content from a book, instruct the LLM:

```
- Rewrite concepts in the chosen tone (formal/casual/poetic)
- Do NOT end chapters with "In conclusion" or "In summary"
- Key ideas: one sentence each, no padding
- Actions: start with an imperative verb (Do this / Don't do that)
- Quotes: preserve exact wording, add source attribution
- Stats: include what the number is measuring
- Identify 2-5 jargon terms per chapter for glossary tooltips
```

---

## Part 2: The Design System

### Light + Dark Mode (Non-Negotiable)

Both modes are built from day one. A toggle in the top-right corner switches between them.
Default follows system preference (`prefers-color-scheme`).

```css
/* ── LIGHT MODE ── */
:root,
[data-theme="light"] {
  --bg:           #fafafa;
  --bg-subtle:    #f2f2f5;
  --surface:      #ffffff;
  --surface-2:    #f7f7f9;
  --border:       #e0e0e6;
  --text:         #1a1a2e;
  --text-dim:     #666680;
  --text-muted:   #9999aa;
  --accent-1:     #d44a2e;
  --accent-1-dim: #f0d0c8;
  --accent-1-glow:rgba(212,74,46,0.08);
  --accent-2:     #6050c0;
  --accent-2-dim: #d8d0f0;
  --accent-2-glow:rgba(96,80,192,0.08);
  --gold:         #b8922e;
  --green:        #2e9e60;
  --red:          #cc3838;
  --shadow:       rgba(0,0,0,0.06);
}

/* ── DARK MODE ── */
[data-theme="dark"] {
  --bg:           #0a0a0f;
  --bg-subtle:    #101018;
  --surface:      #14141e;
  --surface-2:    #1a1a28;
  --border:       #2a2a3e;
  --text:         #e8e8f0;
  --text-dim:     #8888aa;
  --text-muted:   #555570;
  --accent-1:     #e85d44;
  --accent-1-dim: #3a1e16;
  --accent-1-glow:rgba(232,93,68,0.15);
  --accent-2:     #7b68ee;
  --accent-2-dim: #2a2260;
  --accent-2-glow:rgba(123,104,238,0.15);
  --gold:         #d4a843;
  --green:        #4caf82;
  --red:          #e05555;
  --shadow:       rgba(0,0,0,0.3);
}
```

### Theme Toggle

```html
<button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">
  <span class="icon-sun">☀</span>
  <span class="icon-moon">☾</span>
</button>
```

```javascript
function toggleTheme() {
  const root = document.documentElement;
  const current = root.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  root.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
}

// On load: respect saved preference, then system preference, then default to dark
(function initTheme() {
  const saved = localStorage.getItem('theme');
  if (saved) {
    document.documentElement.setAttribute('data-theme', saved);
  } else if (window.matchMedia('(prefers-color-scheme: light)').matches) {
    document.documentElement.setAttribute('data-theme', 'light');
  } else {
    document.documentElement.setAttribute('data-theme', 'dark');
  }
})();
```

### Typography

```
# Two options — pick based on tone from Step 0
# Formal / Reflective → Georgia, serif
# Casual / Conversational → System sans-serif

# Body
font-size: 1rem (16px)
line-height: 1.7
max-width: 680px
margin: 0 auto

# Headings
font-size: clamp(1.5rem, 3vw, 2.5rem)
font-weight: 300-400 (light, airy, not aggressive)

# Labels & Tags
font-size: 0.7rem
letter-spacing: 0.15em
text-transform: uppercase
```

### Spacing

```
--space-xs:  0.5rem   (8px)
--space-sm:  1rem     (16px)
--space-md:  2rem     (32px)
--space-lg:  4rem     (64px)
--space-xl:  6rem     (96px)
--space-book-break: 8rem (128px)   # Between chapters
```

### Accent Colors by Genre

Use these as starting points. Adjust freely.

| Genre | Accent 1 (warm) | Accent 2 (cool) |
|-------|-----------------|-----------------|
| Self-help / Relationships | `#e85d44` | `#7b68ee` |
| Business / Productivity | `#2e7cd5` | `#38b280` |
| Science / Philosophy | `#5088cc` | `#8868bb` |
| Creative / Narrative | `#d45588` | `#44aa88` |
| Technical / How-to | `#cc7722` | `#4488cc` |
| History / Non-fiction | `#aa7744` | `#557799` |

---

## Part 3: Universal Section Templates

These are the **building blocks**. Every chapter is assembled from them.
None of them hide content behind a click.
They work for ANY book, ANY genre, ANY chapter count.

### Template: Progress Bar

Thin bar at the top of the viewport. Shows how far you've read.

```
┌──────────────────────────────────────────┐ ← 2-3px tall, fixed top
│████████████████████░░░░░░░░░░░░░░░░░░░░░│    gradient: accent-1 → accent-2
└──────────────────────────────────────────┘
```

### Template: Theme Toggle

Small button in top-right corner. Sun/moon icon.

```
                                ┌──────┐
                                │ ☀ / ☾ │  ← fixed, top-right, small
                                └──────┘
```

### Template: Chapter Hero

Full viewport or near-full. Centered text. Sets the mood.

```
┌─────────────────────────────────────────┐
│                                         │
│         CHAPTER [N]                     │  ← label: uppercase, muted, small
│                                         │
│    [Chapter Title Goes Here]            │  ← h1: large, light weight
│                                         │
│  [One or two sentences that hook        │  ← subtitle: dim, italic
│   the reader into this chapter.]        │
│                                         │
│       ┌─────────────────────┐           │  ← optional: canvas animation
│       │                     │           │
│       │   [canvas element]  │           │
│       │                     │           │
│       └─────────────────────┘           │
│                                         │
│              ↓                          │  ← subtle scroll hint
│                                         │
└─────────────────────────────────────────┘
```

### Template: Summary Block

Normal readable text. The primary content delivery mechanism.

```
┌─────────────────────────────────────────┐
│                                         │
│  [Section label — optional]             │  ← e.g. "The Problem"
│                                         │
│  [Paragraph one. Sets up the concept,   │
│   introduces the tension, frames the    │
│   question the chapter answers.]        │
│                                         │
│  [Paragraph two. Explains the           │
│   mechanism, the insight, the core      │
│   idea the chapter is built around.]    │
│                                         │
│  [Paragraph three. The "so what."       │
│   Why this matters. What changes if     │
│   you understand this.]                 │
│                                         │
└─────────────────────────────────────────┘
```

### Template: Key Ideas

Short, punchy statements. All visible. No expanding, no clicking.
Each one could be a tweet. Together they're the chapter's skeleton.

```
┌─────────────────────────────────────────┐
│                                         │
│  KEY IDEAS                              │  ← section label
│                                         │
│  ┌─────────────────────────────────┐    │
│  │ 01 / [Label]                    │    │  ← accent color label
│  │                                 │    │
│  │ [One sentence that captures     │    │  ← all text visible
│  │  the core of this idea.]        │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │ 02 / [Label]                    │    │
│  │                                 │    │
│  │ [One sentence that captures     │    │
│  │  the core of this idea.]        │    │
│  └─────────────────────────────────┘    │
│                                         │
│  [3-8 cards, all visible, stacked]      │
│                                         │
└─────────────────────────────────────────┘
```

### Template: Comparison

Side-by-side. Not tabbed. Not hidden. Both visible at once.

```
┌─────────────────────────────────────────┐
│                                         │
│  [COMPARISON LABEL]                     │
│                                         │
│  ┌────────────────┬────────────────┐    │
│  │ ● [SIDE A]     │ ● [SIDE B]     │    │
│  │                │                │    │
│  │ [Heading A]    │ [Heading B]    │    │
│  │                │                │    │
│  │ • [Point 1]    │ • [Point 1]    │    │
│  │ • [Point 2]    │ • [Point 2]    │    │
│  │ • [Point 3]    │ • [Point 3]    │    │
│  └────────────────┴────────────────┘    │
│                                         │
│  (stacks vertically on mobile)          │
│                                         │
└─────────────────────────────────────────┘
```

### Template: Statistics

Numbers that animate when scrolled into view.

```
┌─────────────────────────────────────────┐
│                                         │
│  [STATISTICS]                           │
│                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │  [73%]  │  │  [2.5x] │  │  [12]   │ │  ← large numbers
│  │ ━━━━━━━ │  │ ━━━━━━  │  │ ━━━━━   │ │  ← animated bars
│  │ [label] │  │ [label] │  │ [label] │ │  ← small labels
│  └─────────┘  └─────────┘  └─────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

### Template: Pull Quote

Big, centered, beautiful. A moment to pause.

```
┌─────────────────────────────────────────┐
│                                         │
│                   "                     │  ← decorative quote mark
│                                         │
│  [A powerful sentence or short          │
│   passage from the book that            │
│   deserves to breathe.]                 │
│                                         │
│    — [Source / Attribution]             │
│                                         │
└─────────────────────────────────────────┘
```

### Template: Do / Don't

Practical advice. All visible. No filtering, no tabs.

```
┌─────────────────────────────────────────┐
│                                         │
│  PRACTICAL TAKEAWAYS                    │
│                                         │
│  ✓ [Action to take — imperative]        │
│    [1 sentence of context if needed]    │
│                                         │
│  ✓ [Action to take — imperative]        │
│                                         │
│  ✗ [Action to avoid — imperative]       │
│    [1 sentence of context if needed]    │
│                                         │
│  ✗ [Action to avoid — imperative]       │
│                                         │
└─────────────────────────────────────────┘
```

### Template: Canvas Animation Zone

Visual metaphor. Inline with text. Starts animating when scrolled into view.

```
┌─────────────────────────────────────────┐
│                                         │
│  [VISUAL METAPHOR LABEL]                │
│                                         │
│       ┌─────────────────────┐           │
│       │                     │           │
│       │   [canvas element]  │           │  ← auto-animates on scroll
│       │   responsive width  │           │
│       │                     │           │
│       └─────────────────────┘           │
│                                         │
│  [Short explanation of what the         │  ← always visible below
│   visual represents. Plain text,        │     canvas
│   2-3 sentences max.]                   │
│                                         │
└─────────────────────────────────────────┘
```

### Template: Chapter Divider

Separates chapters. Subtle but clear signal of "new topic."

```
┌─────────────────────────────────────────┐
│                                         │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │  ← gradient line
│                                         │
└─────────────────────────────────────────┘
```

### Template: Top Bar (Global)

Fixed bar at the top of the viewport. Always present. Contains everything.

```
┌──────────────────────────────────────────────────────────────┐
│ ☰  [Current Chapter Title]   ████████████░░░░░░   Aa  ☀  👁 │
│     ← sidebar     ← progress bar →          ← toggles →    │
└──────────────────────────────────────────────────────────────┘
```

- **Left**: Sidebar toggle (☰) + current chapter title (updates on scroll)
- **Center**: Progress bar (gradient fill, accent-1 → accent-2)
- **Right**: Font toggle (Aa) + Theme toggle (☀/☾) + Accessibility (👁)

The chapter title updates as you scroll. It shows which chapter you're currently reading.

### Template: Sidebar (Global)

Collapsible left panel. Optional chapter navigation.
Like a PDF sidebar — you CAN jump to sections, but you don't HAVE to.

```
     ┌────────────────────────┐
     │ [Book Title]           │
     │ by [Author]            │
     ├────────────────────────┤
     │  01 [Chapter 1 Title]  │  ← active = accent border
     │  02 [Chapter 2 Title]  │
     │  03 [Chapter 3 Title]  │
     │  ...                   │
     ├────────────────────────┤
     │  Aa  ☀  👁             │  ← same toggles duplicated
     └────────────────────────┘
```

- Opens on ☰ click, closes on overlay click or chapter click
- Active chapter highlighted with accent left border
- Toggles duplicated in footer for convenience

### Template: End Screen (Book Closing)

The final section. Book's thesis recap + attribution.

```
┌─────────────────────────────────────────┐
│                                         │
│  THE CORE MESSAGE                       │  ← section label
│                                         │
│  [Two or three sentences that capture   │
│   the single most important thing this  │
│   book teaches. The one idea worth      │
│   remembering if you forget everything  │
│   else.]                                │
│                                         │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│                                         │
│    [Book Title] · [Author]              │
│                                         │
│    Built with care.                     │  ← gentle sign-off
│                                         │
└─────────────────────────────────────────┘
```

### Template: Reading Time

Displayed in the Book Hero. Gives the reader a psychological contract.

```
  📖 [N] chapters    ⏱ ~[X] min read
```

Calculation: total word count ÷ 200 words/minute = approximate minutes.
Or just estimate: short book = 15-20min, medium = 30-40min, long = 60min+.

---

## Part 4: The Content Order

Every chapter follows this **fixed sequence**. Not every chapter has every section — skip what doesn't apply. But the ORDER never changes.

```
1.  HERO                  Title + hook + optional canvas
                          ↓
2.  SUMMARY               Main text (2-5 paragraphs)
                          ↓
3.  CANVAS ANIMATION      Visual metaphor (if applicable)
                          ↓
4.  KEY IDEAS             3-8 cards, all visible
                          ↓
5.  COMPARISON            Side-by-side (if applicable)
                          ↓
6.  STATISTICS            Animated numbers (if applicable)
                          ↓
7.  QUOTE                 Big centered quote (if any)
                          ↓
8.  ACTIONS               Do / Don't list (if applicable)
                          ↓
9.  CHAPTER DIVIDER       Gradient line + optional next-chapter teaser
```

### Book-Level Flow

```
TOP BAR             Fixed — always visible, updates as you scroll
SIDEBAR             Collapsible — optional chapter navigation
     ↓
BOOK HERO           Title, author, tagline, reading time
     ↓
TABLE OF CONTENTS   Chapter list overview (visual map, not navigation)
     ↓
CHAPTER 1           (full chapter flow)
     ↓
CHAPTER 2           (full chapter flow)
     ↓
  ...                (as many chapters as the book has)
     ↓
CHAPTER N           (full chapter flow)
     ↓
END SCREEN          Core thesis recap, attribution, sign-off
```

### Background Alternation

Chapters alternate between `--bg` and `--bg-subtle` automatically.
Even subtle alternation breaks monotony and signals "new section."
Dark sections feel weighty. Light sections feel open.

```
Chapter 1 → background: var(--bg)
Chapter 2 → background: var(--bg-subtle)
Chapter 3 → background: var(--bg)
Chapter 4 → background: var(--bg-subtle)
...
```

The reader learns the rhythm after chapter 1.
By chapter 2, they stop thinking about structure and just read.

---

## Part 5: Interaction Rules

### The Golden Rule

> **If a human came here to READ, let them READ.
> Interactions enhance. They never gate.**

### The Sidebar Rule

> **The sidebar navigates TO content. It never gates, reveals, or controls content.
> If the sidebar disappeared entirely, nothing would be hidden.
> It's a scroll-teleporter, not a content controller.**

### Allowed

| Pattern | Trigger | Purpose |
|---------|---------|---------|
| Progress bar | Scroll | Shows reading position |
| Theme toggle | Click (one button) | Light/dark mode |
| Font toggle | Click (one button) | Serif ↔ Sans |
| Accessibility filter | Click (one button) | Color blindness support |
| Sidebar | Click (☰ button) | Optional chapter navigation — ignorable |
| Fade-in on scroll | Scroll past element | Cinematic reveal |
| Canvas animation | Scroll into view | Visual metaphor |
| Canvas responds to scroll | Scroll position | Animation syncs with reading |
| Stat bars fill | Scroll into view | Numbers feel alive |
| Hover on cards | Mouse hover | Subtle visual feedback only |
| Sticky chapter title | Scroll | Always know which chapter you're in |

### Forbidden

| Pattern | Why |
|---------|-----|
| Expandable cards | Gates content behind clicks |
| Tabbed sections | Hides content, forces decisions |
| "Read more" / "Show more" | If it's worth saying, say it |
| Filterable views | This is a book, not a database |
| Modal popups | Interrupts reading violently |
| Carousel / slider | Hides content off-screen |
| Dot navigation (mandatory) | Passive position dots are fine; required click nav is not |
| Any interaction that reveals content | If the interaction disappears, all content must still be visible |

### Scroll Animation Rules

1. Elements fade in as they enter viewport — IntersectionObserver, threshold 0.15
2. Siblings are staggered — `transition-delay: (i * 0.08)s`
3. Canvas starts on visibility, stops when off-screen (performance)
4. No animation exceeds 0.6s
5. **Everything is readable without JavaScript** — animations are progressive enhancement

---

## Part 6: Canvas Animation Catalog

Pick one per chapter based on the chapter's core metaphor.

| ID | Visual | Best For |
|----|--------|----------|
| `wave` | Animated sine wave | Cycles, rhythms, emotional ups and downs |
| `orbit` | Two bodies orbiting | Duality, two perspectives, partnership |
| `stars` | Twinkling star field | Hero sections, cosmic/philosophical themes |
| `well` | Vertical well with dot going down/up | Depths, introspection, inner journey |
| `pulse` | Breathing/glowing circle | Heartbeat, love, vitality |
| `particles` | Floating dots in motion | Complexity, many factors, chaos-to-order |
| `timeline` | Vertical line with animated dots | Sequential stages, processes |
| `seasons` | Rotating color wheel | Natural cycles, change over time |
| `gradient` | Slowly shifting background color | Transitions, mood changes |
| `none` | No canvas | Pure text chapter, no visual needed |

Each animation is a self-contained function:

```javascript
function drawWave(canvas, options = {}) {
  const ctx = canvas.getContext('2d');
  let animId = null;

  function frame() {
    // drawing logic
    animId = requestAnimationFrame(frame);
  }

  return {
    start() { frame(); },
    stop() { cancelAnimationFrame(animId); }
  };
}
```

Canvas elements are sized to their container with CSS:
```css
.canvas-zone canvas {
  width: 100%;
  height: 200px;   /* or whatever fits */
  display: block;
  border-radius: 12px;
  background: var(--surface);
}
```

---

## Part 7: Technical Architecture

### File Structure

Everything is a **single HTML file**. No build tools. No frameworks.
Open it in a browser and it works.

```
book-title.html (single file, ~1000-2500 lines)
│
├── <head>
│   ├── <meta> tags
│   ├── <style>
│   │   ├── CSS reset
│   │   ├── Light mode custom properties (:root)
│   │   ├── Dark mode custom properties ([data-theme="dark"])
│   │   ├── Theme toggle styles
│   │   ├── Progress bar styles
│   │   ├── Typography
│   │   ├── Section layout styles
│   │   ├── Component styles (all templates)
│   │   ├── Canvas container styles
│   │   ├── Scroll animation classes
│   │   └── Responsive breakpoints
│   └── <script> (theme init — in head to prevent flash)
│
├── <body>
│   ├── Theme toggle button
│   ├── Progress bar
│   ├── Book hero
│   ├── Chapter 1
│   │   ├── Hero section
│   │   ├── Summary section
│   │   ├── Canvas section (if any)
│   │   ├── Key ideas section
│   │   ├── Comparison section (if any)
│   │   ├── Stats section (if any)
│   │   ├── Quote section (if any)
│   │   ├── Actions section (if any)
│   │   └── Chapter divider
│   ├── Chapter 2
│   │   └── (same structure)
│   ├── ... (as many as needed)
│   ├── Chapter N
│   │   └── (same structure)
│   ├── Book closing
│   └── <script>
│       ├── Theme toggle logic
│       ├── Progress bar logic
│       ├── Scroll fade-in observer
│       ├── Stat bar animation observer
│       ├── Canvas animation functions
│       └── Canvas visibility observers
│
└── (that's it — nothing else)
```

### Key Principles

1. **No base64 encoding.** Content is plain HTML. Readable. Editable.
2. **No iframes.** Everything is one continuous DOM.
3. **No external dependencies.** No CDN links, no frameworks. Pure HTML + CSS + JS.
4. **Works offline.** Save the file, open it anywhere.
5. **View-source friendly.** Anyone can read the source and understand it.

### CSS Architecture

```css
/* ── RESET ── */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* ── LIGHT MODE (default) ── */
:root {
  --bg: #fafafa;
  /* ... full light palette ... */
}

/* ── DARK MODE ── */
[data-theme="dark"] {
  --bg: #0a0a0f;
  /* ... full dark palette ... */
}

/* ── BASE ── */
body {
  background: var(--bg);
  color: var(--text);
  font-family: /* from Step 0 */;
  line-height: 1.7;
}

/* ── LAYOUT ── */
.page { max-width: 680px; margin: 0 auto; padding: 0 1.5rem; }
.page-wide { max-width: 900px; margin: 0 auto; padding: 0 1.5rem; }

/* ── SCROLL ANIMATIONS ── */
.fade-in {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}

/* ── RESPONSIVE ── */
@media (max-width: 640px) {
  .comparison-grid { grid-template-columns: 1fr; }
  .stats-row { flex-direction: column; }
}
```

### JavaScript Architecture

Just these patterns, nothing fancy:

```javascript
// ── Theme ──
function toggleTheme() { /* swap data-theme, save to localStorage */ }

// ── Progress ──
window.addEventListener('scroll', () => { /* update bar width */ });

// ── Fade-in on scroll ──
const observer = new IntersectionObserver(callback, { threshold: 0.15 });
document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

// ── Stat bars ──
const statObserver = new IntersectionObserver(callback, { threshold: 0.3 });

// ── Canvas start/stop ──
const canvasObserver = new IntersectionObserver(callback, { threshold: 0.1 });
```

---

## Part 8: Content → HTML Mapping

How each piece of extracted data becomes HTML.

```
book.title          → Book hero <h1> + <title> tag + closing section
book.author         → Book hero + closing attribution
book.tagline        → Book hero <p>

chapter.title       → Chapter hero <h1>
chapter.hook        → Chapter hero <p class="subtitle">
chapter.summary[]   → <section><p>...</p></section> (one <p> per paragraph)
chapter.key_ideas[] → <div class="key-idea"> (all visible, stacked)
chapter.quotes[]    → <blockquote> (centered, large)
chapter.stats[]     → <div class="stat"> (animated on scroll)
chapter.comparison  → <div class="comparison-grid"> (side-by-side)
chapter.actions     → <div class="action do/dont"> (green/red dots)
chapter.animation   → <canvas> in a <div class="canvas-zone">
```

---

## Part 9: Production Checklist

### Before Building
- [ ] Step 0 preferences collected from user
- [ ] Book data fully extracted (all chapters, all fields)
- [ ] Accent colors chosen (or derived from genre defaults)
- [ ] Font choice made (serif vs sans, based on tone)
- [ ] Canvas animations assigned to chapters

### Building
- [ ] Single HTML file created
- [ ] Light mode CSS custom properties set
- [ ] Dark mode CSS custom properties set
- [ ] Theme toggle working + localStorage persistence
- [ ] System preference detection on first load
- [ ] Progress bar implemented
- [ ] All sections render correctly without JavaScript
- [ ] Scroll fade-ins working
- [ ] Canvas animations start on visibility, stop on exit
- [ ] Stat bars animate on scroll into view
- [ ] Chapter dividers between all chapters
- [ ] Mobile responsive (comparison stacks, canvas scales, text readable)

### Quality Check
- [ ] Read through ENTIRE book in one scroll (both light and dark mode)
- [ ] Confirm zero clicks are required to read any content
- [ ] Toggle between light/dark — everything looks correct in both
- [ ] Check canvas animations don't drop below 30fps
- [ ] Test on actual mobile device
- [ ] Reading test: 20 minutes continuous reading, no eye strain in either mode
- [ ] Progress bar reaches 100% at the bottom of the page
- [ ] Source code is readable and understandable

---

## Part 10: The Template

A ready-to-use HTML scaffold lives alongside this playbook: `templates/template.html`

### The Template Is a Copy

The template is **not** something you build from scratch each time. You **copy it**, then edit inside:

```
cp templates/template.html my-new-book.html
```

Then open `my-new-book.html` and start replacing placeholders. The scaffold is the starting point — never rewrite the same code twice.

### What the Template Includes

| Feature | How It Works |
|---------|-------------|
| **Top bar** | Fixed bar with sidebar toggle, current chapter title, progress bar, font/theme/a11y toggles |
| **Collapsible sidebar** | Left-side chapter menu. Opens on ☰ click. Optional — ignore it and just scroll. |
| **Reading time** | Displayed in book hero. Estimate: ~200 words/minute. |
| **Table of Contents** | Visual overview of all chapters before chapter 1. |
| **Chapter sections** | Background alternates automatically (odd/even). |
| **Key Ideas** | Visible cards, all expanded. Gold left border. |
| **Comparison** | Side-by-side grid, stacks on mobile. |
| **Stats** | Animated bars that fill on scroll into view. |
| **Pull Quote** | Centered, decorative quote mark, gold attribution. |
| **Do / Don't** | Green/red dot list, all visible. |
| **Canvas Zone** | Placeholder canvas per chapter. Wire up any animation. |
| **End Screen** | Book thesis recap + attribution + sign-off. |
| **Theme toggle** | Light ↔ Dark with View Transitions API. Respects system preference. Persists in localStorage. |
| **Font toggle** | Serif ↔ Sans-serif. Persists in localStorage. |
| **Font size slider** | Rem-based scaling tied to root. Small A ↔ Big A range input. Persists in localStorage. Works in sidebar (mobile) and settings dropdown. |
| **Settings dropdown** | Mobile: ⚙ burger in top bar opens a dropdown panel with all controls (font, theme, size, a11y, audio). Desktop: inline buttons in top bar. |
| **Accessibility filters** | Protanopia / Deuteranopia / Tritanopia color blindness filters via SVG. |
| **Focus mode audio** | 🎧 toggle generates brown noise via Web Audio API. Zero files, opt-in. |
| **Progress bar** | Gradient fill from accent-1 to accent-2. |
| **Time remaining** | Dynamic "X min left" in top bar based on scroll position. |
| **Scroll animations** | Fade-in and stagger via IntersectionObserver. |
| **Scroll-scrubbed canvas** | Canvas drawing tied to scroll progress (0→1). Scroll up = reverse animation. |
| **Hover glossary** | CSS-only tooltips for jargon terms. Dotted underline, no click needed. |
| **Print stylesheet** | Cmd+P gives a clean, UI-free PDF. Chapters page-break. |
| **Copy takeaways** | End screen button collects all Key Ideas + Actions into clipboard. |
| **RTL support** | `dir="rtl"` on `<html>` handles Arabic/Hebrew. Sidebar mirrors automatically. |
| **Responsive** | Mobile header restructured (title left, ⚙ burger right). Settings in dropdown. Comparison/stats stack on mobile. No horizontal scroll. |

### How to Use It

1. **Copy the template**: `cp templates/template.html my-new-book.html`
2. Open `my-new-book.html` in a browser to see the scaffold
3. Replace every `[PLACEHOLDER]` with your content
4. Delete sections you don't need (canvas, comparison, stats, etc.)
5. Add more `<section class="chapter">` blocks for more chapters
6. Update sidebar and ToC to match your chapters
7. Done. Single file. Works offline.

> **Key rule**: You never rewrite the CSS, JS, or layout from scratch. The template is your starting point. Every new book is a copy, not a rebuild.

---

## Quick Reference

```
STEP 0:    Ask user preferences (tone, focus, depth, visual richness, genre)
INPUT:     Structured content per chapter (summary, ideas, quotes, stats, actions)
TEMPLATE:  Open `templates/template.html`, replace placeholders, done.
DESIGN:    Light + Dark mode, font toggle, a11y filters, RTL support. All built in.
LAYOUT:    Continuous scroll. Max-width 680px for text. No iframes.
NAV:       Collapsible sidebar (scroll-teleporter, not content controller). Scroll is primary.
INTERACT:  Scroll-based only. Theme/font/a11y/audio toggles are the exceptions.
ANIMATE:   Fade-in on scroll. Canvas on visibility or scroll-scrubbed. Stats on scroll.
FILE:      Single .html file. Zero dependencies. Works offline. Cmd+P for PDF.
RULE:      If it's worth saying, it's visible. No hidden content.
```

---

*Version 3.0 — Now With a Real Template You Can Open and Use*

---

## Appendix: New Features Added in This Version

### Scroll-Scrubbed Canvas
Instead of time-based animation, the canvas frame is tied to scroll position.
Scroll forward → animation progresses. Scroll back → animation reverses.
The template provides `canvas.dataset.progress` (0.0 to 1.0) for each canvas zone.

### Hover Glossary
CSS-only tooltips for jargon terms. Wrap terms in `<span class="glossary-term" data-def="definition">`.
Dotted underline on the term. Tooltip appears on hover (desktop) or focus (mobile).
No JavaScript. No clicks. Pure CSS `::after` pseudo-element.

### Dynamic Time Remaining
The top bar shows "~X min left" based on scroll depth.
Calculated from total word count ÷ 200 words/min on page load.
Updates in real-time as you scroll. Shows "Done!" at the very end.

### Copy Takeaways
End screen has a "📋 Copy all takeaways" button.
Collects all Key Ideas, Actions (Do/Don't), and Pull Quotes into plain text.
Copies to clipboard. One click. Paste into your notes app.

### Focus Mode Audio (Optional)
🎧 toggle in top bar. Generates brown noise via Web Audio API.
Zero audio files. Zero bytes. Completely opt-in.
Stops cleanly when toggled off. Good for blocking distractions while reading.

### Print Stylesheet
`@media print` strips all UI (top bar, sidebar, canvas, buttons).
Content flows naturally with page breaks between chapters.
Cmd/Ctrl+P gives a clean, formatted document you can save as PDF.

### RTL Support
Set `dir="rtl"` and `lang="ar"` (or `he`, `fa`, `ur`) on the `<html>` tag.
Sidebar mirrors to the right side. Key idea borders mirror. Layout adapts.
All CSS uses logical properties where needed.
