# The Ten Confusion Patterns

These are the most common ways products fail their users. They appear across every domain, every technology, every product type. Learn to recognize them. Every finding you produce should be traceable to at least one of these patterns.

---

## 1. The Promise Gap

The product claims to do something. When the user tries it, reality differs from the claim.

**What it looks like:**
- Documentation says installation is one command. It requires three hidden steps.
- A feature is advertised in the README but does not work as described.
- Help text implies a capability the interface does not expose.
- Examples in docs use syntax that no longer works.
- Screenshots show an old version of the interface.
- Changelog claims a feature was added but it is not present.
- Version numbers in README, package file, and actual software are all different.

**Why it confuses:** The user made a decision based on a promise. They invested time and trust. When the promise breaks, they don't know if they misunderstood, if the docs are wrong, or if the product is broken. They feel betrayed and stupid — neither is their fault.

**Real cases:**
| What was promised | What actually happened |
|---|---|
| "Install with one command" | The one command installs only base package. Core features require optional extras not mentioned in install section. |
| "Works on all platforms" | Windows installation silently requires different steps. Mac install hangs without Xcode tools. |
| README shows Ctrl+X shortcut | Actual binding is Alt+X. Ctrl+X does nothing. |
| "Automatic setup" | Setup crashes in non-interactive environments with no fallback. |
| Changelog: "Added export feature" | Feature is not present in any command list or help text. |

**What to check:**
- Does the README quickstart work from a completely clean environment?
- Does the first example in docs run without modification?
- Do keyboard shortcuts in docs match actual bindings?
- Does the version in docs match the version in the product?
- Do screenshots reflect the current interface?

---

## 2. The Silent Failure

Something goes wrong, but the product gives no feedback. The user does not know if it worked, failed, or is still running.

**What it looks like:**
- A command exits with code 0 but did nothing useful.
- A button click produces no visible change.
- A background process fails but the UI still shows "in progress."
- A notification is suppressed by the OS, and the product assumes it was seen.
- A network request times out silently.
- A config file is invalid, but the product starts anyway with broken defaults.
- An error is logged internally but never surfaced to the user.

**Why it confuses:** The user is in limbo. They cannot tell if they should wait, retry, or debug. They may waste hours before discovering the failure. They may assume success and make downstream decisions based on false confidence. Silent failures erode trust more than loud failures — at least loud failures tell you something happened.

**Real cases:**
| The action | What was silent |
|---|---|
| Running a deployment command | Command returned immediately. Nothing was deployed. Exit code was 0. |
| Sending a desktop notification | Focus Assist suppressed it. No feedback to user or calling script. |
| Running a cron-like scheduler | One-off jobs silently did nothing on Unix. No error, no log. |
| Clicking "Save" | Page refreshed. No confirmation. User did not know if it saved. |
| Calling an API endpoint | Rate limit hit. Response was empty. No error body. |

**What to check:**
- After any action, does the user receive confirmation?
- Are there operations that exit cleanly but may have failed?
- Does the product have debug/verbose modes that reveal hidden failures?
- What happens when a background operation fails?
- What happens when an external dependency is unavailable?

---

## 3. The Unwinnable Game

The user is stuck and there is no way out. No error message points to a solution. No help text explains the situation. No workaround exists.

**What it looks like:**
- Installation fails with an error that has no troubleshooting steps.
- Required configuration crashes in a headless environment with no alternative path.
- A file lock prevents upgrade, and the error does not say which process holds the lock.
- A form rejects input but does not say which field or why.
- A tool requires interactive input but provides no flag for automation.
- The product enters a corrupt state and provides no way to reset.

**Why it confuses:** The user hits a dead end with no information about why or how to proceed. Their only options are to abandon the task or spend hours researching. For many users, this is the point where they uninstall and never return.

