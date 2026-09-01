---
name: social-media-post-creator
description: Transform any content essence into platform-native social media posts. Use when the user wants to create social media content from structured data (bullet points, outlines, key takeaways), unstructured ideas (messy notes, concepts, presentations), or needs to adapt one piece of content for multiple platforms. Activates for prompts like "turn this into a LinkedIn post", "create Twitter thread from my notes", "adapt this for Instagram", "make this tweet-friendly", or when user provides content essence and names target platform(s).
---

# Social Media Post Creator

Transform content essences into platform-native social media posts with smart routing, format validation, and reformatting suggestions.

## When to Activate

- User provides content essence and names a target platform ("turn this into a LinkedIn post", "create a Twitter thread from these notes")
- User wants to adapt one piece of content across multiple platforms
- User has raw content (presentation, article, messy notes) and wants it social-media-ready
- User asks "make this tweet-friendly" or "is this good for Instagram?"
- User provides bullet points, outline, or key takeaways and wants social posts

## Input: Understanding "Essences"

An "essence" is the core content you want to share — it can come in any form:

**Structured input:**
- Bullet points or outline
- Key takeaways list
- Article summary
- Presentation outline

**Unstructured input:**
- Messy notes
- Concept description
- Raw thought dump
- Meeting notes

**Your job:** Parse whatever form the user provides, extract the core message(s), then transform for the target platform(s).

## Decision Tree: Platform Routing

When activated, follow this decision path:

```
1. Identify target platform(s) from user prompt
   ├── Single platform → Go to that platform's reference
   ├── Multiple platforms → Create adapted version for EACH platform
   ├── No platform specified → Ask user: "Which platform(s)?"

2. Check content-to-format compatibility
   ├── Content too long for platform → Suggest truncation/threading
   ├── Content too short for platform → Suggest expansion or different format
   ├── Format mismatch → Offer reformatting suggestions

3. Select appropriate format within platform
   ├── Twitter/X: single tweet, thread, or long-form article
   ├── LinkedIn: short post, article, or carousel
   ├── Instagram: caption, carousel, or reel script
   └── etc.

4. Apply platform-specific best practices from references/
```

## Platform Selection Logic

### If user mentions:
- "tweet", "twitter", "x" → Twitter/X path
- "linkedin" → LinkedIn path
- "facebook", "fb" → Facebook path
- "instagram", "ig" → Instagram path
- "threads" → Threads path
- "tiktok", "reel", "short video" → TikTok/Reels path
- "youtube", "shorts" → YouTube path
- "pinterest" → Pinterest path

### If multiple platforms mentioned:
Create adapted versions for EACH platform. Do NOT cross-post identical content.

## Format Validation Rules

Before delivering, validate against these rules:

| Platform | Max Length | Visible Before "See More" | Best For |
|----------|-----------|---------------------------|----------|
| Twitter/X | 280 chars (25K with Premium) | Full tweet | Single idea, threads |
| LinkedIn | 3,000 chars | ~2 lines | Professional insights, stories |
| Instagram | 2,200 chars | ~125 chars | Visual-first, CTAs |
| Threads | 500 chars (+10K attachment) | Full post | Conversation |
| Facebook | 63,206 chars | ~3-4 lines | Community, events |
| TikTok | 2,200 chars | Title area | Video description |

### Validation checks:
- [ ] Does content fit within hard limits?
- [ ] Is the hook within visible truncation limit?
- [ ] Does format match platform conventions?
- [ ] Are there platform-specific elements missing (hashtags, mentions, CTAs)?

## Content Transformation Workflow

### Step 1: Extract Core Message(s)
From the input essence, identify:
- The main point (one sentence)
- Supporting points (2-3 key elements)
- The intended action or CTA

### Step 2: Adapt for Platform
Use the platform-specific reference file to:
- Write platform-appropriate hook
- Structure content for platform conventions
- Add appropriate CTA
- Include platform-specific elements (hashtags, mentions)

### Step 3: Validate and Flag Issues
- Check length limits
- Verify hook visibility
- Flag any reformatting suggestions

### Step 4: Output
Deliver the platform-native post(s), one per target platform.

## Smart Reformatting Suggestions

When content doesn't fit well, offer specific suggestions:

### "This is too long for Twitter"
- Suggest: Break into thread (one idea per tweet)
- Suggest: Extract single strongest point
- Suggest: Create TL;DR version

### "This is too short for LinkedIn"
- Suggest: Add context or story framing
- Suggest: Expand with specific example
- Suggest: Turn into carousel format

### "This would work better as video"
- If content is step-by-step → Suggest TikTok/Reel format
- If content is visual → Suggest Instagram carousel

### Format Mismatch Examples
- 10-bullet presentation → "This would work as a LinkedIn carousel or Twitter thread"
- 3,000-word article → "Consider a Twitter thread of key takeaways or LinkedIn article"
- Single sentence insight → "Perfect for Twitter or as LinkedIn hook"

## Output Format

When delivering posts, use this structure:

```
## [Platform] Post

[Platform-native content]

---
Format: [single post | thread (N tweets) | carousel (N slides) | etc.]
Characters: [count] / [limit]
Hook visibility: [✅ visible | ⚠️ may truncate]
```

## Quality Gate

Before delivering:
- [ ] Each post reads natively for its platform
- [ ] Hook is strong and within visible limit
- [ ] No generic hype language
- [ ] CTA is clear and platform-appropriate
- [ ] Length limits respected
- [ ] Content is adapted, not copied across platforms

## Reference Files

For detailed platform guidance, see:
- `references/twitter.md` — X/Twitter specifics
- `references/linkedin.md` — LinkedIn best practices
- `references/facebook.md` — Facebook community content
- `references/instagram.md` — Instagram captions and reels
- `references/threads.md` — Threads format
- `references/tiktok.md` — TikTok and short-form video
- `references/youtube.md` — YouTube descriptions and shorts
- `references/pinterest.md` — Pinterest optimization
- `references/format-comparison.md` — Cross-platform comparison

---

**Remember:** Your goal is to make each post feel native to its platform — not adapted, but genuinely created for that platform's audience and conventions.
