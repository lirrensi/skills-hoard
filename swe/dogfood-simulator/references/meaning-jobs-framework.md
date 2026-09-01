# Meaning & Jobs Framework

## The Core Idea

Products are not collections of features. They are answers to a question: "What does a user want to accomplish?"

A dogfood tester who only counts features will find 0 bugs in a product that has 100 features but makes users feel stupid. The bugs that matter are in the gap between what the product does and what the user needs to do. You find those bugs by understanding the user's intent — their **Job to Be Done**.

## Jobs to Be Done

### What Is a Job?

A job is NOT a feature. A job is a human goal:

- ❌ "The user wants to use the cron tool."
- ✅ "The user wants their database backup to run every night without them having to remember."

- ❌ "The user wants to open the dashboard."
- ✅ "The user wants to know if anything went wrong overnight so they can fix it before the morning meeting."

- ❌ "The user wants to call the search API."
- ✅ "The user wants to find relevant information quickly so they can finish their report."

### How to Find Jobs

Read the README, docs, and any marketing material. Ask:
1. What problem does this claim to solve?
2. Who has this problem, and in what context?
3. What does success look like for that person?

Write 2-4 user stories in this format:

```
As a [specific person in a specific context],
I want to [accomplish a meaningful goal],
so that [I get a specific benefit].
```

### Example Jobs by Product Type

**CLI toolkit:**
- "As a developer rushing to ship before the weekend, I want to schedule health checks for my deployment, so that I am notified if it goes down while I am away."
- "As a solo developer without a DevOps team, I want to run background tasks without setting up a job queue, so that I can focus on features instead of infrastructure."

**Search tool:**
- "As a researcher working on a deadline, I want to search across multiple sources and get verified answers in one place, so that I do not waste time switching between browser tabs."
- "As a developer debugging a production issue, I want to quickly look up error messages and find relevant solutions, so that I can fix the problem before users notice."

**Editor extension:**
- "As a developer with repetitive terminal commands, I want to run them directly from my notes file, so that I do not have to copy-paste between editor and terminal."
- "As a team lead, I want new developers to follow a runbook of commands without knowing the CLI tools, so that onboarding is faster and less error-prone."

### Testing Against Jobs

For each job:
1. Can you complete it from a cold start?
2. Where does the path break?
3. Are there steps that require insider knowledge?
4. Does the product tell you when the job is done?

---

## Meaning Gap Analysis

### What Is a Meaning Gap?

A meaning gap is not a missing feature. It is a missing connection between the product's behavior and the user's understanding. The product DOES something, but the user does not understand what, why, or what to do next.

### The Lenses for Meaning Analysis

**The Intention Lens:**
- What was the user trying to do when they discovered this gap?
- Why did they choose this product to do it?
- What did they expect to happen?

**The Context Lens:**
- What else is the user doing at the same time?
- What is their emotional state? (Stressed? Rushed? Curious?)
- What did they do before using this product? What will they do after?

**The Expectation Lens:**
- What do similar products do?
- What would a reasonable person assume?
- What did the documentation or marketing promise?

**The Emotion Lens:**
- How does this make the user feel? Competent or stupid? In control or trapped? Confident or anxious?
- Does the product build trust or erode it?
- Would the user recommend this, or warn others away?

### Applying the Lenses

For every finding, run through these questions:

1. **What was the user trying to do?**  
   Be specific about context. "The user was setting up their CI pipeline. They had 15 minutes before a meeting. They needed to configure the tool to run in the pipeline."

2. **What did they expect to happen?**  
   "They expected the setup command to produce a config file they could commit to the repo."

3. **What actually happened?**  
   "The setup command launched an interactive wizard that required keyboard input. In the CI environment (headless), this crashed with a terminal error and wrote a corrupt config file."

4. **Why does this gap matter to the user's life?**  
   "This turns a 2-minute configuration step into a 30-minute debugging session. The user misses their meeting. They now distrust the tool for any automation use case."

5. **What would fix it at the meaning level?**  
   "The tool should detect non-interactive environments and either skip the wizard (using defaults) or provide a clear flag like `--non-interactive` with documentation on how to configure manually."

---

## Workflow Completion Analysis

### The End-to-End Test

For each job, map the COMPLETE path from intent to satisfaction:

```
INTENT → DISCOVER → START → EXECUTE → VERIFY → FINISH
```

At each transition, ask: is the user...  
- Sure about what to do next?  
- Able to do it without reading source code?  
- Given feedback that the step completed?  
- Able to go back if they made a mistake?

