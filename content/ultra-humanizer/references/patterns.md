# Pattern Backlog for Ultra Humanizer

Candidate slop patterns and example additions not yet folded into SKILL.md.

## New Pattern Categories

### 1. Permission-Granting / Reassurance Endings
AI softens every claim with emotional permission.

- "Teams struggle with alignment. **And that's okay.**"
- "Nobody knows the answer. **Which is fine.**"
- "You don't have to get it right immediately. **That's completely understandable.**"

**Fix:** Delete the permission. The fact stands on its own.

**Example:**
- Before: "Most teams miss deadlines. And that's okay."
- After: "Most teams miss deadlines."

---

### 2. Fake Precision
LLMs love specific-looking numbers that imply false accuracy.

- "$140.55 billion"
- "19.2% CAGR"
- "3.81 mm" when "about 4 mm" is what a human would say
- "12 to 16 place settings" when "about a dozen" is fine

**Fix:** Round to human precision or delete the number if it is invented.

**Example:**
- Before: "The market will reach $140.55 billion by 2029, growing at 19.2% CAGR."
- After: "The market could reach roughly $140 billion by 2029."

---

### 3. Expletive Openings
"There is/are" and "It is [adjective] that" waste words before the subject.

- "**There are** three reasons why this works." -> "Three reasons..."
- "**It is clear that** the policy failed." -> "The policy failed."
- "**The fact that** we shipped late matters." -> "We shipped late. That matters."

**Example:**
- Before: "There are several factors that contribute to the delay."
- After: "Several factors caused the delay."

---

### 4. Future-Perfect Promises
AI hedges forward with fake momentum.

- "is poised to revolutionize"
- "is set to transform"
- "will continue to drive innovation"
- "is expected to disrupt"

**Fix:** Say what it does now, or admit uncertainty.

**Example:**
- Before: "The platform is poised to revolutionize how teams collaborate."
- After: "The platform lets teams share files in real time."

---

### 5. Weak Capability Statements
Hiding the agent behind "designed to," "aims to," "allows users to."

- "The app **is designed to** help users track habits." -> "The app tracks habits."
- "This feature **allows users to** export data." -> "You can export data."
- "The tool **enables teams to** collaborate." -> "Teams use it to collaborate."

**Example:**
- Before: "The dashboard is designed to provide actionable insights."
- After: "The dashboard shows which pages lose users."

---

### 6. Press-Release Emotion
"We are thrilled / delighted / excited / proud to announce..."

**Fix:** State the news. The emotion is implied or irrelevant.

**Example:**
- Before: "We are thrilled to announce the launch of our new feature."
- After: "We launched the new feature today."

---

### 7. Fake Personalization
"As a [role] myself" and "As someone who has worked in [field]..."

- "As a writer myself, I understand the challenges of drafting."
- "As someone who has led teams, I know how hard this is."

**Fix:** Just make the point. The fake credential adds nothing.

**Example:**
- Before: "As a developer myself, I know debugging is frustrating."
- After: "Debugging is frustrating."

---

### 8. Pseudo-Scenarios
"Picture this," "Imagine a world where," "Consider the following scenario."

**Fix:** State the example directly.

**Example:**
- Before: "Imagine a world where your code deploys itself."
- After: "The tool deploys code automatically."

---

### 9. Intensifiers Without Numbers
"significantly," "dramatically," "substantially," "exponentially" with no metric.

**Fix:** Give the number or delete.

**Example:**
- Before: "The change dramatically improved performance."
- After: "Latency dropped from 200 ms to 40 ms."

---

### 10. Historical Framing Cliches
"Gone are the days," "In the age of," "With the advent of."

- "Gone are the days when teams worked in silos."
- "In the age of AI, every company is a tech company."
- "With the advent of cloud computing, everything changed."

**Fix:** Say the actual change.

**Example:**
- Before: "In the age of remote work, office culture has changed forever."
- After: "Remote work killed the daily commute for a lot of people."

---

### 11. Dead Metaphors and Corporate Cliches
- "double-edged sword"
- "tip of the iceberg"
- "perfect storm"
- "low-hanging fruit"
- "move the needle"
- "circle back"
- "at the end of the day"
- "the bottom line is"
- "low-hanging fruit"

**Fix:** Replace with the literal claim.

**Example:**
- Before: "The new policy is a double-edged sword."
- After: "The policy helps retention but hurts hiring speed."

---

### 12. Abstract Noun Subjects
"The analysis reveals," "This finding suggests," "The report highlights."

**Fix:** Name the people who did the thing.

