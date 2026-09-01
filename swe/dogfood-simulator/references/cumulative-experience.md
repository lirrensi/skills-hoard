# Cumulative Experience & Paper Cuts

## The Compound Failure

Individual findings are useful. But the most dangerous product failure is not any single finding — it is the **sequence** of findings a user hits in one session. Three Medium-severity problems back-to-back create a worse experience than one Critical problem. The user does not encounter your findings list. They encounter a timeline.

### The Death Spiral

A typical abandoned-user journey:

```
Minute 0-2:  Installation fails with cryptic error.            [Medium]
Minute 2-5:  First command documented in README doesn't work.   [High]
Minute 5-8:  Tries --help, it shows wrong version number.       [Low]
Minute 8-10: Finds a workaround on StackOverflow, it works.     [Relief]
Minute 10-15: Second command hangs with no feedback.             [Medium]
Minute 15:    Closes terminal. Uninstalls. Tells coworkers "don't use this."
```

None of these findings alone would kill the product. The sequence killed it. The user's emotional arc went: hope → confusion → frustration → relief → betrayal → abandonment. The "relief" moment (the workaround) actually made it worse — it created a false expectation that things were improving, making the final hang feel like a deeper betrayal.

### How to Detect Cumulative Friction

When you dogfood, you are not testing findings in isolation. You are experiencing them in sequence. Track your **session arc**:

1. **Before starting**: Write down your expectations. What are you hoping to achieve? How long do you think it will take?
2. **During**: Note every moment of friction. Not just the big ones. Every "hmm," every extra click, every moment of uncertainty.
3. **After**: How do you feel? Relieved it is over? Proud you figured it out? Exhausted? Annoyed? Your post-session emotion is the best single indicator of cumulative friction.

If you finish a session thinking "that was harder than it should have been" — that is a cumulative finding, not an individual one.

### Counting Paper Cuts

Paper cuts are individually minor frictions that collectively destroy the experience:

| Paper cut | Alone | In a 10-minute session with 15 others |
|---|---|---|
| Error message at wrong place on page | Minor | User stops reading error messages |
| Inconsistent flag naming (-v vs --verbose on different commands) | Minor | User cannot predict how anything works |
| Form clears on validation error | Minor | User retypes everything, twice, three times |
| Back button loses state | Minor | User stops using back button, navigation becomes manual |
| No autocomplete on common commands | Minor | User types everything by hand, wastes 30% of time |
| Slightly slow page load | Minor | 15 pages × 2s delay = 30 seconds of staring at nothing |

**The paper cut threshold**: when the user starts adapting their behavior to avoid the product's flaws rather than to accomplish their task, the cumulative damage has exceeded the product's value.

### Reporting Cumulative Friction

Do not just list individual paper cuts. Report them as a cluster:

```
### Cumulative Finding: The First-Use Death Spiral
- **What the user experienced**: In a 15-minute attempt to complete the primary job,
  the user encountered: (1) install failure needing manual workaround,
  (2) documented example not working, (3) wrong version in --help,
  (4) command hang with no feedback.
- **Why it matters cumulatively**: Individually, each is Medium or Low severity.
  Together, they created a 15-minute failure session where the user never
  achieved their goal. The session ended in abandonment. The user will not return.
- **The paper cuts (minor contributory factors)**: Wrong version number, inconsistent
  flag naming, missing progress indicators on sub-commands.
- **What should happen instead**: The install should work from the documented command.
  The first example should work. Version should match. Commands should have timeouts
  and progress. Fixing any ONE of these would not save the user — fixing the first
  three in sequence would.
```

### The Three-Strikes Rule

If a user hits three distinct friction points (not the same bug three times, but three different problems) before achieving their first success, the product is in danger. Users rarely give a product more than three chances to prove itself.

When dogfooding, if YOU hit three distinct failures before completing the primary job, report it as a cumulative Critical finding — even if each individual failure would be Medium. The cumulative experience is what matters to the user.

### The Relief-Betrayal Pattern

Watch for this sequence especially:

```
Failure → Workaround → Relief → Failure → Abandonment
```

The relief moment (finding a workaround) creates trust. The second failure destroys that trust MORE completely than if the user had never succeeded. It is better to fail consistently than to succeed once and then fail — the user feels personally betrayed by the false hope.

If your dogfood session follows this pattern, flag it prominently. This is the most psychologically damaging user experience.

### The Abandonment Interview

After a difficult session, ask yourself these questions as if you were interviewing a user who just abandoned the product:

1. "What were you trying to do when you decided to stop?"
2. "What was the moment you realized this was not going to work?"
3. "What would have kept you going? What one fix would have made you try one more time?"
4. "What will you use instead? Why is that better?"
5. "If a colleague asked about this product, what would you say?"

These questions reveal the cumulative impact better than any individual finding.
