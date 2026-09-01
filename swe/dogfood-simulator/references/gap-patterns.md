# Universal Gap Patterns

Every product type has the same structural failure modes. These patterns help you systematically find what is missing — not by reading code, but by understanding what any product in a given domain should offer.

---

## Symmetry Gaps

Every action should have a reverse. Users will discover one direction and immediately expect the other.

### Complete Symmetry Pairs

These are the most common "WTF, why can't I..." moments:

| Forward | Reverse |
|---------|---------|
| open | close |
| start | stop / end |
| create | delete |
| add | remove / delete |
| import | export |
| upload | download |
| connect | disconnect |
| enable | disable |
| subscribe | unsubscribe |
| follow | unfollow |
| enter | exit / leave |
| push | pull |
| forward | back |
| next | previous |
| maximize | minimize / restore |
| expand | collapse |
| activate | deactivate |
| mount | unmount |
| install | uninstall |
| lock | unlock |
| show | hide |
| pack | unpack |
| encode | decode |
| encrypt | decrypt |
| compress | decompress |
| serialize | deserialize |
| confirm | cancel / reject |
| apply | revert / discard |
| publish | unpublish |
| invite | revoke / remove |
| pin | unpin |
| bookmark | remove bookmark |
| mute | unmute |
| block | unblock |

### Testing for Symmetry

For every command, button, endpoint, or action you find:
1. Identify the "forward" action — what does it do?
2. Does the reverse action exist?
3. If the reverse exists, is it as discoverable as the forward?
4. Is the reverse action destructive and missing safety? (See safety gaps)

---

## Lifecycle Stage Gaps

Every entity in a product has a lifecycle. Products often handle the beginning and end but miss the middle.

### Document Lifecycle
Create → Draft → Edit → Review → Approve → Publish → Revise → Archive → Delete

Missing stages cause:
- No draft → users publish incomplete work or lose it on refresh
- No archive → completed/old work clutters active space
- No delete → test documents accumulate forever

### User Account Lifecycle
Register → Verify → Login → Update Profile → Reset Password → Change Email → Suspend/Deactivate → Delete Account

Missing stages cause:
- No verify → fake accounts, security issues
- No reset password → support burden
- No delete account → privacy compliance failure, user frustration

### Task / Work Item Lifecycle
Create → Assign → Start → Pause → Resume → Complete → Cancel → Reopen → Archive → Delete

Missing stages cause:
- No pause → user must either finish or abandon
- No cancel → tasks linger forever as "in progress"
- No reopen → accidental completions are permanent

### Resource / Asset Lifecycle
Acquire → Configure → Start/Deploy → Monitor → Scale → Backup → Restore → Migrate → Release/Destroy

Missing stages cause:
- No backup → disaster = total loss
- No monitor → blind to problems
- No destroy → leaked resources, cost accumulation

### Message / Communication Lifecycle
Compose → Preview → Send → Edit → Reply → Forward → Archive → Search → Delete

Missing stages cause:
- No edit after send → typos are permanent
- No search → cannot find old messages
- No archive → cluttered inbox

### File / Data Lifecycle
Create → Read → Write → Copy → Move → Rename → Share → Version → Delete → Recover

Missing stages cause:
- No versioning → overwritten data is lost
- No share → collaboration requires external tools
- No recover → deleted items are permanently gone

### Configuration Lifecycle
Read → Set → Unset → Validate → Reload → Reset → Backup → Migrate → Diff

Missing stages cause:
- No validate → invalid config silently breaks things
- No reset → stuck with experimental changes
- No diff → cannot see what changed

### API Key / Credential Lifecycle
Create → View → Rotate → Regenerate → Audit → Revoke → Delete

Missing stages cause:
- No list existing → unknown how many keys exist, security risk
- No rotate → long-lived credentials, security risk
- No audit → cannot tell who used which key

### Browser Tab / Navigation Lifecycle
Open → Close → Switch focus → Navigate → Back → Forward → Refresh → Duplicate → Pin → Reopen closed

Missing stages cause:
- No back/forward → cannot navigate multi-page workflows
- No switch focus → multiple tabs but cannot control which is active
- No duplicate → cannot compare or experiment

---

## Bulk Operation Gaps

If a user can do something to one item, they will eventually need to do it to many.

### Common Patterns

| Individual Action | Expected Bulk Action |
|---|---|
| Add one item | Batch add / Import from file |
| Delete one item | Bulk delete / Select all + delete |
| Update one item | Bulk update / Mass edit |
| Move one item | Move multiple / Reorganize |
| Tag one item | Apply tag to all |
| Send one message | Mass send / Campaign / Broadcast |
| Invite one user | Invite many / Import invite list |
| Duplicate one item | Duplicate many / Template-based creation |
| Archive one item | Archive all / Cleanup mode |

### Why Bulk Matters

Without bulk operations:
- Cleanup becomes a Sisyphean task (click delete 100 times)
- Import/migration workflows break (batch import not supported)
- Power users leave for more efficient tools
- Test data accumulates forever because cleaning is too painful

### What to Check
- If a create/add action exists, does a batch-add exist?
- If a delete action exists, can you select multiple and delete?
- If an update action exists, can you apply changes to many?
- Is there an import/export path at all?

---

## Visibility Gaps

If users can create or modify things, they need to be able to see and find them.

### Create → Need to See