### Common Breaks in the Chain

**INTENT → DISCOVER:**  
The user knows what they want, but cannot find the feature.  
- Missing search  
- Poor command naming  
- Feature buried in menus  
- Documentation that doesn't match the interface

**DISCOVER → START:**  
The user found the right thing, but cannot begin.  
- Requires configuration that hasn't been set up  
- Requires permissions the user doesn't have  
- Requires a dependency that isn't installed  
- Requires knowledge of a parameter format

**START → EXECUTE:**  
The user started, but the path breaks partway.  
- Missing step in the workflow (can create but not configure)  
- Confusing step (ambiguous options with no guidance)  
- Step that works in isolation but not in sequence (race condition, order dependency)

**EXECUTE → VERIFY:**  
The user did the thing, but does not know if it worked.  
- Silent failure  
- Success output that looks like failure  
- No confirmation of side effects  
- Results not visible without additional steps

**VERIFY → FINISH:**  
The user knows it worked, but cannot close the loop.  
- Cannot save or export results  
- Cannot share with others  
- Workflow has no defined end state  
- Lingering state that clutters future sessions

---

## The Emotion Audit

Products are not just functional. They are emotional. Every interaction builds or destroys trust.

### The Trust Scale

After using a product, ask: where on this scale would a user land?

```
HOSTILE ← → FEARFUL ← → TOLERANT ← → COMFORTABLE ← → CONFIDENT ← → DELIGHTED
```

- **Hostile**: The product actively harms the user (loses data, corrupts config, wastes time)
- **Fearful**: The user is afraid to explore or make changes (no undo, no preview, punishment for mistakes)
- **Tolerant**: The product works but the user is constantly working around its quirks
- **Comfortable**: The product mostly does what is expected, minor frustrations
- **Confident**: The user explores freely knowing mistakes are safe and reversible
- **Delighted**: The product surprises the user with unexpected helpfulness, speed, or insight

### Emotional Anti-Patterns

**The Betrayal:**  
The product promised something in its README. The user invested time based on that promise. The promise was false. The user will never trust the README again.

**The Trap:**  
The user entered a state. They cannot exit. They feel trapped and anxious. They avoid that part of the product in the future.

**The Punishment:**  
The user made a minor mistake. The product punished them with data loss, wasted time, or a cryptic error. They feel stupid. They will blame themselves, not the product — but they will also stop using it.

**The Ghost:**  
The product behaves differently each time. The user cannot form a mental model. They feel like they are fighting an invisible force. They lose confidence in their own understanding.

**The Desert:**  
The user needs help. There is none. No error message. No documentation. No community. They are alone with their confusion. They abandon the product.

### Emotional Design Questions

- Does this product make the user feel: a) competent, b) stupid, or c) indifferent?
- After using this product, does the user feel: a) relieved, b) frustrated, or c) afraid?
- Would the user: a) recommend this, b) tolerate this, or c) warn others away?
- If the user makes a mistake, do they think: a) "oops, let me fix that" or b) "oh no, what have I done?"
- Does the product communicate: a) "I've got you covered" or b) "you're on your own"?

---

## How to Write Meaning-Rich Findings

### Bad (Feature-Centric)

> Missing `bg stop` command. Users cannot stop background jobs without removing them.

### Good (Meaning-Centric)

> **What the user was trying to do:** A developer had a model training job running in the background. They needed to free up GPU memory for an urgent debugging task before a meeting in 20 minutes. They wanted to pause the training, debug, and resume later.
>
> **What went wrong:** There is no way to stop a background job without permanently destroying it. The `rm` command kills the process AND deletes the job record, logs, and history. The user must choose between keeping their GPU tied up indefinitely or losing all trace of the training run.
>
> **Why it was confusing:** The user expected symmetry. They started the job, so they should be able to stop it. The only option (remove) is destructive and named like a cleanup operation, not a control operation. The user feels trapped and anxious — they started something they cannot control.
>
> **What should happen:** A clear `stop` command that terminates the process while preserving the job record, logs, and status. The user can then `status` to confirm it stopped, `logs` to review progress, and `start` (or `resume`) to continue later.

### The Difference

The bad finding tells you WHAT is missing (a command). The good finding tells you WHY it matters (a developer about to miss a meeting, trapped between losing GPU memory and losing training history). The bad finding suggests a feature. The good finding diagnoses a broken trust relationship between user and product.
