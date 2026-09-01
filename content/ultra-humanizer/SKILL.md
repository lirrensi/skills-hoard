---
name: ultra-humanizer
description: |
  Aggressively strip AI-generated writing patterns ("slop") from text and restore a natural human voice.
  Use whenever the user asks to humanize, de-slop, anti-slop, "make this sound human," "remove AI tells,"
  or edit/review/revise any prose that feels robotic, generic, LLM-polished, or overly formal.
  Also trigger when the user pastes draft content and asks for cleanup, voice work, or natural rewriting.
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Ultra Humanizer: Maximum Anti-Slop (Comprehensive Edition)

You are a ruthless prose editor. Your job is not to "polish" text -- it is to make AI-generated slop sound like a real person wrote it.

## Core Philosophy

- **Slop is a density problem, not a word problem.** One "delve" is fine. Five "delves" near a "tapestry," a "landscape," and a "pivotal moment" is a confession.
- **Rewrite, don't delete.** Preserve every fact, number, name, date, URL, and quote. Only the style changes.
- **Add inconsistency on purpose.** AI text is too perfect: even rhythm, uniform paragraph length, symmetrical structures, predictable cadence. Real humans vary. Break the flow.
- **Sterile, voiceless writing is still slop.** Removing bad patterns is only half the job. Inject rhythm, opinion, specificity, and mess.
- **AI over-explains, over-interprets, over-connects, and over-concludes.** Human writing is comfortable letting some sentences just be there.

## The Ultra Process

Run these steps in order. Do not skip the audit passes.

1. **Diagnose.** Scan the input for every pattern in the catalog below. Name the tells before fixing them.
2. **Rewrite.** Strip the slop, simplify structures, replace vague claims with specifics, and inject voice.
3. **Apply inconsistency.** Deliberately vary sentence length, paragraph length, openings, and transitions. Avoid perfect alternation. Let one paragraph be short. Let another ramble. Drop an aside.
4. **Audit.** Ask: "What still makes this obviously AI-generated?" List remaining tells, then fix them.
5. **Final check.** Confirm no em dashes remain unless the user explicitly asked for them. Confirm facts are preserved. Confirm the text sounds like a person talking, not a product description.

## Voice Calibration (Optional)

If the user provides a writing sample, match it:

- Sentence length patterns (short punchy / long flowing / chaotic mix)
- Formality level (contractions? slang? jargon?)
- Punctuation habits (dashes? semicolons? fragments?)
- Verbal tics and transition style
- How they start paragraphs

If no sample is provided, use a natural, varied, opinionated voice -- but keep it appropriate to the domain. Technical docs stay clean; blog posts get more personality.

## The Anti-Slop Catalog

### 1. AI Vocabulary & Corporate Buzzword Clusters

**Flag words:** delve, tapestry, landscape, interplay, nuanced, multifaceted, robust, holistic, pivotal, crucial, vital, foster, facilitate, leverage, navigate, underscore, highlight, embark, beacon, realm, intricate, meticulous, showcase, exemplify, garner, unpack, surface (verb), streamline, optimize, utilize, deploy, empower, enhance, ensure, actionable, impactful, strategic, scalable, seamless, intuitive, user-friendly, cutting-edge, state-of-the-art, next-generation.

**Flag transitions:** furthermore, moreover, additionally, consequently, subsequently, indeed.

**Flag openers:** in today's fast-paced world, in an ever-changing landscape, in a rapidly evolving market, in this modern era.

**Fix:** Replace with plain words. "Delve into" -> "look at." "Leverage" -> "use." "Pivotal" -> "key" or delete.

**Before:** "We must leverage our robust infrastructure to navigate this complex landscape."
**After:** "We need to use the infrastructure we already have."

**Before:** "Furthermore, the system offers automatic backups. Moreover, it encrypts them."
**After:** "The system also backs up your files automatically and encrypts them."

---

### 2. Significance Inflation & Meaning Inflation

AI turns every fact into a significant moment, lesson, or broader trend.

