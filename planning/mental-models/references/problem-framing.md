# Problem Framing Library

How to define the problem before trying to solve it. Often the highest-leverage move is better problem definition, not better analysis.

---

## Core Framing Questions

Ask these before diving into solutions:

| Question | Why It Matters |
|----------|---------------|
| **What is the actual problem?** | Often what people describe is a symptom, not the root problem. |
| **Who says this is a problem?** | Different stakeholders see different problems. |
| **What would "solved" look like?** | If you can't define success, you can't achieve it. |
| **Is this my problem to solve?** | Not every problem you notice is yours to fix. |
| **Is this a problem worth solving?** | Cost of solving vs cost of living with it. |
| **What's the real constraint?** | Often the assumed constraint isn't the actual bottleneck. |

---

## Problem Types

Different problems need different approaches:

| Type | Characteristics | Approach |
|------|----------------|----------|
| **Search Problem** | Solution exists, you need to find it | Research, explore, iterate |
| **Coordination Problem** | Everyone would benefit from aligning but can't | Standards, protocols, communication |
| **Incentive Problem** | People act against the collective good because of individual incentives | Change the incentive structure |
| **Information Problem** | Decisions are bad because information is missing or asymmetric | Gather information, reduce asymmetry |
| **Constraint Problem** | Something is blocking progress | Identify and relieve the bottleneck |
| **Definition Problem** | The problem itself is unclear | Spend time clarifying before solving |

---

## Reframing Techniques

| Technique | What to Do | Example |
|-----------|-----------|---------|
| **Reverse the problem** | Instead of "how to achieve X," ask "how to avoid not-X" | Instead of "how to succeed," ask "how to guarantee failure" — then avoid those things |
| **Zoom in / Zoom out** | Change the level of detail | Zoom out: "Is this a strategy problem?" Zoom in: "What's the specific blocker?" |
| **Time horizon shift** | Change the timeframe you're considering | "How does this look in 1 week vs 1 year vs 10 years?" |
| **Stakeholder lens** | Look at the problem from different perspectives | "How does the user see this? The engineer? The manager? The competitor?" |
| **Symptom vs Root Cause** | Ask "why" five times to dig deeper | "Server crashed" → "Why?" → "No monitoring" → "Why?" → "No one owned it" |
| **Constraint identification** | Find the actual bottleneck | "We need more developers" — but is the constraint developers, or unclear requirements? |
| **Reframe the metric** | Are you measuring what matters? | "We need more users" → "We need more engaged users" → "We need users who retain" |

---

## The Cynefin Framework

Sort problems into domains. Each needs a different strategy.

| Domain | Characteristics | Strategy |
|--------|----------------|----------|
| **Simple / Clear** | Cause and effect are obvious. Best practices exist. | **Sense → Categorize → Respond.** Follow the playbook. |
| **Complicated** | Cause and effect exist but aren't obvious. Expert analysis needed. | **Sense → Analyze → Respond.** Get expert input, then decide. |
| **Complex** | Cause and effect can only be understood in retrospect. No best practices. | **Probe → Sense → Respond.** Run experiments, learn, adapt. |
| **Chaotic** | No clear cause and effect. Crisis mode. | **Act → Sense → Respond.** Do something immediately to stabilize, then assess. |
| **Disorder** | You don't even know which domain you're in. | Figure out which domain you're in first. |

**Key insight:** Most people treat complex problems as complicated (trying to analyze when they should be experimenting) or simple problems as complex (overthinking when they should just follow the playbook).

---

## Root Cause Analysis

### The 5 Whys Technique:

1. State the problem
2. Ask "Why?" → get an answer
3. Ask "Why?" about that answer → get a deeper answer
4. Repeat 5 times (or until you hit a systemic cause)

**Example:**
- Problem: Website went down
- Why? Server ran out of memory
- Why? Memory leak in the new feature
- Why? No load testing before deploy
- Why? No load testing in the CI pipeline
- Why? **No one owns testing infrastructure** ← root cause

### When 5 Whys breaks down:

- When there are multiple causes (use a fault tree instead)
- When causes are circular (use systems thinking)
- When the "why" leads to "because people" (usually means a process/system problem, not a people problem)

---

## Constraint Analysis (Theory of Constraints)

1. **Identify the constraint** — what's the bottleneck limiting throughput?
2. **Exploit the constraint** — get maximum value from the bottleneck
3. **Subordinate everything else** — align non-bottlenecks to support the constraint
4. **Elevate the constraint** — invest in increasing bottleneck capacity
5. **Repeat** — once the constraint is relieved, a new one emerges

**Key insight:** Optimizing non-bottlenecks is wasted effort. Only improvements at the constraint matter.

---

## Common Framing Mistakes

| Mistake | What Goes Wrong |
|---------|----------------|
| **Solving the wrong problem** | Perfect solution to a problem that doesn't matter |
| **Confusing symptoms with causes** | Treating fever instead of infection |
| **Anchoring on the first framing** | Accepting how the problem was presented without questioning it |
| **Scope creep** | Problem definition keeps expanding until it's unsolvable |
| **Ignoring stakeholders** | Solving from one perspective while creating problems for others |
| **Premature solution jumping** | Jumping to solutions before understanding the problem |
| **Optimizing the wrong metric** | Goodhart's Law — improving the number instead of the thing |
