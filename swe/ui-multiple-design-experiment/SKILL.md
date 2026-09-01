---
name: ui-multiple-design-experiment
description: Generate 5 divergent redesigns of an existing interface from code and/or a screenshot. Use this skill whenever the user wants to explore multiple UI directions, get design variations, see different takes on the same interface, or says anything like "give me 5 versions", "show me variations", "explore different designs", "redesign this", "what could this look like", or submits a UI screenshot or code and wants options. Always use this skill — it produces a single HTML file with tabbed iframes, one per variation.
---

# UI multiple design experiments

The user has submitted an interface — as code, a screenshot, or both — and wants 5 genuinely divergent redesign versions presented in a single HTML page with tab-switching between iframes.

Your job is to understand what the interface *is*, what it *does*, and who it's *for* — then generate 5 versions that are radically different from each other, not just reskinned.

---

## Step 1: Analyze and Interview

Before generating anything, you must understand context. Do **both** of these:

### A. Analyze the input
If code is provided, read it carefully: what components exist, what data is displayed, what interactions are present, what framework/language is used.

If a screenshot is provided, describe what you see: layout structure, key components, apparent purpose, target user type.

### B. Ask the user 3 questions (ask all at once, inline — no tool needed)

1. **What is this?** — In one sentence, what does this interface do and who uses it? (e.g. "internal analytics dashboard for ops team", "mobile onboarding flow for a fitness app", "multiplayer game lobby")

2. **What's working, what isn't?** — Any parts they want preserved or specifically want to escape from? Any pain points in the current design?

3. **What flavor of variety?** — Point them toward one or more of these axes, or let them say "surprise me":
   - *Structural*: completely different layout paradigms
   - *Density*: from ultra-sparse to information-rich
   - *Interaction*: different interaction models (hover states, keyboard-first, drag, etc.)
   - *Aesthetic*: wildly different visual languages
   - *Audience shift*: same functionality, different target user (consumer vs enterprise, expert vs novice)

Wait for their response before proceeding.

---

## Step 1.5: Research (Optional)

**Only do this if the user asks for it, or if they say something like "surprise me" / "find inspiration" / "I don't know what I want."**

Do NOT do this by default — it adds time and the user may not want it.

If requested, use web search to gather design vocabulary and directional ideas *before* choosing personas. The goal is not to copy anything — it's to absorb the language of what's currently being made in this space and use it to push your personas further.

### What to search for

Tailor queries to the interface type. Examples:
- `site:behance.net [interface type] UI design` — Behance project titles and descriptions often contain rich design language even without seeing images
- `[interface type] dashboard design trends [year]`
- `[interface type] UI redesign case study`
- `dribbble [interface type] interface exploration`

### What to extract

You're looking for *words and concepts*, not images:
- Named aesthetic directions people are using ("bento grid", "glassmorphism", "editorial brutalism", "data ink ratio", "calm technology")
- Structural patterns being explored ("sidebar-less", "command palette first", "card-free", "full-bleed")
- Audience framings ("designed for focus", "built for speed", "feels like a physical object")
- Anything surprising that you wouldn't have thought of on your own

Use `web_fetch` on promising pages to get more than just the snippet — but keep it efficient, 3–5 fetches max.

### What to do with it

Synthesize into a short internal brief (you can share it with the user or not — read the room). Then let it inform your persona choices in Step 2. If you found something genuinely unexpected, name-drop it: "I found people are doing a 'calm technology' direction for this type of tool — I'm making that one of the personas."

---

## Step 2: Design the 5 Personas

Based on the user's answers and your analysis of the interface, **choose 5 named personas** that will anchor each version. These are not just aesthetic labels — each persona is a conceptual position that forces genuinely different structural and interaction decisions.

