# Missing Verbs Patterns Reference

This document catalogs common patterns of domain closure gaps — the "forgot to add go-back" class of problems.

## 1. Symmetry Gaps (The Most Common)

If a user can do something, they usually expect to be able to undo or reverse it.

| Action | Expected Reverse |
|--------|-----------------|
| Open | Close |
| Start | Stop / End |
| Create | Delete |
| Add | Remove |
| Import | Export |
| Upload | Download |
| Connect | Disconnect |
| Enable | Disable |
| Subscribe | Unsubscribe |
| Follow | Unfollow |
| Enter | Exit / Leave |
| Push | Pull |
| Forward | Back |
| Next | Previous |
| Maximize | Minimize |
| Expand | Collapse |
| Activate | Deactivate |
| Mount | Unmount |
| Install | Uninstall |
| Lock | Unlock |
| Show | Hide |

**Example**: A browser API that lets you open tabs but not close them. A task manager that lets you create tasks but not archive them.

## 2. Lifecycle Stage Gaps

Products often handle the beginning and end of a lifecycle but miss the middle.

### Document Lifecycle
- Create → Draft → Edit → Review → Approve → Publish → Archive → Delete

### User Account Lifecycle
- Register → Verify → Login → Logout → Update Profile → Reset Password → Deactivate → Delete Account

### Task Lifecycle
- Create → Assign → Start → Pause → Resume → Complete → Cancel → Reopen → Archive

### Resource Lifecycle
- Acquire → Configure → Start → Monitor → Scale → Backup → Restore → Release

**Example**: A CMS that lets you create and publish posts but has no draft state. A CI/CD tool that can trigger builds but not pause or cancel them.

## 3. Bulk Operation Gaps

If a user can do something to one item, they often need to do it to many.

| Individual | Expected Bulk |
|-----------|--------------|
| Add item | Batch add / Import CSV |
| Delete item | Bulk delete / Select all + delete |
| Update item | Bulk update / Mass edit |
| Send message | Mass send / Campaign |
| Apply tag | Apply to all |
| Move item | Move multiple |

**Example**: An email tool that lets you send one email at a time but not a newsletter. A file manager that can delete one file but not select-and-delete.

## 4. Visibility Gaps

If users can create or modify things, they need to be able to see and find them.

| Action | Expected Visibility |
|--------|-------------------|
| Create | List / View / Search |
| Update | View changes / History / Diff |
| Delete | Confirm / Undo / Trash |
| Share | See who has access / Permissions |
| Configure | View current config / Validate |

**Example**: An API that lets you create API keys but not list existing ones. A settings panel that lets you change settings but not see the defaults.

## 5. Safety & Recovery Gaps

Users make mistakes. Good products anticipate this.

- **Undo/Redo**: Any destructive or state-changing action
- **Confirmations**: Destructive actions without confirmation
- **Autosave**: Long-form input without autosave
- **Drafts**: Multi-step workflows without save-as-draft
- **Recovery**: Deleted items with no trash/recycle
- **Timeouts**: Operations that can hang forever
- **Cancellation**: Long-running operations that can't be cancelled

**Example**: A form that loses all data on accidental refresh. A deployment tool with no rollback.

## 6. Cross-Cutting Concern Gaps

These features are expected in almost any product but are often forgotten.

| Concern | Why It Matters |
|---------|---------------|
| Search | Finding things among many items |
| Filter | Narrowing down lists |
| Sort | Organizing lists |
| History | Tracking what happened |
| Backup/Restore | Disaster recovery |
| Import/Export | Data portability |
| Share | Collaboration |
| Permissions | Multi-user safety |
| Settings | Customization |
| Help/Documentation | Onboarding |
| Keyboard shortcuts | Power users |
| Accessibility | Inclusivity |
| Dark mode | User comfort |
| Offline mode | Reliability |
| Notifications | Awareness |
| Audit log | Accountability |
| Templates | Repetition reduction |
| Duplicate | Avoiding rework |
| Preview | Reducing mistakes |
| Compare/Diff | Understanding changes |

## 7. Mental Model Mismatches

Sometimes the feature exists but works in a way that violates user expectations.

- **Noun vs Verb confusion**: Is "project" a thing you create or an action you take?
- **Inconsistent patterns**: "Add user" works differently than "Add team"
- **Hidden state**: The app remembers something the user didn't know it remembered
- **Surprise mutations**: Clicking something changes state unexpectedly
- **Missing affordances**: Buttons that don't look clickable, links that don't look like links

## 8. Edge Case Gaps

Products often work for the happy path but fail on edge cases.

- Empty input / zero items
- Very large input / many items
- Invalid input / malformed data
- Network failure / timeout
- Concurrent modifications
- Permission denied
- Resource exhausted (disk full, memory limit)
- Unicode / special characters
- Time zones / daylight saving
- Browser back button behavior

## Quick Checklist

Before declaring a product "complete", verify:

- [ ] Every "open" has a "close"
- [ ] Every "create" can be "deleted"
- [ ] Every "start" can be "stopped"
- [ ] Users can see what they created
- [ ] Users can undo mistakes
- [ ] Users can do operations in bulk
- [ ] Error messages are helpful, not internal jargon
- [ ] Multi-step workflows can be saved/resumed
- [ ] The product works when offline or degraded
- [ ] Power users have shortcuts
- [ ] Help is discoverable without reading source code