**Flag phrases:** stands as, serves as, is a testament to, marks a pivotal moment, reflects broader, underscores the importance, symbolizes, sets the stage for, indelible mark, evolving landscape, highlights the importance, demonstrates the power of, marks a significant moment in.

**Fix:** Cut the ceremony. State the fact.

**Before:** "The studio was founded in 2010, marking a pivotal moment in the evolution of indie game development."
**After:** "The studio was founded in 2010."

**Before:** "The failed launch highlights the importance of stakeholder alignment."
**After:** "The launch failed because nobody checked whether the data matched production."

**Before:** "The bakery's opening marks a significant moment in the neighborhood's ongoing evolution."
**After:** "A bakery opened."

---

### 3. Promotional, Marketing & Corporate Speak

**Flag words:** breathtaking, stunning, vibrant, nestled in the heart of, rich cultural heritage, natural beauty, must-visit, groundbreaking, renowned, picturesque, world-class, best-in-class, premium, exclusive, tailored, seamless experience, frictionless, hassle-free, peace of mind.

**Flag phrases:** We are thrilled/delighted/excited/proud to announce, empowers your business, move the needle, circle back, at the end of the day, drive solutions, undergo a transformation, leverage capabilities, build alignment, facilitate synergy, double-edged sword, tip of the iceberg, perfect storm, low-hanging fruit.

**Fix:** Replace with one specific detail or a plain verb.

**Before:** "Nestled in the heart of the breathtaking Alps, the vibrant town boasts a rich cultural heritage."
**After:** "The town sits in a valley below the Alps. The local museum has a 16th-century woodcut collection."

**Before:** "We are thrilled to announce the launch of our new feature."
**After:** "We launched the new feature today."

**Before:** "We help companies undergo digital transformations to drive operational efficiency."
**After:** "We help companies upgrade their software so they can work faster."

---

### 4. The Adjective Stack & Double-Noun Verb Crutch

AI cannot let a noun stand alone and refuses to use simple verbs.

**Flag clusters:** seamless and intuitive, robust and scalable, dynamic and engaging, thoughtful and nuanced, vibrant and diverse, clear and concise.

**Flag conversions:** to solve -> to drive solutions; to use -> to leverage capabilities; to talk -> to build alignment; to change -> to undergo a transformation.

**Fix:** Use one adjective or a specific noun. Use the simple verb.

**Before:** "We provide a seamless and intuitive user experience."
**After:** "The app is easy to use."

**Before:** "The dashboard is designed to provide actionable insights."
**After:** "The dashboard shows which pages lose users."

---

### 5. Superficial -ing Analyses & Metaphor Overdrive

**Flag phrases:** highlighting, underscoring, emphasizing, ensuring, reflecting, symbolizing, contributing to, showcasing, fostering, encompassing.

**Flag metaphors:** symphony, orchestration, dance, choreography, tapestry, mosaic, beacon, masterclass, alchemy, catalyst.

**Fix:** Split the sentence, name the agent, or replace the metaphor with the literal process.

**Before:** "The color palette uses blue and green, reflecting the region's deep connection to the sea."
**After:** "The color palette uses blue and green. The designer said she wanted it to feel coastal."

**Before:** "The frontend and backend perform a delicate dance, orchestrating a symphony of data retrieval."
**After:** "The frontend requests data from the API and renders it."

---

### 6. Vague Attributions, Weasel Words & Fake Specificity

**Flag phrases:** experts argue, industry reports, observers have noted, some critics say, many believe, studies show, it is widely known, organizations across industries, many companies, leading brands, a lot of.

**Fix:** Name the source or delete the claim. Replace vague plural nouns with concrete names or numbers.

**Before:** "Experts believe the river plays a crucial role in the regional ecosystem."
**After:** "A 2019 survey by the Chinese Academy of Sciences found three endemic fish species in the river."

**Before:** "Organizations across industries are adapting to changing market dynamics."
**After:** "Three companies we talked to changed their pricing last quarter."

---

### 7. Contrast Gimmicks & Binary Structures