**Real cases:**
| The trap | The missing exit |
|---|---|
| Windows file lock on tool directory prevents upgrade | Error says "Access denied." No indication which process holds the lock. User must guess and kill processes manually. |
| Config wizard crashes in CI pipeline | Tool requires TTY for setup. No `--non-interactive` flag. Config file corrupted as side effect. |
| CLI asks `[Y/n]` prompt | No `--yes` flag for scripting. Tool hangs forever waiting for input that will never come in CI. |
| Install requires specific dependency version | Error says "incompatible version." No suggestion of which version works. |
| Web app requires browser feature | No fallback. No error page. Just a blank screen. |

**What to check:**
- Does the product work in non-interactive environments (CI, headless, scripts)?
- Are there setup steps that cannot be skipped or automated?
- When something fails, does the error message suggest a next step?
- Can the user recover from a partially-failed state?
- Can the user reset to a known-good state?

---

## 4. The Missing Door

The user can enter a state or start an action, but they cannot exit, stop, undo, or reverse it.

**Why it confuses:** The user feels trapped. They made a decision — maybe by accident, maybe as an experiment — and now they are stuck with the consequences. This creates anxiety and reduces willingness to explore. Users will avoid features they cannot undo.

**Common symmetry violations:**
| Can... | But cannot... |
|---|---|
| Open tab | Close tab |
| Start process | Stop process |
| Create item | Delete item |
| Subscribe | Unsubscribe |
| Enable feature | Disable feature |
| Enter mode | Exit mode |
| Send message | Recall/edit message |
| Join group | Leave group |
| Push data | Pull data |
| Go forward | Go back |
| Maximize | Minimize |
| Expand | Collapse |
| Connect | Disconnect |
| Install | Uninstall |
| Lock | Unlock |
| Show | Hide |

**Real cases:**
- A browser extension could open tabs and navigate — but not go back, close tabs, or switch between them.
- A task manager could create and complete tasks — but not delete, archive, or bulk-manage them.
- An SSH manager could add hosts interactively — but not remove them non-interactively or edit existing entries.
- A settings panel could change values — but not view defaults or reset to defaults.

**What to check:**
- For every "start," is there a "stop?"
- For every "open," is there a "close?"
- For every "create," is there a "delete?"
- For every "enable," is there a "disable?"
- For every "enter," is there an "exit?"
- Can the user undo their last action?
- Can the user reset to defaults?

---

## 5. The Documentation Lie

The documentation describes a feature, behavior, or interface that does not match reality. Worse than missing docs — it actively misleads.

**What it looks like:**
- README lists keyboard shortcuts that do not work.
- Docs describe a menu item that does not exist.
- Examples use flags that have been renamed or removed.
- Help text mentions a command that does not exist.
- Configuration examples reference keys that are not recognized.
- Screenshots show a previous major version.
- The documented "getting started" path does not work.

**Why it confuses:** The user follows instructions precisely. When they fail, they assume they made a mistake. They retry. They re-read. They doubt themselves. The problem is not the user — the documentation is false. But the user does not know this. They waste time and confidence on a lie.

**Real cases:**
| What docs said | Reality |
|---|---|
| "Press Ctrl+X to run" | Alt+X runs. Ctrl+X does nothing. |
| "Install with: `tool install repo`" | This installs base only. Core features fail unless you add `[extras]`. |
| "Use --install-completion" | Help text advertises this flag. Running it produces "No such option." |
| "Version 2.2.5" (README) | Package is version 3.0.0. |
| "See examples/" | The examples directory is empty or contains broken code. |

**What to check:**
- Do documented examples actually work?
- Do shortcuts and keybindings match?
- Do menu paths and button labels match the current interface?
- Does the version in docs match the installed version?
- Are there TODO comments or placeholder text in user-facing docs?

---

## 6. The Expert Assumption

The product assumes the user knows something only the builder could know. It uses internal jargon, requires implicit steps, or expects domain knowledge the target user lacks.

**What it looks like:**
- Error messages reference internal variable names, class names, or stack traces.
- A setup step assumes the user knows which of three similar options to pick.
- An API expects parameters in an order that only makes sense given the implementation.
- A CLI flag is named after an internal concept, not a user concept.
- The user must create a config file in a specific location with specific keys — never explained.
- Dependencies are assumed to be pre-installed without documentation.