**Example:**
- Before: "The analysis reveals a significant decline in engagement."
- After: "We found engagement dropped 30% last quarter."

---

### 13. Not-All-X Hedging
"Not all X are Y, but..."

**Fix:** Make the specific claim.

**Example:**
- Before: "Not all startups fail, but many struggle with product-market fit."
- After: "Startups often struggle with product-market fit."

---

### 14. Overused Contrastive Pairings
"Both X and Y," "Not only X but also Y."

**Fix:** State plainly.

**Example:**
- Before: "The tool is not only fast but also reliable."
- After: "The tool is fast and reliable."

---

## Example Additions for Existing Categories

### AI Vocabulary Clusters
Add: unpack, surface (verb), orbit, ladder, gradient, vector, orthogonal (metaphorical), tapestry, delve, landscape.

**Example:**
- Before: "Let's unpack the key drivers behind this shift."
- After: "Here's what changed."

---

### Rule of Three
Add alliterative tricolon.

**Example:**
- Before: "fast, flexible, and future-proof"
- After: "fast and flexible"

---

### Filler / Hedging
Add:
- "Needless to say..." -> delete
- "It goes without saying..." -> delete
- "To be perfectly honest..." -> cut to the honest part
- "In my humble opinion..." -> cut

**Example:**
- Before: "Needless to say, the deadline was missed."
- After: "The deadline was missed."

---

### Formulaic Structures
Add "Challenges and Legacy" section opener.

**Example:**
- Before: "Challenges and Legacy: Korattur faces several challenges typical of urban areas."
- After: "Traffic congestion increased after 2015 when three new IT parks opened."

---

### Structural Tells
Add:
- Numbered headings that are really a forced outline
- Every paragraph ending with a takeaway sentence
- Identical paragraph length across the whole doc

**Example:**
- Before: Three paragraphs of exactly 40 words each.
- After: Vary paragraph length deliberately.

---

### Chatbot Artifacts
Add:
- "Want me to..."
- "Should I continue?"
- "Would you like examples?"

**Example:**
- Before: "Want me to walk you through the setup?"
- After: "Here's how to set it up."

---

### Sycophancy
Add:
- "I'm glad you asked."
- "I'd be happy to."
- "Absolutely, you're spot on."

**Example:**
- Before: "I'm glad you asked. I'd be happy to explain."
- After: "Here's the explanation."

---

### Knowledge-Cutoff Disclaimers
Add:
- "not extensively documented in readily available sources"
- "maintains a relatively private personal life"

**Example:**
- Before: "Details about his family are not extensively documented in readily available sources."
- After: "His family is not mentioned in the sources I have."

---

### Spatial Copulas / False Agency
Add:
- "The library stands as a beacon of knowledge."
- "The program acts as a bridge between communities."

**Example:**
- Before: "The library stands as a beacon of knowledge in the community."
- After: "The library has the best local history collection in the neighborhood."

---


---

## Batch 2 — Additional Candidate Patterns

### 15. The "Whether You're A... Or A..." Hook
Opening by dividing readers into two neat, contrasting categories.

- Before: "Whether you're a seasoned system administrator or a curious hobbyist just starting your journey, Linux has something to offer."
- After: "Linux is difficult to learn, but it gives you total control over your hardware."

---

### 16. The Double-Adjective Noun Sandwich
Flanking a noun with two redundant positive adjectives.

- Before: "We provide a seamless and intuitive user experience."
- After: "The app is easy to use."

---

### 17. The "From X to Y" False Spectrum
Listing unrelated endpoints to sound comprehensive.

- Before: "The tool handles everything from simple data entry to complex machine learning algorithms."
- After: "You can use it to log spreadsheets or train models."

---

### 18. The "At Its Core, [X] Is About..." Existential Crutch
Defining a practical thing by its supposed spiritual essence.

- Before: "At its core, project management is not about spreadsheets; it's about fostering human connection and alignment."
- After: "Project management is about making sure people ship their work on time."

---

### 19. The Passive Rhetorical Question Hand-Off
Asking a question as a transition because the writer can't link ideas.

- Before: "Automating your tests saves time. But how do we actually implement this without breaking our existing pipeline?"
- After: "To automate your tests without breaking the pipeline, start with a staging environment."

---

### 20. "Not Only... But Also" Over-Inflation
Using emphatic structure for incredibly minor points.

- Before: "Not only does the app allow you to save files, but it also lets you rename them."
- After: "You can save and rename files in the app."

---

### 21. High-School Metaphor Overdrive
Grand theatrical metaphors for boring processes.

- Before: "The frontend and backend perform a delicate dance, orchestrating a symphony of data retrieval."
- After: "The frontend requests data from the API and renders it."

