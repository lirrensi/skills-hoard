# Master Dogfood Checklist

This is the exhaustive reference. When you need to be absolutely sure you have not missed anything, run through this list. Not every question applies to every product. Use judgment.

---

## Section 1: First Contact

### Installation
- [ ] Can I install using ONLY the documented command?
- [ ] Does installation work in a completely clean environment?
- [ ] Does installation work in a path with spaces?
- [ ] Are there hidden dependencies not mentioned?
- [ ] Can I upgrade without breaking existing config?
- [ ] Can I uninstall completely? No leftover files?
- [ ] Does the install command match what the README shows?

### First Run
- [ ] What happens with no arguments?
- [ ] Does `--help` work? Is every subcommand/option listed?
- [ ] Does `--version` work? Match README?
- [ ] Is the first example in the README copy-paste runnable?
- [ ] Does it create any files I did not ask for?
- [ ] Does it require config that is not auto-generated?

---

## Section 2: Can the User Do Their Job?

### For Each Job to Be Done
- [ ] Can I complete the job using only docs and help text?
- [ ] How long did it take? How long SHOULD it take?
- [ ] Where did I hesitate? Where was I confused?
- [ ] Did I need knowledge not in the docs?
- [ ] Did I need to read source code?
- [ ] After completing: do I KNOW it worked?
- [ ] After completing: do I know what to do next?
- [ ] If I made a mistake: could I recover?
- [ ] If I stop mid-way: is my state preserved?
- [ ] Can I do this job a second time faster?

---

## Section 3: Symmetry & Closure

### For Every Action
- [ ] Open → Can I close?
- [ ] Start → Can I stop?
- [ ] Create → Can I delete?
- [ ] Enable → Can I disable?
- [ ] Add → Can I remove?
- [ ] Import → Can I export?
- [ ] Enter → Can I exit?
- [ ] Subscribe → Can I unsubscribe?
- [ ] Install → Can I uninstall?
- [ ] Push → Can I pull?
- [ ] Forward → Can I go back?
- [ ] Expand → Can I collapse?
- [ ] Maximize → Can I minimize?
- [ ] Connect → Can I disconnect?
- [ ] Lock → Can I unlock?
- [ ] Show → Can I hide?
- [ ] Pin → Can I unpin?
- [ ] Activate → Can I deactivate?
- [ ] Apply → Can I revert?
- [ ] Confirm → Can I cancel?

---

## Section 4: Lifecycle Completeness

### For Each Entity Type
Map: Create → [Draft] → Modify → View → [Share] → [Archive] → Delete
- [ ] Are all stages present that make sense for this entity?
- [ ] Are there dead-end states the user cannot leave?
- [ ] Can the user view ALL entities they created?
- [ ] Can the user find a specific entity among many?
- [ ] Is "delete" present? If not, why?
- [ ] Is there an archive/hide option that is not delete?
- [ ] Can the user duplicate or template common entities?

### For Each Workflow Type
Map: Start → [Pause] → Monitor → Complete → [Review] → [Reopen]
- [ ] Can the user pause without losing progress?
- [ ] Can the user see progress or status?
- [ ] Is the completion step clear and confirmable?
- [ ] Can the user reopen or restart from the end?

---

## Section 5: Visibility & Discoverability

### Can the User See...?
- [ ] Everything they created
- [ ] Current configuration
- [ ] What will happen before they commit an action
- [ ] Change history or version differences
- [ ] Who has access to shared items
- [ ] Scheduled or queued operations
- [ ] Active connections or sessions
- [ ] Error conditions or warnings
- [ ] Resource usage or limits
- [ ] Default values before changing them

### Can the User Find...?
- [ ] The main feature without reading docs
- [ ] Help for any command or page
- [ ] The search function
- [ ] Settings or configuration
- [ ] The way to give feedback or report issues

---

## Section 6: Safety & Recovery

### Undo & Redo
- [ ] Can the user undo their last action?
- [ ] Can the user redo if they undo too far?
- [ ] Is undo available for destructive actions?
- [ ] Is undo available for bulk operations?
- [ ] How far back does undo go? Is it enough?

### Confirmation
- [ ] Are destructive actions confirmed?
- [ ] Is the confirmation clear about what will happen?
- [ ] Is there a way to skip confirmation for power users?
- [ ] Are "nuclear" options visually distinct from safe options?

### Recovery
- [ ] Is there a trash or recycle bin?
- [ ] Is there autosave for in-progress work?
- [ ] Can the user restore from backup?
- [ ] Can the user reset to defaults?
- [ ] Can the user recover from a crash or interruption?
- [ ] Can the user recover from a partial operation?