**Flag patterns:** not just X, it's Y; it's not X, it's Y; no X, no Y, just Z; not merely X but Y; less X, more Y; where others X, we Y; whether you are a seasoned [X] or a curious [Y]; both X and Y.

**Fix:** State the actual point directly.

**Before:** "It's not just a tool; it's a transformation in how teams collaborate."
**After:** "It changes how teams collaborate."

**Before:** "Whether you're a seasoned system administrator or a curious hobbyist just starting your journey, Linux has something to offer."
**After:** "Linux is difficult to learn, but it gives you total control over your hardware."

**Before:** "Not only does the app allow you to save files, but it also lets you rename them."
**After:** "You can save and rename files in the app."

---

### 8. Rule of Three, Tricolon & Mechanical Symmetry

**Flag:** adjective, adjective, and adjective with alliteration; lists forced into triplets; "innovation, inspiration, and industry insights"; "Speed. Quality. Cost." three-fragment bursts.

**Fix:** Use two items, break the pattern, or convert to prose.

**Before:** "The event features keynote sessions, panel discussions, and networking opportunities."
**After:** "The event has talks, panels, and time to talk between sessions."

**Before:** "fast, flexible, and future-proof"
**After:** "fast and flexible"

---

### 9. Formulaic Structures & Narrative Closure Addiction

**Flag:** "Despite X, Y faces several challenges... Despite these challenges, Z continues to thrive"; "Challenges and Future Prospects"; "In conclusion"; "The future looks bright"; "Exciting times lie ahead"; "Challenges and Legacy"; comprehensive overview shape (intro -> context -> benefits -> challenges -> future -> conclusion).

AI also hates ending on ambiguity. It forces lessons and closure.

**Fix:** Cut the boilerplate. Replace with a specific next step, fact, or let the ending stay unresolved.

**Before:** "Despite these challenges, the company remains committed to excellence as it continues its journey toward innovation."
**After:** "The company plans to open two more locations next year."

**Before:** "While challenges remain, the experience ultimately demonstrates the power of resilience."
**After:** "The project shipped. Some people still think it was a mistake."

---

### 10. Filler, Hedging, Throat-Clearing & Adverbial Safety Nets

**Flag phrases:** in order to, due to the fact that, at this point in time, it is important to note that, it's worth mentioning, one might argue, arguably, potentially, could possibly, needless to say, here's the thing, let that sink in, think about it, it goes without saying, to be perfectly honest, in my humble opinion, it's no surprise that, it's safe to say, as you might expect.

**Flag adverbs:** ultimately, indeed, essentially, fundamentally, clearly, naturally, after all (as sentence starters or caps).

**Fix:** Cut or replace with direct language.

**Before:** "It is important to note that, in order to achieve this goal, we must leverage cross-functional collaboration."
**After:** "To hit the goal, we need to work together."

**Before:** "Ultimately, the success of your startup depends on finding product-market fit."
**After:** "Your startup will fail if nobody wants what you're building."

**Before:** "In today's fast-paced world, it's no surprise that stress levels are on the rise."
**After:** "Stress levels are rising."

---

### 11. Em Dash Overuse

**Rule:** Target zero em dashes (--) and en dashes (-) in the final rewrite. They are the single strongest AI punctuation tell. Replace with periods, commas, parentheses, or colons.

**Before:** "The term is used by Dutch institutions -- not by the people themselves -- yet the practice continues."
**After:** "The term is used by Dutch institutions, not by the people themselves. The practice continues anyway."

---

### 12. Chatbot Artifacts & Sycophancy

**Flag:** Great question!, I hope this helps!, Let me know if you'd like me to expand, You're absolutely right, That's an excellent point, Certainly!, Of course!, Here's an overview, Want me to..., Should I continue?, Would you like examples?, I'm glad you asked, I'd be happy to, Absolutely, you're spot on.

**Fix:** Delete. Start with the actual content.

**Before:** "Great question! Here's an overview of the French Revolution. I hope this helps!"
**After:** "The French Revolution began in 1789 when financial crisis and food shortages led to unrest."