Personas should be:
- Named evocatively (e.g. "The Command Center", "The Zen Garden", "The Newspaper", "The Terminal", "The Toy")
- Chosen to be **mutually incompatible** — a user of version 1 should look at version 3 and feel like it's a different product
- Appropriate to the *type* of interface (a silly toy persona makes no sense for an ICU monitoring dashboard; a brutalist terminal makes no sense for a children's game)

For each persona, define internally (you don't need to show this to the user, but you must think it through):
- **Layout paradigm**: how is space organized?
- **Interaction model**: how does the user navigate and act?
- **Information density**: sparse / balanced / dense
- **Visual language**: what aesthetic world does this belong to?
- **Motion philosophy**: static / subtle / expressive / physics-based
- **Audience frame**: who does this version implicitly assume is using it?

### Persona Selection Guide by Interface Type

Use this to calibrate which kinds of personas make sense:

**Dashboards / Data tools** → consider: Command Center, The Newspaper, The Spreadsheet Evolved, The Executive Summary, The War Room, The Analyst's Notebook

**Consumer apps / Onboarding** → consider: The Magazine, The Toy, The Conversation, The Poster, The Minimal Card, The Game

**Developer / Internal tools** → consider: The Terminal, The IDE, The Wiki, The Kanban, The API Docs, The Log Stream

**E-commerce / Marketing** → consider: The Lookbook, The Catalog, The Story, The Billboard, The Boutique, The Marketplace

**Games / Entertainment** → consider: The Arcade, The Board Game, The HUD, The Menu Screen, The Storybook, The Loading Screen

**Forms / Flows** → consider: The Interview, The Wizard, The Checklist, The Conversation, The Document, The Kiosk

These are starting points — invent new ones if the interface warrants it.

---

## Step 3: Generate the 5 Versions

Generate each version as a **complete, self-contained HTML file** (inline CSS, inline JS — no external dependencies except CDN-hosted fonts/icons if needed).

### Code Generation Rules

- Each version must be **fully functional** — not a mockup. Buttons should feel clickable, inputs should work, hover states should exist.
- **Populate with realistic fake data** — never use "Lorem ipsum" or "Item 1, Item 2". Use contextually plausible content matching the interface's purpose.
- Each version should use **different fonts, different color systems, different spacing rhythms** — not just the same UI with a color swap.
- **Reuse the user's code logic** where possible (especially JS/data structures), but feel free to completely restructure the markup and styles.
- If the original is in React/Vue/etc and you're generating HTML — that's fine. Translate faithfully.
- Every version must **fill a standard browser viewport** naturally (no tiny widgets floating in a void).

### Divergence Enforcement

Before finalizing each version, check: *if someone saw versions 1 and 2 side by side, would they immediately feel like these are two different design philosophies?* If not, push harder.

Specific anti-patterns to avoid:
- Same nav position across all versions
- Same card/grid pattern with different colors
- Same font pairing style (all serif, or all geometric sans)
- Same interaction model repeated

---

## Step 4: Assemble the Output HTML

Wrap all 5 versions in a **single HTML file** with a tabbed iframe viewer.

### Viewer Spec

```html
<!-- Structure -->
- Fixed top bar with: skill name, interface name/title, 5 tabs
- Each tab shows: persona name + a one-line description of its design philosophy
- One iframe below, switching on tab click
- iframe is full viewport height minus the tab bar
- Smooth tab switching (no flash)
- Active tab clearly indicated
- The tab bar itself should be beautifully designed — not an afterthought
```

### Embedding the Versions

Use `srcdoc` to embed each HTML version directly into its iframe — no separate files needed:

```javascript
const versions = [
  { name: "The Terminal", tagline: "Keyboard-first, monospace, zero decoration", html: `...full html...` },
  // ...
];

function switchTo(index) {
  iframe.srcdoc = versions[index].html;
  // update active tab
}
```

Escape the inner HTML strings properly (backtick template literals work; watch for backticks inside the HTML content — escape them as `\``).

### Tab Bar Design

The tab bar should feel like a product in itself:
- Show the persona name large, tagline small
- Use a subtle but beautiful design — think: dark bar with light text, or a clean white bar with a strong accent
- The "currently viewing" state should be obvious
- Include a small label like "UI Multiplier — 5 Variations" on the left

---

## Step 5: Deliver

- Save the output as a `.html` file (e.g. `ui-multiplier-[short-name].html`) and present it
- After presenting, briefly name the 5 personas and their one-line philosophy — let the user know they can ask to:
  - "Push version 3 further in X direction"
  - "Combine the nav from version 1 with the cards from version 4"
  - "Generate 5 more versions with a different persona set"
  - "Export version 2 as a standalone file"

---

## Quality Bar

Before saving, ask yourself:
- [ ] Are all 5 versions genuinely, structurally different — not just reskinned?
- [ ] Does each version feel like it was designed by a different designer with a different worldview?
- [ ] Is every version fully functional (not a static mockup)?
- [ ] Is the tab bar itself well-designed?
- [ ] Did I use real-feeling data, not placeholder text?
- [ ] Would a designer look at this and feel inspired, not embarrassed?

If any answer is no — fix it before delivering.