---

### 22. The Adverbial Safety Net
Starting or ending paragraphs with summarizing adverbs.

- Before: "Ultimately, the success of your startup depends on finding product-market fit."
- After: "Your startup will fail if nobody wants what you're building."

---

### 23. The "Equipped With" / "Armed With" Passive Lead
Passive participles describing tools or knowledge.

- Before: "Armed with this data, marketing teams can craft highly targeted campaigns."
- After: "Marketing teams use this data to target their ads."

---

### 24. "No Surprise" / "Safe To Say" Hedges
Prefacing platitudes with obviousness markers.

- Before: "In today's fast-paced world, it's no surprise that stress levels are on the rise."
- After: "Stress levels are rising." (Or show a stat and cut the sentence.)

---

### 25. The Double-Noun Compound Verb
Replacing crisp verbs with noun-based corporate phrases.

- Before: "We help companies undergo digital transformations to drive operational efficiency."
- After: "We help companies upgrade their software so they can work faster."

---

### 26. The Title-Case, Colon, Short Explanation Bullet List
Rigid uniform bullet structure.

- Before:
  - **Security:** Features a robust system to keep your data secure.
  - **Speed:** Optimizes performance to ensure lightning-fast speeds.
- After:
  - It uses end-to-end encryption for all user data.
  - Pages load in under 200ms.

---

### 27. "Not Just [Literal], But [Grandiose]" Contrast
Elevating a simple product to an abstract philosophy.

- Before: "This is not just a keyboard; it's an extension of your creative mind."
- After: "This keyboard has mechanical switches and a split layout to reduce wrist strain."

---

### 28. The "Furthermore, Moreover, Additionally" Transition Stack
Overusing formal conjunctive adverbs.

- Before: "Furthermore, the system offers automatic backups. Moreover, it encrypts them."
- After: "The system also backs up your files automatically and encrypts them."

---

### 29. The Fast-Paced / Ever-Changing / Rapidly Evolving Trifecta
Opening by reminding the reader that things change quickly.

- Before: "In today's fast-paced digital landscape, businesses must adapt quickly to survive."
- After: "If businesses don't update their software, they lose customers to faster competitors."

---

## Batch 3 — Psychological / Structural AI Habits

### 30. The "Everything Has a Lesson" Impulse
Turning observations into morals.

- Before: "The failed launch highlights the importance of stakeholder alignment."
- After: "The launch failed because nobody checked whether the data matched production."

---

### 31. Constant Interpretation Instead of Observation
AI explains; humans report.

- Before: "His hesitation reflected deeper uncertainty about the project's direction."
- After: "He paused for a few seconds before answering."

---

### 32. Narrative Closure Addiction
AI hates ending on ambiguity.

- Before: "While challenges remain, the experience ultimately demonstrates the power of resilience."
- After: "The project shipped. Some people still think it was a mistake."

---

### 33. Universalizing
One example becomes a statement about society.

- Before: "This trend reflects broader shifts in how modern consumers engage with technology."
- After: "People used the app more after they added notifications."

---

### 34. Excessive Coherence
Paragraphs connect suspiciously smoothly. Real writing jumps tracks.

- Before: Three paragraphs each beginning with a neat transition and building logically.
- After: Let one paragraph veer into a related tangent or restart the thought.

---

### 35. Generic Emotional Vocabulary
AI names emotions from a distance.

- Before: "She was frustrated."
- After: "She deleted the draft and started over."

---

### 36. Fake Specificity
Looks concrete, says nothing.

- Before: "Organizations across industries are adapting to changing market dynamics."
- After: "Three companies we talked to changed their pricing last quarter."

---

### 37. Retrospective Certainty
AI writes causes as obvious.

- Before: "The decision ultimately led to the company's decline."
- After: "People inside the company still argue about whether that decision hurt them."

---

### 38. Metadata Leakage
The text discusses its own significance.

- Before: "This highlights the need for better communication."
- After: "We need to talk more."

---

### 39. Uniform Confidence
Every statement has the same certainty level.

- Before: All sentences are flat, declarative, and equally certain.
- After: Mix "I know this happened," "I think this mattered," and "Maybe I'm wrong, but..."

---

### 40. Synthetic Fairness
AI compulsively gives equal airtime.

- Before: "There are valid arguments on both sides."
- After: "Most people in the room thought it was a bad idea."

---

### 41. Meaning Inflation
Tiny facts become significant moments.

- Before: "The bakery's opening marks a significant moment in the neighborhood's ongoing evolution."
- After: "A bakery opened."

---

## Notes on What NOT to Add