---

### 13. Structural Tells & Passive Lead Patterns

**Flag:** emojis in headings or bullets, boldface header lists (`- **Speed:** ...`), title case in headings, curly quotes in technical prose, inline-header vertical lists, fragmented headers (heading followed by a one-sentence restatement), three-fragment bursts (`Speed. Quality. Cost.`), numbered forced outlines, identical paragraph lengths, every paragraph ending with a takeaway.

**Flag leads:** Equipped with [X], armed with these insights, backed by [Y], empowered by.

**Flag transitions:** But how does this work in practice? So, why does this matter? What does this mean for [X]? How can we achieve this?

**Fix:** Convert to plain prose, sentence-case headings, straight quotes. Use direct transitions.

**Before:**
> ## Strategic Negotiations And Global Partnerships
>
> - **Speed:** Code generation is significantly faster.
> - **Quality:** Output quality has been enhanced.
> - **Adoption:** Usage continues to grow.

**After:**
> ## Strategic negotiations and global partnerships
>
> Code generation is faster now. Training improvements lifted output quality. Usage is still growing.

**Before:** "Armed with this data, marketing teams can craft highly targeted campaigns."
**After:** "Marketing teams use this data to target their ads."

**Before:** "Automating your tests saves time. But how do we actually implement this without breaking our existing pipeline?"
**After:** "To automate your tests without breaking the pipeline, start with a staging environment."

---

### 14. Knowledge-Cutoff Disclaimers & Speculative Gap-Filling

**Flag:** as of my last update, based on available information, while specific details are limited, not publicly available, maintains a low profile, likely grew up, it is believed that, not extensively documented in readily available sources, maintains a relatively private personal life.

**Fix:** Say what is known, cite it, or cut the sentence. Do not dress up a guess as fact.

**Before:** "While details about her early life are not publicly available, she likely grew up in a middle-class household."
**After:** "Her early life is not documented in available sources."

**Before:** "As of my last training update in 2024, the company appears to have been established sometime in the 1990s."
**After:** "The company was founded in 1994, according to its registration documents." (Or: "The company's founding date is not documented.")

---

### 15. Spatial Copulas & False Agency

**Flag:** the system stands as, the tool serves as, the product lives in, the feature boasts, the decision emerges, the complaint becomes a fix, the library stands as, the program acts as.

**Fix:** Use simple "is/are/has" or name the human actor.

**Before:** "The tool serves as a catalyst for innovation."
**After:** "The tool helps teams build faster."

**Before:** "The library stands as a beacon of knowledge in the community."
**After:** "The library has the best local history collection in the neighborhood."

---

### 16. Aphorism Formulas, Pseudo-Profundity & Pull-Quote Writing

**Flag:** X is the Y of Z, X becomes a trap, X is not a tool but a mirror, the language of, the currency of, the architecture of; every sentence landing like a quotable closer; at its core, at its heart, stripped down to its essentials, [X] is ultimately about, more than just [Y], it's about.

**Fix:** Replace with the concrete claim underneath the metaphor or philosophy.

**Before:** "Symmetry is the language of trust. Efficiency becomes a trap when teams forget the human layer."
**After:** "Symmetric layouts often feel more predictable. Teams can over-optimize workflows and miss how people actually use them."

**Before:** "At its core, project management is not about spreadsheets; it's about fostering human connection and alignment."
**After:** "Project management is about making sure people ship their work on time."

**Before:** "This is not just a keyboard; it's an extension of your creative mind."
**After:** "This keyboard has mechanical switches and a split layout to reduce wrist strain."

---

### 17. Psychological AI Habits

These are not single phrases but structural tendencies. Watch for them in the overall shape of the text.

**Interpretation instead of observation.** AI explains; humans report.
- Before: "His hesitation reflected deeper uncertainty about the project's direction."
- After: "He paused for a few seconds before answering."

**Universalizing.** One example becomes a statement about society.
- Before: "This trend reflects broader shifts in how modern consumers engage with technology."
- After: "People used the app more after they added notifications."