| User can... | User needs to... |
|---|---|
| Create items | List all items / Search items / View item details |
| Create accounts | List users / See user activity |
| Create configurations | View current config / See defaults |
| Create API keys | List existing keys / See key metadata |
| Create schedules | View calendar / See upcoming / See past |

### Modify → Need to Track

| User can... | User needs to... |
|---|---|
| Update items | See change history / Diff before and after |
| Configure settings | See current values / Validate before applying |
| Share/grant access | See who has access / See permission levels / Audit access |
| Delete items | See what will be deleted / Confirm / Undo / See trash |

### State → Need to Know

| State exists | User needs to know |
|---|---|
| Background jobs running | Which jobs? Status? When started? |
| Scheduled tasks | What is scheduled? When next? |
| Active connections | How many? To what? Since when? |
| Resource usage | CPU? Memory? Disk? File handles? |
| Error conditions | What failed? When? How to fix? |

---

## Safety & Recovery Gaps

Users make mistakes. Good products anticipate this and provide escape hatches.

### Undo / Redo
Any action that changes state should be undoable. Especially:
- Data modifications (edit, delete, move, rename)
- Configuration changes
- Bulk operations
- Destructive operations

### Confirmations
Destructive actions should confirm, especially:
- Delete / bulk delete
- Irreversible changes (publish, send, deploy)
- Operations affecting other users (revoke access, reset passwords)
- Operations that cannot be undone

### Cancellation
Long-running operations should be cancellable:
- Network requests / Uploads / Downloads
- Batch processing / Computations
- Workflow steps the user started accidentally
- Operations the user changed their mind about

### Recovery Paths
When things go wrong, the user needs a way back:
- Trash / Recycle bin for deleted items
- Autosave / Drafts for in-progress work
- Rollback for deployments
- Backup for critical data
- Session restore after crash or restart
- "Reset to defaults" for configuration

### Timeout & Deadlock Protection
Operations that can hang should have:
- Configurable timeout with clear error on expiry
- Progress indicator or heartbeat
- Ability to cancel and clean up
- No silent retry loops

---

## Cross-Cutting Concern Gaps

These are needed by almost every product but are systematically forgotten.

### Search & Discovery
- Full-text search across all items
- Filter by attributes (tags, status, date, category)
- Sort by relevant fields
- Recent / frequently used
- Saved searches or bookmarks

### History & Audit
- Action history (who did what, when)
- Change tracking (what was changed, before/after)
- Session history (what did I do last time?)
- Error history (what went wrong?)

### Data Portability
- Import from common formats
- Export to common formats
- Backup entire state
- Restore from backup
- Migrate between versions or environments

### Collaboration
- Share items with others
- Permission levels (view, edit, admin)
- See who has access
- Revoke access
- Comment / discuss items

### Customization
- User preferences / settings
- Customize behavior (not just appearance)
- Templates for repeated workflows
- Defaults that can be changed
- Hooks or extension points

### Help & Documentation
- In-product help (tooltips, descriptions)
- Command-line help (`--help`, `help [topic]`)
- Error messages that explain and suggest
- Examples that actually work
- Getting-started guide or tutorial

### Power User Features
- Keyboard shortcuts for common actions
- Batch operations (see bulk gaps)
- Scripting / automation hooks
- Environment variable overrides for config
- Pipe-friendly output (JSON, TSV, etc.)

### Resilience
- Offline mode or degraded operation
- Graceful handling of missing dependencies
- Network failure recovery
- Rate limit handling with backoff
- Concurrent access safety

---

## Edge Case Gaps

Products work for the happy path but fail on these:

### Input Edge Cases
- Empty input / zero items
- Very long input (10x normal)
- Very large number of items (1000+)
- Invalid input (wrong type, wrong format)
- Malformed data (corrupted, truncated)
- Unicode / emoji / special characters
- Mixed language content
- Leading/trailing whitespace
- Duplicate input

### Environment Edge Cases
- Missing runtime (no Node, no Python, wrong version)
- Missing dependency
- File permission denied
- Disk full
- Memory exhausted
- Rate limit reached
- Network timeout
- DNS failure

### User Behavior Edge Cases
- First-time user, no prior state
- Returning user after months, stale state
- User in a hurry, skips steps
- User makes typos in every input
- User copies and pastes from somewhere else
- User has multiple sessions open concurrently
- User refreshes or closes mid-operation
- User runs the wrong command in the wrong directory
- User follows instructions in the wrong order

### Time & Locale Edge Cases
- Different time zones
- Daylight saving time transitions
- Leap seconds / leap years
- Different date formats (MM/DD vs DD/MM)
- Different number formats (1,000 vs 1.000 vs 1 000)
- Different languages / RTL text

---

## How to Use This Reference

When analyzing a product, run through each section:

1. **Symmetry**: For every action you find, is the reverse present?
2. **Lifecycle**: For each entity type, map the full lifecycle. Where are the gaps?
3. **Bulk**: Can the user do things one-at-a-time or many-at-once?
4. **Visibility**: Can the user see everything they have created, changed, or configured?
5. **Safety**: Can the user undo, confirm, cancel, and recover?
6. **Cross-cutting**: Search? History? Export? Help? Settings?
7. **Edge cases**: Empty? Large? Invalid? Offline? Concurrent?

Not every product needs everything. A simple calculator does not need import/export. A single-user CLI might not need permissions. Use judgment — but err on the side of "a user will expect this."

The most common oversight is believing "users won't need this" when in fact users need it constantly and simply suffer in silence.
