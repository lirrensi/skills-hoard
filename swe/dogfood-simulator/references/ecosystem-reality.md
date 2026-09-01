# Ecosystem Reality

Products do not exist in isolation. They are used between other tools, alongside competing options, and in real environments that are messier than the developer's machine. This reference helps you find gaps at the ecosystem level — the space between the product and everything around it.

---

## Cross-Product Integration

### The Pipe Test

A CLI tool that cannot be piped is a CLI tool that does not belong in the Unix ecosystem. A web app that cannot share URLs is a web app that does not belong on the internet. An API that cannot be called from code with standard error handling is an API that does not belong in any stack.

For each output the product produces, ask:
- Can this output be consumed by the next tool in a pipeline?
- Is the format parseable? (plain text with predictable structure? JSON? CSV?)
- Are error messages separated from normal output? (stderr vs stdout?)
- Are exit codes meaningful and consistent?
- Does the output format change between versions? Is that documented?

For each input the product accepts, ask:
- Can it read from stdin? From a file? From an environment variable?
- Can it accept output from common upstream tools without preprocessing?
- Does it handle piped input differently from interactive input?

### The Scripting Test

Can a user embed this product in a shell script, Python script, or CI pipeline without reading source code?

- Are there `--yes`, `--non-interactive`, or `--batch` flags for automation?
- Can all configuration be done via command-line flags or environment variables?
- Does the tool exit with code 0 on success and non-zero on failure?
- Are error conditions distinguishable by exit code? (1=usage error, 2=network error, etc.)
- Is there a `--json` or `--quiet` output mode for machine consumption?

### The Environment Test

Real environments are messy. Test the product in:
- A path with spaces in it
- An environment where the expected runtime is a different version
- An environment where a dependency is missing
- An environment behind a proxy or firewall
- An environment with limited permissions (no admin, no sudo)
- An environment where the locale is not English

### The Coexistence Test

What happens when the product shares space with:
- An older version of itself (upgrade path)
- A newer version of itself (downgrade path)
- A different tool that uses the same port, config directory, or temp directory
- Multiple instances running simultaneously
- The same data being accessed concurrently

---

## Switching & Stickiness

### The Switching Cost Audit

Every user of this product was previously using SOMETHING — even if that something was "copy-pasting into Google" or "writing it down on paper." How hard is it to switch?

- Is there an import path from common alternatives?
- Is there documentation comparing this product to alternatives?
- Can the user's existing data be migrated automatically or with clear steps?
- If the user switches, what do they lose? (History? Muscle memory? Integrations?)
- How long until the user is as productive as they were with their old solution?

### The Stickiness Audit

Once a user has invested time in this product, how hard is it to leave? This sounds perverse, but stickiness matters for ecosystem survival. A product that is easy to leave is easy to forget.

- Does the product accumulate valuable state? (History, config, templates, data)
- Can that state be exported? (The user should be able to leave, but the VALUE should be portable)
- If the user stops using it for a month, do they lose anything?
- Is there a community, plugin ecosystem, or integration network that adds switching cost?

### The "Why Remember This?" Test

Users have finite attention. They install dozens of tools. They bookmark hundreds of pages. Most of them are forgotten. Ask:

- After installing, does the product do something to make itself memorable?
- Does it provide immediate value, or does it require setup before value appears?
- Does it "make noise" — notifications, presence, reminders — or does it fade into the background?
- If the user does not use it for two weeks, will they remember it exists? Will they remember how to use it?
- Is there a "welcome back" experience for returning users?

**The forgotten tool pattern**: A tool that works perfectly but makes no impression. The user installs it, uses it once, and never thinks about it again. It sits on disk consuming space and never opens. It might as well not exist. The product failed not because it was bad, but because it was forgettable.

### The "Why Integrate Now?" Test

Tools that require integration work before showing value are at extreme risk. The user installs it, realizes they need to connect it to five other things, and says "I will do that later." They never come back.