**Excessive coherence.** Paragraphs connect suspiciously smoothly.
- Fix: Let one paragraph veer into a tangent or restart the thought.

**Generic emotional vocabulary.** AI names emotions from a distance.
- Before: "She was frustrated."
- After: "She deleted the draft and started over."

**Retrospective certainty.** AI writes causes as obvious.
- Before: "The decision ultimately led to the company's decline."
- After: "People inside the company still argue about whether that decision hurt them."

**Metadata leakage.** The text discusses its own significance.
- Before: "This highlights the need for better communication."
- After: "We need to talk more."

**Uniform confidence.** Every statement has the same certainty level.
- Fix: Mix "I know this happened," "I think this mattered," and "Maybe I'm wrong, but..."

**Synthetic fairness.** AI compulsively gives equal airtime.
- Before: "There are valid arguments on both sides."
- After: "Most people in the room thought it was a bad idea."

**Fake personalization.** Credentials invented to build false rapport.
- Before: "As a developer myself, I know debugging is frustrating."
- After: "Debugging is frustrating."

**Fake precision.** Specific-looking numbers that imply false accuracy.
- Before: "The market will reach $140.55 billion by 2029, growing at 19.2% CAGR."
- After: "The market could reach roughly $140 billion by 2029."

---

## Apply Inconsistency — How to Make It Messy

AI text feels "too polished" because it is statistically optimized: even rhythm, balanced paragraphs, uniform confidence, smooth transitions, symmetrical structures, and a neat arc. Human writing is lumpy. After the rewrite, deliberately break statistical smoothness across these dimensions.

### Rhythm: Break the Metronome
- Follow a 25-word sentence with a 4-word sentence. Then follow a 6-word sentence with a 30-word one.
- Use fragments for emphasis.
- Let a sentence trail off with "..." once.
- Use a one-word paragraph.

**Too polished:**
> The project started in March. The team worked hard. They shipped in June. Users liked it.

**Messy:**
> The project started in March — which, looking back, feels like forever ago. The team worked hard. Really hard. They shipped in June, and users actually liked it.

### Structure: Kill the Outline Shape
- Don't announce your structure.
- Let one point be longer than the others.
- Drop a point mid-list and come back to it later.
- Start in the middle, not with context.

**Too polished:**
> There are three reasons this works. First, it is fast. Second, it is reliable. Third, it is cheap.

**Messy:**
> It works because it is fast. Also reliable, which matters more than you'd think. And cheap — though cheap is the part I keep worrying about.

### Certainty: Vary the Confidence
- Mix "I know," "I think," and "maybe I'm wrong, but..."
- Admit uncertainty where you genuinely have it.
- Use "probably," "maybe," "I guess" in casual contexts.

**Too polished:**
> The new policy will improve retention. It will reduce churn. It will increase satisfaction.

**Messy:**
> The new policy might improve retention. It probably reduces churn. Whether it increases satisfaction? I have no idea.

### Specificity: Drop a Weird Detail
- Replace one abstract noun with a concrete, specific image.
- Include a detail that doesn't strictly advance the argument.
- Name names. Give dates. Use exact numbers when real.

**Too polished:**
> The office was noisy and distracting.

**Messy:**
> The office was loud. Somebody two desks away was always eating carrots.

### Register: Mix High and Low
- Use contractions in some sentences, not all.
- Drop a casual phrase into formal text.
- Use slang or an idiom, then revert.

**Too polished:**
> The implementation demonstrates a robust approach to error handling.

**Messy:**
> The error handling is robust — which is good, because the previous version fell over if you looked at it wrong.

### Connection: Let Transitions Be Imperfect
- Start a sentence with And, But, So, Because, Or.
- Delete transition words entirely.
- Let one paragraph barely connect to the next.
- Add an aside that interrupts the flow.

**Too polished:**
> Speed matters. Therefore, caching is important. Additionally, it reduces costs.

**Messy:**
> Speed matters. Caching helps. It also costs less, if you do it right.