**Why it confuses:** The user feels stupid. They assume everyone else understands this. In reality, the product is built by experts for experts, and the actual target audience is much broader. The user may abandon rather than admit confusion.

**Real cases:**
| The assumption | The confused user |
|---|---|
| Install hint uses pip syntax, but user uses uv | "Install with: pip install package[extras]" — does not work with uv tool install. User must guess the equivalent. |
| Config key named "orchestrator.pipeline_strategy" | User has never heard of an orchestrator. Has no idea what values are valid. |
| Error: "KeyError: 'auth'" with stack trace | User does not know Python. The error is internal implementation detail. |
| "Requires Node.js 18+" | No check for Node.js version. User runs Node 16 and gets cryptic error. |
| Feature gated behind "edit ~/.config/app/config.toml" | No UI. No example config. User must guess syntax. |

**What to check:**
- Do error messages explain what went wrong in user terms?
- Are there setup steps that require knowledge not in the docs?
- Does the product use terminology from the implementation domain or the user domain?
- Can a user succeed without ever reading source code?
- Are defaults sensible for a newcomer?

---

## 7. The Invisible State

The product remembers things or behaves differently based on state the user cannot see, understand, or predict.

**What it looks like:**
- The product behaves differently on first run vs second run, and the user does not know why.
- A setting persists across sessions but there is no UI to view the current value.
- The product caches data and shows stale results with no indication of staleness.
- A workflow step is skipped because of an invisible flag the user set weeks ago.
- Auto-save writes to a location the user does not know about.
- A "clean" or "reset" command does not actually reset all state.

**Why it confuses:** The user cannot form a reliable mental model. The product behaves unpredictably. Actions that worked yesterday do not work today. The user feels like the product is haunted. They lose trust.

**Real cases:**
| The invisible state | The confusion |
|---|---|
| First run creates config and exits. Second run actually does the thing. | User runs in a script. First run exits 0 with no output. User thinks tool is broken. |
| Cache holds stale data from 24 hours ago. | User sees old results. No indication data might be outdated. No "refresh" button obvious. |
| Config file created in ~/.config/app/ | User uninstalls. Config remains. Reinstalls. Old config from months ago takes effect silently. |
| Session expires after 30 minutes of inactivity. | No warning. No countdown. User clicks something and is abruptly logged out mid-work. |

**What to check:**
- Does the product behave differently on first use vs subsequent uses?
- Is there state that affects behavior but cannot be viewed?
- Are there caches or auto-saves the user might not know about?
- Does the product make decisions for the user without explaining?
- Can the user predict what will happen when they take any action?

---

## 8. The Hanging Thread

An operation takes a long time or potentially forever, with no progress indicator, no cancellation, no timeout. The user does not know if it is working, stuck, or failed.

**What it looks like:**
- A terminal command prints nothing for 60+ seconds.
- A web page loads indefinitely with no spinner or progress bar.
- An API call has no timeout and hangs forever.
- A background job shows "in progress" for hours with no updates.
- A network request retries silently and infinitely.
- A processing operation has no ETA or stage indicator.

**Why it confuses:** The user is trapped waiting. They do not know if they should interrupt (risk corrupting state), wait longer (waste time), or check elsewhere. The lack of control and information is deeply frustrating.

**Real cases:**
| The hanging operation | The user's experience |
|---|---|
| Search tool runs for 120 seconds with no output | User presses Ctrl+C. Does not know if it was about to return results, was stuck, or consumed their API quota. |
| File upload with no progress bar | User stares at a spinning cursor for 10 minutes. File is 2GB. Is it even uploading? |
| npm install with no output for 5 minutes | User kills terminal. Partial install may be corrupt. Restart works. User wasted time. |
| Database migration with no feedback | User waits 30 minutes. Has no idea if it is 10% done or 90% done. |