### Errors
- [ ] Are error messages in user language?
- [ ] Do errors suggest what to do next?
- [ ] Do errors distinguish "you did something wrong" from "something broke"?
- [ ] Are errors logged somewhere the user can access?
- [ ] Are errors consistent in format and location?

---

## Section 7: Bulk & Scale

- [ ] Can the user add many items at once?
- [ ] Can the user delete many items at once?
- [ ] Can the user update many items at once?
- [ ] Can the user select multiple items?
- [ ] Can the user select all?
- [ ] Are bulk operations confirmed?
- [ ] Can bulk operations be undone?
- [ ] Does the product handle 100 items? 1000? 10,000?

---

## Section 8: Customization

- [ ] Can the user change behavior (not just appearance)?
- [ ] Are there sensible defaults for every setting?
- [ ] Can the user see current values before changing?
- [ ] Can the user validate config before applying?
- [ ] Can the user reset any setting to default?
- [ ] Are settings documented with examples?
- [ ] Do settings persist across sessions or restarts?

---

## Section 9: Help & Learning

- [ ] Is `--help` or equivalent useful?
- [ ] Is there a getting-started guide?
- [ ] Are there examples for common tasks?
- [ ] Are error messages helpful?
- [ ] Is there a way to contact support or community?
- [ ] Is the documentation version-locked or does it always show latest?

---

## Section 10: Automation & Scripting

- [ ] Can the user run this non-interactively?
- [ ] Are there `--yes` or `--non-interactive` flags?
- [ ] Does it output parseable formats? (JSON, CSV, TSV)?
- [ ] Are exit codes meaningful?
- [ ] Does normal output go to stdout? Errors to stderr?
- [ ] Can it be piped? Can it pipe to others?
- [ ] Does it respect environment variables for config?
- [ ] Can it be used in CI/CD pipelines?

---

## Section 11: Cross-Cutting

- [ ] Search: finding things among many items
- [ ] Filter: narrowing down by attributes
- [ ] Sort: organizing by relevant fields
- [ ] History: tracking what happened
- [ ] Import: getting data in
- [ ] Export: getting data out
- [ ] Share: collaboration with others
- [ ] Permissions: controlling access
- [ ] Notifications: being aware of events
- [ ] Keyboard shortcuts: efficiency for power users
- [ ] Templates: reducing repetitive work
- [ ] Preview: seeing before committing
- [ ] Compare/Diff: understanding changes
- [ ] Duplicate: copying without rework
- [ ] Backup: protecting against disaster
- [ ] Offline mode: working when degraded
- [ ] Progress indicators: knowing what is happening
- [ ] Timeouts: not waiting forever
- [ ] Cancellation: stopping what you started

---

## Section 12: Edge Cases

### Input
- [ ] Empty input
- [ ] Very long input (10x normal)
- [ ] Invalid input (wrong type or format)
- [ ] Special characters / Unicode / Emoji
- [ ] Leading/trailing whitespace
- [ ] Duplicate input

### Environment
- [ ] Missing runtime
- [ ] Wrong runtime version
- [ ] Missing dependency
- [ ] Permission denied
- [ ] Disk full
- [ ] Memory exhausted
- [ ] Network timeout
- [ ] Network offline
- [ ] Rate limit hit

### User Behavior
- [ ] First-time user, no state
- [ ] Returning user, stale state
- [ ] User in a hurry, skipping steps
- [ ] User making typos
- [ ] User closing mid-operation
- [ ] User has multiple tabs or windows open
- [ ] User follows steps in wrong order

---

## Section 13: Trust & Emotion

### The Trust Checklist
- [ ] After using this product, do I feel competent?
- [ ] After making a mistake, do I feel safe or afraid?
- [ ] Do I trust the documentation?
- [ ] Do I trust that my data is safe?
- [ ] Do I trust that operations will complete?
- [ ] Would I use this for something important?
- [ ] Would I recommend this to a colleague?
- [ ] Would I use this on a deadline?

### The Emotion Checklist
- [ ] Any moment of "wait, what?"
- [ ] Any moment of "why did it do that?"
- [ ] Any moment of "how do I...?"
- [ ] Any moment of "oh no!"
- [ ] Any moment of "that was easy!"
- [ ] Any moment of "I trust this"

---

## Using This Checklist

Run through every section. Check what applies. For items that do NOT apply, note why — this sharpens your understanding of the product's domain. For items you cannot answer ("does it handle 1000 items?"), note them as untested.

A product that passes this entire checklist is rare. That is normal. The goal is not perfection — it is awareness of gaps and prioritization of what matters most.

If you only have 30 minutes, run Section 1 (First Contact) and Section 2 (Can the User Do Their Job). Those two sections alone will find 80% of real-world problems.