- Can the product demonstrate value without full integration?
- Is there a "quick start" that uses mock data or built-in defaults?
- Is integration progressively revealed (connect one thing, see value, connect another) rather than all-at-once?
- What is the minimum time-to-first-value? Under 5 minutes is ideal. Under 30 minutes is acceptable. Over 30 minutes and most users will not complete it.

---

## Unusual Usage Degradation

### The Abuse Test

What happens when the product is used in ways the developer did not anticipate? Not maliciously — just differently.

**Volume abuse:**
- What happens with 100x the expected input?
- What happens with files 10x the expected size?
- What happens with concurrent usage 5x the expected load?
- Does it degrade gracefully (slow down but keep working) or catastrophically (crash, corrupt, hang)?

**Frequency abuse:**
- What happens if the user runs the same command 100 times in 10 seconds?
- What happens if the user rapidly opens and closes the UI?
- What happens if the user starts and cancels operations repeatedly?
- Does state accumulate? Does performance degrade? Do resources leak?

**Path abuse:**
- What happens if the user skips a step in a documented workflow?
- What happens if the user does steps in reverse order?
- What happens if the user starts a workflow, abandons it, and starts again?
- Does the product handle partial state, or does it corrupt?

**Input abuse:**
- What happens with binary data where text is expected?
- What happens with deeply nested structures?
- What happens with circular references?
- What happens with Unicode everywhere? Emoji? RTL text? Mixed direction?

### The Recovery Test

After abuse, can the product recover?

- Can the user reset to a known-good state?
- Is there a "safe mode" or minimal configuration that bypasses broken features?
- Can the user export their data before attempting recovery?
- Are there diagnostics or health checks?

---

## Complexity Choice

### The Forced Complexity Anti-Pattern

Some products force the user to configure everything before anything works. A thousand-line config file required on day one. Five environment variables that must be set. Three external services that must be running.

This is not complexity. This is **hostility to new users.**

Check:
- Can the product start and show value with zero configuration?
- Are defaults sensible for 80% of users?
- Can configuration be added incrementally as needs grow?
- Is there a distinction between "required to run" and "recommended for production"?
- Does the README or onboarding distinguish these clearly?

### The Progressive Disclosure Audit

Good products reveal complexity as the user demonstrates readiness:

```
Level 0: Works with zero config. Shows immediate value.
Level 1: User discovers a setting they want to change. Changes it easily.
Level 2: User needs advanced features. Discovers them through natural exploration.
Level 3: User becomes a power user. Discovers scripting, automation, plugins.
```

Bad products dump Level 3 on Level 0 users. Ask:
- What does the user see on first run? Is it overwhelming or inviting?
- Can the user complete the primary job at Level 0?
- Are advanced features behind clear "advanced" or "expert" labels, not mixed into the main interface?
- Can the user ignore features they do not need, or do they clutter the experience?

### The Escape From Complexity Test

If a user DOES dive into complex configuration, can they escape?

- Can they reset individual settings to defaults?
- Can they reset all settings to defaults without reinstalling?
- Can they see what they changed and when?
- Can they export their configuration to share with others or save for later?

---

## Value Recognition

### The "Did It Show Value?" Test

After a session, ask:

- Did the user achieve something they could not have achieved without the product?
- Did the user achieve something FASTER than without the product?
- Did the user DISCOVER something they did not know before?
- Did the product save the user from a mistake they would have made otherwise?

If the answer to all four is "no" or "maybe" — the product has not demonstrated its value. The user will not return. It does not matter how well-designed the product is. Value must be FELT, not explained.

### The Time-to-Value Ratio

How long until the user feels the product was worth the time they invested?

```
Time invested: reading README + installing + configuring + learning + first use
Value received: time saved, mistakes prevented, insights gained, capabilities added
```

If Time > Value after the first session, the user will not return for a second. The product must pay back the user's investment in the first session, or the relationship ends.

### The "One Thing" Test

After using the product, can you name ONE thing it did that made you think "I am glad I used this"?

If not, the product has failed its ecosystem reality check. It does not matter if the code is elegant, the architecture is clean, or the test coverage is excellent. It did not earn its place in the user's toolkit.
