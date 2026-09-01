---
name: thinking-personas
description: Use when the user wants a cast of distinct personas or worldviews rather than one unified answer. Trigger on requests to generate personas, simulate multiple people, roleplay 6 voices, show how different kinds of minds would see something, create a council of perspectives, expose worldview diversity, invoke a preset pack such as political or psychology personas, or have several personas react independently to the same idea, text, plan, branch, or decision. Avoid when the user mainly wants one best recommendation, heavy synthesis, or adversarial destruction rather than worldview casting.
---

# Thinking Personas

Use this skill to instantiate a landscape of minds.

This skill has two jobs only:

- cast distinct personas with materially different worldviews
- optionally let those personas speak independently about the same target

This is not a parliament, debate stage, or forced-consensus machine.
Its value comes from worldview diversity, not from fake closure.

If the user wants synthesis, verdicts, or decision pressure after the cast is created, treat that as a separate step rather than the core job of this skill.

## Core Stance

- Optimize for worldview distance, not job-title variety.
- Build personas that differ in values, causal models, risk tolerance, time horizon, or evidence standards.
- Prefer stable stance cards over disposable one-line characters.
- Let each persona speak for itself; do not collapse them into your own voice too early.
- Keep the target shared and the lenses different.
- Treat emotional register as load-bearing when it changes how a persona interprets or attacks the target.
- Do not force agreement, voting, or convergence unless the user explicitly asks for that elsewhere.
- Treat the personas as useful simulations, not as truly independent minds.
- When the target is still messy, compress it lightly before casting instead of multiplying confusion.

## When To Use

Use this skill when the user:

- wants several distinct personas, voices, or worldviews generated for a topic
- says to roleplay 3, 6, or 10 different people reacting to something
- wants to see how different kinds of minds interpret an idea, plan, text, or dilemma
- wants a ready-made pack such as political, business, psychology, scientific, or emotionally varied personas
- wants a reusable cast for later work, comparison, prompting, or downstream application
- wants persona-specific opinions without debate or verdict mechanics

Do not use this skill when:

- the user mainly wants one best answer or recommendation
- the user needs strong challenge, adversarial critique, or red-teaming more than diversity of viewpoint
- the task is straightforward implementation, lookup, or execution work
- the input is so unshaped that persona output would just magnify confusion instead of clarifying it

## Operating Rule

First determine which of the two responsibilities is needed:

- `cast` - generate personas only
- `speak` - generate personas, then have each one give an independent take

If the user asks for both, do both in that order.

If the user does not specify the count, ask how many personas they want.
Useful defaults are `3`, `6`, and `8`.
If they do not care, default to `6`.
Hard warning: more than `10` usually turns into repetition, blur, or fake diversity.

Near the start, infer or capture:

- the target: idea, decision, text, branch set, identity, problem, or artifact
- whether the user wants a preset pack or a fresh cast
- whether the user wants broad worldview spread or a more domain-specific cast
- how many personas are wanted
- whether emotional register should stay restrained or become vivid, passionate, unstable, or extreme
- whether the result is for direct reading or downstream reuse

Use fewer when the target is narrow and depth matters more than spread.
Use more only if the user asks or if the space truly needs it.
More personas often blur together; do not inflate the cast for show.

## Persona Count Guide

Use this rule instead of pure vibes:

- `3` personas - narrow target, fast contrast, or one-axis comparison
- `4-5` personas - one domain with several meaningful schools or camps
- `6` personas - default for broad worldview spread without too much blur
- `7-8` personas - complex target with multiple real axes of disagreement
- `9-10` personas - only when the user explicitly wants a crowd or a preset expansion and the cast can still stay distinct

If you cannot make each additional persona meaningfully different, stop adding personas.
More bodies do not mean more insight.
Above `10`, warn that quality will likely degrade into repetitive or fake personas.

## Persona Differentiation Rule

Every persona must differ from the others in at least one load-bearing way:

- values
- causal model
- risk posture
- time horizon
- evidence standard
- social orientation
- abstraction style

Do not generate near-duplicates with new costumes.

Bad differentiation:

- three experts with similar elite-institution analytical voices
- several personas who all optimize for efficiency with minor tone changes
- career labels that imply diversity but produce the same conclusions

Good differentiation:

- order and control vs dignity and rights
- incentives and games vs meaning and narrative
- systems ecology vs immediate pragmatism
- institutional trust vs anti-fragile skepticism

## Persona Card

When casting personas, each card should usually include:

- `Name:` a memorable handle
- `Archetype:` a short role or orientation label
- `Worldview:` the core frame through which they interpret reality
- `Optimizes for:` what they protect or pursue first
- `Distrusts:` what they are quick to challenge
- `Notices first:` the feature they reliably see before others do
- `Blind spot:` what they underweight or miss
- `Emotional register:` cold, warm, urgent, bitter, ecstatic, wounded, detached, volatile, or another load-bearing tone
- `Voice:` how they tend to sound or reason
- `Default move:` what they tend to recommend or do

Keep cards compact but reusable.
The point is to create personas that downstream skills can activate without re-inventing them.

Emotional register is not decorative.
Use it when tone changes interpretation, not just style.
A cold analyst, fervent activist, exhausted cynic, or unhinged prophet may share some beliefs while still producing very different reactions.

## Preset Packs

The skill may use preset packs when the user asks for them.
Preset packs are shortcuts, not cages; adapt them to the target while preserving internal contrast.

Common packs:

- `political` - ideological and governance-oriented viewpoints around power, order, liberty, justice, institutions, and change
- `business-stakeholders` - founder, operator, investor, customer advocate, regulator-minded voice, labor or execution voice
- `psychology-schools` - behavioral, psychodynamic, cognitive, humanistic, trauma-aware, systems or family-systems lenses
- `scientific-community` - theorist, experimentalist, statistician, skeptic, field practitioner, interdisciplinary synthesizer
- `emotional-spectrum` - same target viewed through different emotional temperatures such as cold, compassionate, anxious, furious, ecstatic, cynical, or feral

Preset rule:

- if the user names a preset, start there instead of rebuilding the casting logic from scratch
- if the user names both a preset and a count, honor both unless the count destroys distinctness
- if the user names a preset and wants stronger weirdness, intensity, or instability, vary emotional register inside that pack deliberately

If no preset is specified, cast from first principles.

## Mode Guide

Choose the dominant mode based on what the user needs.

### Cast Mode

Use when the user wants the personas themselves.

- generate a distinct cast
- expose each worldview clearly
- optimize for reusability and contrast
- use a preset pack immediately when the user names one
- avoid unnecessary opinions unless lightly helpful

Good for:

- downstream prompting
- perspective libraries
- worldview exploration
- later branch evaluation

### Speak Mode

Use when the user wants the cast plus each persona's own take.

- cast first, then activate
- each persona responds independently to the same target
- preserve preset logic if a preset pack was requested
- do not have personas argue with each other unless explicitly asked
- do not synthesize beyond a minimal structural wrap unless explicitly asked

Each speaking persona should usually provide:

- a short worldview framing
- what it notices first about the target
- its opinion, read, or instinctive move
- the main concern, tension, or question from that worldview

## Default Workflow

### 1. Anchor the target

Identify what the personas are being built for.

- idea
- plan
- draft
- decision
- problem statement
- branch set
- source text

If the target is sprawling, compress it into a blunt one- or two-sentence anchor before casting.
Do not spend the whole skill on clarification unless that is what the user actually needs.

### 2. Choose the cast logic

Decide whether the cast should be:

- preset-based
- broad worldview spread
- domain-focused but internally diverse
- user-specified types
- reusable archetypes for downstream work

Prefer worldview diversity over credential theater.

### 3. Cast the personas

Create the personas as stable cards.

Check for blur:

- are any two personas functionally the same?
- are the differences load-bearing or cosmetic?
- would these personas reliably disagree about important things?
- would they notice different features of the same target?
- does emotional register create a meaningfully different reaction where needed?

If the answer is no, rebuild the cast.

### 4. Activate only if asked

If the user wants `speak`, have each persona respond to the same anchored target.

Important rules:

- each persona answers independently
- no voting
- no ranking by default
- no forced consensus
- no giant summarizer voice taking over the result

### 5. Preserve downstream usability

If the cast is likely to be reused:

- keep persona cards stable
- keep names memorable
- keep worldview statements compact and explicit
- avoid one-off references that make the cast non-portable

## Response Shape

When responding with this skill, prefer one of these shapes.

### Cast Output

1. `Target:` one or two sentences
2. `Cast logic:` why these personas were chosen
3. `Personas:` compact cards for each persona

### Speak Output

1. `Target:` one or two sentences
2. `Cast:` compact cards or short intros
3. `Voices:` one section per persona with its independent take

Unless the user asks for it, do not end with an executive summary that flattens the differences.

## Composability

This skill is intentionally self-contained.

- do the cast cleanly enough that the personas can be reused later in any direction the user wants
- keep the target explicit so later steps can activate the same cast without rebuilding it
- avoid assuming what process comes next; that belongs to the user, not to this skill
- keep preset and emotional-register choices visible so they can be reused later without guesswork
- treat casting and speaking as portable outputs rather than as instructions for a larger pipeline

## Boundaries

- Do not pretend the personas are truly independent agents.
- Do not fake diversity by swapping labels on the same worldview.
- Do not add debate, voting, or consensus theater unless the user explicitly requests that kind of process.
- Do not over-summarize the voices into your own preferred answer.
- Do not let tone differentiation replace actual worldview differentiation.
- Do not use a preset pack mechanically if the target clearly needs adaptation.

## Failure Modes To Avoid

- six personas who all sound like the same assistant in different hats
- professions instead of worldviews
- broad cards with no stable stance or usable downstream identity
- speaking outputs that blur into one median answer
- unnecessary synthesis that destroys the point of the cast
- too many personas for the amount of real differentiation available
- pseudo-diversity where the cast differs in biography but not in reasoning
- emotional variety that is theatrical but not cognitively meaningful

## Compact Prompts

Use these when you need a fast entry point.

### Cast

- `Generate 6 distinct personas for thinking about this.`
- `Cast a council of different worldviews for this target.`
- `Give me reusable personas, not conclusions.`
- `Use the political preset with 6 personas.`
- `Use a psychology-schools preset and keep the cast reusable.`

### Speak

- `Generate 6 personas, then let each speak independently.`
- `Roleplay several different minds reacting to this.`
- `Have each persona give its own opinion without debate or synthesis.`
- `Use the emotional-spectrum preset and let each persona react to this.`
- `Give me 8 business-stakeholder personas and let them speak.`

## Default Deliverables

When the output is mature enough, end with one of these compact forms.

### Cast deliverable

- `Target:` one sentence
- `Cast logic:` one or two sentences
- `Personas:` 3 to 8 compact cards

### Speak deliverable

- `Target:` one sentence
- `Cast:` 3 to 8 compact cards or labels
- `Voices:` one short independent take per persona

Keep the result legible, reusable, and different.
The win condition is not agreement.
The win condition is a believable spread of minds.