- Legal / contract phrases ("pursuant to," "hereinafter") — domain-appropriate
- Single common transitions ("however," "therefore") — only clusters are slop
- Technical jargon used correctly — do not flatten expertise
- Profanity / slang used naturally — preserve human voice

---

## Messiness Techniques — How to Break Structural Niceness

AI text feels "too polished" because it is statistically optimized: even rhythm, balanced paragraphs, uniform confidence, smooth transitions, symmetrical structures, and a neat arc. Human writing is lumpy. Below are concrete ways to introduce healthy lumps.

### 1. Rhythm: Break the Metronome

**Too polished:**
> The project started in March. The team worked hard. They shipped in June. Users liked it.

**Messy:**
> The project started in March — which, looking back, feels like forever ago. The team worked hard. Really hard. They shipped in June, and users actually liked it.

**Techniques:**
- Follow a 25-word sentence with a 4-word sentence. Then follow a 6-word sentence with a 30-word one.
- Use fragments for emphasis.
- Let a sentence trail off with "..." once.
- Use a one-word paragraph.

---

### 2. Structure: Kill the Outline Shape

**Too polished:**
> There are three reasons this works. First, it is fast. Second, it is reliable. Third, it is cheap.

**Messy:**
> It works because it is fast. Also reliable, which matters more than you'd think. And cheap — though cheap is the part I keep worrying about.

**Techniques:**
- Don't announce your structure.
- Let one point be longer than the others.
- Drop a point mid-list and come back to it later.
- Start in the middle, not with context.

---

### 3. Certainty: Vary the Confidence

**Too polished:**
> The new policy will improve retention. It will reduce churn. It will increase satisfaction.

**Messy:**
> The new policy might improve retention. It probably reduces churn. Whether it increases satisfaction? I have no idea.

**Techniques:**
- Mix "I know," "I think," and "maybe I'm wrong, but..."
- Admit uncertainty where you genuinely have it.
- Use "probably," "maybe," "I guess" in casual contexts.

---

### 4. Specificity: Drop a Weird Detail

**Too polished:**
> The office was noisy and distracting.

**Messy:**
> The office was loud. Somebody two desks away was always eating carrots.

**Techniques:**
- Replace one abstract noun with a concrete, specific image.
- Include a detail that doesn't strictly advance the argument.
- Name names. Give dates. Use exact numbers when real.

---

### 5. Register: Mix High and Low

**Too polished:**
> The implementation demonstrates a robust approach to error handling.

**Messy:**
> The error handling is robust — which is good, because the previous version fell over if you looked at it wrong.

**Techniques:**
- Use contractions in some sentences, not all.
- Drop a casual phrase into formal text.
- Use slang or an idiom, then revert.

---

### 6. Connection: Let Transitions Be Imperfect

**Too polished:**
> Speed matters. Therefore, caching is important. Additionally, it reduces costs.

**Messy:**
> Speed matters. Caching helps. It also costs less, if you do it right.

**Techniques:**
- Start a sentence with And, But, So, Because, Or.
- Delete transition words entirely.
- Let one paragraph barely connect to the next.
- Add an aside that interrupts the flow.

---

### 7. Closure: Don't Wrap Everything Up

**Too polished:**
> In conclusion, the tool is useful, reliable, and worth adopting.

**Messy:**
> The tool is useful. Whether it's worth adopting depends on whether your team will actually maintain it.

**Techniques:**
- End on a question.
- End on an unresolved tension.
- End with a detail that doesn't summarize.
- Admit the conclusion is provisional.

---

### 8. Self-Correction and Asides

**Too polished:**
> The meeting was productive and aligned the team.

**Messy:**
> The meeting was productive — or at least it felt productive, which might be the same thing at 9 a.m.

**Techniques:**
- Insert a parenthetical that questions or clarifies.
- Say "actually" and change direction.
- Use "I keep wanting to say X, but Y."
- Add a small confession.

---

### 9. Repetition and Parallelism Breaks

**Too polished:**
> The app is fast. The app is reliable. The app is secure.

**Messy:**
> The app is fast. Reliable too. Security is the part they keep patching.

**Techniques:**
- Break parallel structure intentionally.
- Repeat a word on purpose.
- Let one item in a list be a different grammatical form.

---

### 10. Imperfect Opening and Closing

**Too polished:**
> In this article, we will explore the benefits of automated testing.

**Messy:**
> I used to hate automated testing. Then a bug cost us a weekend.

**Techniques:**
- Start with a story, complaint, question, or hot take.
- Skip the roadmap sentence.
- End with the thing you actually care about, not a summary.