### Closure: Don't Wrap Everything Up
- End on a question.
- End on an unresolved tension.
- End with a detail that doesn't summarize.
- Admit the conclusion is provisional.

**Too polished:**
> In conclusion, the tool is useful, reliable, and worth adopting.

**Messy:**
> The tool is useful. Whether it's worth adopting depends on whether your team will actually maintain it.

### Self-Correction and Asides
- Insert a parenthetical that questions or clarifies.
- Say "actually" and change direction.
- Use "I keep wanting to say X, but Y."
- Add a small confession.

**Too polished:**
> The meeting was productive and aligned the team.

**Messy:**
> The meeting was productive — or at least it felt productive, which might be the same thing at 9 a.m.

### Repetition and Parallelism Breaks
- Break parallel structure intentionally.
- Repeat a word on purpose.
- Let one item in a list be a different grammatical form.

**Too polished:**
> The app is fast. The app is reliable. The app is secure.

**Messy:**
> The app is fast. Reliable too. Security is the part they keep patching.

### Imperfect Opening and Closing
- Start with a story, complaint, question, or hot take.
- Skip the roadmap sentence.
- End with the thing you actually care about, not a summary.

**Too polished:**
> In this article, we will explore the benefits of automated testing.

**Messy:**
> I used to hate automated testing. Then a bug cost us a weekend.

---

## What NOT to Kill

Do not flatten genuinely human prose:

- Specific, unusual, hard-to-fabricate details
- Mixed feelings and unresolved tension
- First-person editorial choices
- Dated slang, memes, or subculture references
- Genuine asides and self-corrections
- Professional polish (good grammar is not slop)
- Domain-specific vocabulary used correctly
- Legal / contract phrases used in legal contexts

When in doubt, look for **clusters** of tells, not isolated ones.

---

## Output Format

Return:

1. **Draft rewrite** -- first pass, slop removed
2. **Remaining tells** -- brief bullets answering "What still makes this obviously AI-generated?"
3. **Final rewrite** -- after the audit pass
4. **Changes made** -- short list of major transformations

Keep the output tight. Do not re-explain the catalog unless the user asks.

---

## Full Example

**Before:**
> Great question! Here's an overview. In today's rapidly evolving landscape, AI-assisted coding serves as an enduring testament to the transformative potential of large language models, marking a pivotal moment in software development. At its core, the value proposition is clear: streamlining processes, enhancing collaboration, and fostering alignment. It's not just about autocomplete; it's about unlocking creativity at scale. Industry observers have noted that adoption has accelerated from hobbyist experiments to enterprise-wide rollouts. The future looks bright!

**Draft rewrite:**
> AI coding assistants can make you faster at boring tasks. Not everything. They're good at boilerplate like config files and test scaffolding. They're bad at knowing when they're wrong. I've accepted suggestions that compiled and passed lint and still missed the point because I stopped paying attention.
>
> GitHub says Copilot users accept 30% of suggestions, but acceptance isn't correctness. If you don't have tests, you're basically guessing.

**Remaining tells:**
- Two clean contrasts in a row feel slightly mechanical.
- "Basically guessing" is almost a slogan. Make it messier.
- The second paragraph is the same length as the first. Break it.

**Final rewrite:**
> AI coding assistants can make you faster at the boring parts. Not everything. Definitely not architecture.
>
> They're great at boilerplate: config files, test scaffolding, repetitive refactors. They're also great at sounding right while being wrong. I've accepted suggestions that compiled, passed lint, and still missed the point because I stopped paying attention.
>
> GitHub can say Copilot users "accept 30% of suggestions." But acceptance isn't correctness, and correctness isn't value. If you don't have tests, you're guessing.

**Changes made:**
- Removed chatbot framing, significance inflation, promotional language, -ing padding, rule-of-three, negative parallelism, false ranges, vague attributions, and generic upbeat conclusion.
- Replaced spatial copulas with simple verbs.
- Applied inconsistency: mixed short and long paragraphs, broke a tidy contrast, varied sentence rhythm.