**What to check:**
- Are there operations that can take more than 5 seconds with no feedback?
- Can long operations be cancelled?
- Is there a timeout? Is it reasonable?
- Does the user know what stage of a multi-step process they are in?
- Are network operations resilient to failure, or do they hang forever?

---

## 9. The Punishing Mistake

One wrong action — often accidental, often irreversible — causes severe consequences with no warning, no confirmation, and no recovery.

**What it looks like:**
- A single click deletes hours of work with no confirmation.
- A command with a typo destroys production data.
- Running a tool in the wrong directory recursively deletes files.
- A "clean" or "reset" command wipes all user data with no backup.
- An accidental keystroke irreversibly changes a critical setting.
- The browser back button loses all form data with no warning.

**Why it confuses:** The user loses trust instantly. They become afraid to explore. They may stop using features altogether, demanding approval workflows for every action. The product feels hostile rather than helpful.

**Real cases:**
| The punishing action | The damage |
|---|---|
| Clicking "Run" executes `rm -rf /tmp/build` instantly | No preview, no confirmation, no undo. |
| Running "nexi clean" | Wipes all search history and config. No backup. No confirmation on non-TTY. |
| Typing `bg rm 1` instead of `bg logs 1` | Kills job and permanently deletes record. |
| Refreshing a long form | All data lost. No autosave. No draft. |

**What to check:**
- Are there destructive actions with no confirmation?
- Can accidental input cause irreversible damage?
- Is there an undo mechanism?
- Is there a trash, recycle bin, or recovery mechanism?
- Are "nuclear" commands too easy to trigger accidentally?
- Does the product visually distinguish safe from dangerous actions?

---

## 10. The Incomplete Lifecycle

The product handles the beginning of a workflow well but misses steps in the middle or end. The user starts confidently but gets stranded partway through.

**What it looks like:**
- You can create a project but cannot archive or delete it.
- You can start a task but cannot pause, cancel, or reopen it.
- You can send a message but cannot edit, recall, or view it later.
- You can upload a file but cannot replace, version, or delete it.
- You can invite a user but cannot revoke access or change permissions.
- You can enter search criteria but cannot save or share the search.
- You can configure a feature but cannot view current config or reset.

**Why it confuses:** The user invests energy in the early steps, forming a positive impression. Then they hit a wall. The product feels half-finished. They have partially completed work they cannot finish or clean up. Clutter accumulates until the product becomes unusable.

**Real cases:**
| The half-lifecycle | The stranded user |
|---|---|
| Create document → Publish. No draft, no schedule, no delete. | Ten test documents clutter workspace. No way to clean up. |
| Start training job → ... no pause, no stop without losing history. | GPU memory is tied up. User must kill process and lose logs. |
| Add SSH host → Connect. No edit, no update, no remove without losing history. | Changed hostname? Must delete and re-add. Lose color-animal name. |
| Create API key → Use it. No list existing keys, no revoke, no rotate. | Unknown how many keys exist. Security risk. |

**What to check:**
- Map the full lifecycle of each major entity: create → modify → view → share → archive → delete.
- Map each workflow: start → monitor → pause → resume → complete → review.
- Are there entities that can be created but never removed?
- Are there workflows that start but have no defined end state?
- Can the user gracefully exit any state they enter?

---

## How to Use These Patterns

When you find something wrong during dogfooding, do not just describe it. **Classify it** using these patterns. This helps the product owner understand not just the symptom but the category of failure.

Example finding format:

```
### [Priority]. The [Confusion Pattern]: [Finding Title]
- **What the user was trying to do**: A developer wanted to stop a long-running background job
  to free up resources, but keep the job logs for later review.
- **What went wrong**: The tool only provides `rm` which kills AND deletes the record.
  There is no way to stop without destroying history.
- **Pattern**: The Missing Door — can start a process but cannot stop it.
- **What it should do instead**: Add a `stop` command that terminates the process
  but preserves the job record and logs.
```

**Multiple patterns often apply to one finding.** The Promise Gap often coexists with The Documentation Lie. The Unwinnable Game often contains Silent Failures. Name them all.
