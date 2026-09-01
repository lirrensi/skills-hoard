# Real Dogfooding Cases

These are anonymized but real discoveries from actual dogfooding sessions. Each case includes what was found, which confusion pattern it maps to, and what the fix looked like. Use these to recognize patterns in your own testing.

---

## Case 1: The Browser Extension Missing Navigation

**Product type:** Browser automation extension
**The jobs:** "As a tester, I want to automate browser interactions for multi-page workflows, so that I can write end-to-end tests."

**What was found:**

The extension exposed functions for:
- Open tab
- Close tab
- Navigate to URL
- Click element
- Type in field
- Screenshot

**What was missing:**
- No "back" function. Users testing a checkout flow (page 1 → page 2 → page 3) could not return to verify page 2 after reaching page 3.
- No "refresh" function. Could not retry failed page loads.
- No "switch tab." Once multiple tabs were open, only the most recently opened was active.
- No "duplicate tab." Users comparing A/B versions of a page had to open each from scratch.
- No "reopen closed tab." Accidentally closing a tab was permanent.

**Patterns:** Symmetry gaps (navigate → no back), Missing lifecycle stages (tab lifecycle incomplete), The Missing Door (can open but can't switch or duplicate).

**The fix:** Added back(), forward(), refresh(), switchToTab(), duplicateTab() functions. Most were ~10 lines each — the interface surface was the only barrier.

**Lesson:** The developers implemented the "happy path" of open → navigate → close, but not the "reality path" where users need to go back, retry, compare, and manage multiple tabs. Happy path testing is insufficient — test the mess.

---

## Case 2: The Task Manager That Could Not Clean Up

**Product type:** In-repository task management CLI
**The jobs:** "As a developer, I want to track tasks in my repo, so that I know what to work on and what is blocked."

**What was found:**

The tool provided:
- Create task
- Update status (12 statuses available)
- List tasks
- Search tasks
- Close/complete tasks

**What was missing:**
- No delete function. Users created test tasks, accidental tasks, and placeholder tasks. These cluttered the workspace forever.
- No archive function. Completed tasks remained in the active list, making it hard to distinguish active from done.
- No bulk operations. Cleanup required manual status changes one at a time.
- No task dependency reversal: you could say "A blocks B" but not "B depends on A" — same relationship, different mental model. Users expected both.

**Patterns:** Incomplete lifecycle (create → update → close, but missing delete and archive), Bulk operation gaps (can update one, not many), The Missing Door (can enter tasks into system but cannot remove them).

**The fix:** Added delete command with confirmation, archive command, and batch operations. The dependency system was made bidirectional.

**Lesson:** Creators focus on the "interesting" part (task statuses, dependencies) and forget the "boring" part (cleanup, organization). Boring things matter because they accumulate — 100 completed tasks without archive is a UX disaster.

---

## Case 3: The CLI Toolkit That Promised Too Much

**Product type:** CLI tool suite with multiple sub-tools
**The jobs:** "As a developer, I want a suite of CLI productivity tools (cron, notifications, background jobs), so that I spend less time on operational tasks."

**What was found:**

The README promised:
- "Install with one command"
- "Works on all platforms"
- "Cron jobs in plain English"
- "Background jobs, tracked by name"

**What was actually discovered:**
- The one install command installed only the base package. 4 of 7 tools required extra dependencies installed with a different, undocumented syntax.
- The first example in the README used a tool that was not installed by the base command. It failed with a cryptic error about missing dependencies.
- "Cron jobs in plain English" was true for recurring jobs on all platforms. But one-off jobs ("in 5 minutes", "at 3pm") silently did nothing on Linux — the scheduler backend was a stub.
- "Background jobs, tracked by name" was true, but "stop a job" did not exist. Only "remove" existed, which killed AND deleted the history.
- Windows upgrade was impossible because background job worker processes held file locks on the installation directory.

**Patterns:** The Promise Gap (install one command → actually needs multiple), The Silent Failure (one-off jobs silently do nothing), The Missing Door (can start background job, cannot stop without destroying history), The Unwinnable Game (Windows upgrade blocked by own file locks).

**The fix:** Unified install with all extras by default, implemented the Unix scheduler backend, added stop command, fixed worker process file locking.

**Lesson:** First impressions are everything. If the first command a user runs fails, they will not try the other tools. Test the install story COLD. Test it from a clean machine. Test the very first example in the docs.

---

## Case 4: The Search Tool That Could Not Be Trusted

**Product type:** Terminal-native web search and research tool
**The jobs:** "As a researcher, I want to search the web and extract information from my terminal, so that I can research without leaving my workflow."

**What was found:**

The core function (ask a question, get a researched answer) was unreliable:
- Search would hang for 60-120 seconds with zero output — no spinner, no "searching...", no progress.
- If you ran it in a non-TTY environment (CI, IDE terminal), it crashed with a terminal error and corrupted its config file.
- If you ran it without arguments, it entered an infinite crash loop.
- It sometimes returned citations ([1], [2]) when it had performed zero web searches (empty URLs array in history). Users were given false confidence.
- The verbose mode printed the API key in plaintext.
- The "doctor" command checked 3 of 4 tools for readiness, skipping one entirely.
- The README said version 2.2.5. The package was version 3.0.0.

**Patterns:** The Hanging Thread (120s with no feedback), The Invisible State (first-run behavior changed based on hidden config), The Unwinnable Game (non-TTY crash with config corruption), The Promise Gap (citations without sources), The Documentation Lie (wrong version).

**The fix:** Added progress bars, timeouts, graceful non-TTY fallbacks, config backup before writes, version sync, source verification for citations.

**Lesson:** Reliability is the foundation. If the core value proposition (get a researched answer) fails unpredictably, no amount of features matters. Test the main job first, repeatedly, in different environments.

---

## Case 5: The Editor Extension That Could Run Anything

**Product type:** VS Code: extension for running commands from editor text
**The jobs:** "As a developer, I want to run shell commands directly from my notes or config files, so that I do not have to copy-paste between editor and terminal."

**What was found:**

The extension worked — but dangerously:
- A single click on a command instantly executed it with NO confirmation. Destructive commands (rm -rf, DROP TABLE, format C:) ran with one misclick.
- There was no preview — you could not see what would run before it ran.
- There was no edit-before-run — you could not tweak a command before executing.
- There was no "kill" — once a command started, you could not stop it from the extension (only from terminal).
- Five CodeLens buttons appeared on every command, creating visual clutter. For a file with 10 commands, there were 50 buttons.
- The README documented Ctrl+X as the shortcut. The actual binding was Alt+X, which conflicted with Linux defaults.
- The extension activated semantic token highlighting on ALL files, not just .easycmd files, impacting performance.
- The version in the .vsix file was 0.2.3. The version in package.json was 0.2.5. The README changelog was stuck at 0.1.0.

**Patterns:** The Punishing Mistake (destructive commands with one click, no confirmation), The Documentation Lie (wrong shortcuts, wrong versions), The Expert Assumption (CodeLens overload — developer thought "more buttons = more useful"), The Missing Door (can run, cannot stop).

**The fix:** Added confirmation for destructive commands, preview/edit-before-run, kill-command action, reduced CodeLens to one primary button, fixed shortcuts and versions.

**Lesson:** Safety is not a "nice to have" for developer tools. Developers run real commands on real systems. One misclick on "rm -rf /" is catastrophic. The default must be safe. Speed can come after safety.

---

## Case 6: The Notification Tool Nobody Could Verify

**Product type:** Cross-platform desktop notification CLI
**The jobs:** "As a developer, I want to send desktop notifications from scripts, so that I know when long-running tasks complete."

**What was found:**
- On Windows, notifications were silently suppressed by Focus Assist. The command exited successfully (code 0) but no notification appeared. The user had no way to know it failed.
- On all platforms, the command produced zero output on success. Scripts could not verify that notifications were sent.
- There was no way to check notification history — did the notification actually appear? No way to know.
- There was no way to configure notification duration, priority, or style.
- When piping input (e.g., `curl api/status | notify "API Check"`), the notification only showed the title, not the piped content.

**Patterns:** The Silent Failure (Focus Assist suppression with no feedback, zero output on success), Visibility gaps (no history, no status check), Missing customization.

**The fix:** Added return codes for delivery status, `--history` flag to check recent notifications, `--urgency` and `--duration` flags, and fixed piped content display.

**Lesson:** For tools used in scripts and automation, "silence" is not golden — it is terrifying. Scripts need to know if something worked. Return codes, status flags, and verbose modes are not features — they are the API contract.

---

## Case 7: The SSH Manager That Could Not Be Automated

**Product type:** SSH profile manager CLI
**The jobs:** "As a developer, I want to save and manage SSH connections by friendly name, so that I do not have to memorize IP addresses." AND "As an AI agent, I want to connect to remote servers programmatically."

**What was found:**

The tool was well-designed for human use:
- `essh add user@host` → auto-generates a memorable name (coral-fox, amber-badger)
- `essh coral-fox` → connects immediately
- `essh list` → shows all profiles

But it failed for its secondary (marketed!) audience — AI agents and automation:
- Adding a host forced an interactive `[Y/n]` prompt with no `--yes` flag
- In CI or agent contexts, the tool simply hung, waiting for input that would never come
- There was no way to pre-authorize connections non-interactively
- The error message did not explain that interactive input was required

**Patterns:** The Unwinnable Game (tool requires interaction in non-interactive context), The Promise Gap (marketed to agents but unusable by agents).

**The fix:** Added `--yes` and `--non-interactive` flags, made authorization skippable in non-TTY, improved error messages to explain the interactive requirement.

**Lesson:** If you market to two audiences, test with BOTH. The human path worked beautifully. The agent path was completely broken. One audience will discover that the other's path is blocked.

---

## Case 8: The Screenshot Tool That Lied About Failure

**Product type:** Screen capture CLI
**The jobs:** "As a tester, I want to capture screenshots from scripts, so that I can document bugs and test results."

**What was found:**

When the primary capture library was not installed:
- The tool printed "ERROR: Failed to load screenshot library" to stderr
- THEN succeeded using a fallback library
- THEN printed the saved file path to stdout

Result: script authors saw "ERROR" and assumed failure. They never noticed the file path on the last line. Scripts parsing stderr for errors falsely detected a failure.

**Patterns:** The Promise Gap (the error was not an error — the tool succeeded but communicated failure), The Silent Failure in reverse (success was hidden behind a scary error message).

**The fix:** Changed error to a warning/INFO level. Made the success message unmistakable. Separated stderr warnings from actual errors.

**Lesson:** The emotional content of console output matters. "ERROR" triggers scripts and humans alike. If the operation succeeded, do not print "ERROR." If it failed, do not print a success message.

---

## Case 9: The Config System With No Visibility

**Product type:** CLI tool with TOML configuration
**The jobs:** "As a user, I want to configure the tool's behavior, so that it works the way I need."

**What was found:**
- `tool config` opened the config file in an editor. Good.
- But there was no `tool config show` to just view the config without editing.
- There was no `tool config get [key]` to query a specific value.
- In headless/CI environments, `tool config` tried to open an editor and hung forever.
- When the config was invalid, the tool silently used broken defaults with no warning.
- There was no `tool config validate`.
- When config keys changed between versions, old configs silently broke.

**Patterns:** The Expert Assumption (assumes user knows config file location and syntax), The Unwinnable Game (editor hangs in headless), The Silent Failure (invalid config silently uses defaults), Visibility gaps (cannot view current config).

**The fix:** Added `config show`, `config get`, `config validate`, `--no-editor` flag, warnings on invalid config, migration notes on version change.

**Lesson:** Configuration is an interface like any other. If users can change something, they need to be able to VIEW current values, VALIDATE changes, and UNDERSTAND what went wrong. Config should never be a blind leap of faith.

---

## Case 10: The Web Form That Punished Mistakes

**Product type:** Web application with multi-step form
**The jobs:** "As a customer, I want to submit an order, so that I can purchase the product."

**What was found:**
- Form was 5 steps, each with 10+ fields.
- Going back a step cleared all fields on the current step.
- Refreshing the page lost ALL data across ALL steps.
- Validation errors appeared only at the bottom of the form — you had to scroll to find which field was wrong.
- On mobile, the form was nearly unusable due to small touch targets.
- After submission, there was no confirmation number on screen — only in email.
- If the email went to spam (common), the user had no proof of submission.

**Patterns:** The Punishing Mistake (browser back/refresh loses everything), The Silent Failure (validation errors hard to find), Missing visibility (no confirmation on screen).

**The fix:** Added autosave, in-field error indicators, mobile-responsive layout, on-screen confirmation with number, and "resume draft" on return.

**Lesson:** Forms are where user trust is made or broken. Every keystroke is an investment. Losing that investment (refresh, back button, timeout) is the fastest way to lose a user permanently. Autosave is not a feature — it is an apology for browsers being unreliable.

---

## Case 11: The API With Inconsistent Return Types

**Product type:** REST API library
**The jobs:** "As a developer, I want to call API endpoints and handle responses, so that I can integrate with the service."

**What was found:**
- Some endpoints returned objects. Others returned arrays. One returned a string.
- Error responses had different shapes depending on the error type.
- Some errors returned HTTP error codes. Others returned 200 with an error field.
- Pagination was sometimes in headers, sometimes in body, sometimes absent.
- The "list all" endpoint silently capped at 100 results. No indication of truncation. No pagination to get the rest.

**Patterns:** The Expert Assumption ("developers will figure out the response format"), The Silent Failure (list truncated with no indication), The Hanging Thread (developers waste time guessing response shapes).

**The fix:** Standardized response format, consistent error shape, proper HTTP status codes, explicit pagination with total/resume cues.

**Lesson:** Consistency is the API. Users do not call one endpoint — they chain them. If every endpoint has different patterns, every integration becomes a puzzle. Consistent error shapes, pagination, and response formats are not "nice to have" — they are the difference between an API people recommend and one they complain about on Twitter.

---

## Case 12: The Library With No Error Story

**Product type:** Python utility library
**The jobs:** "As a developer, I want to use this library in my project, so that I do not have to implement the functionality myself."

**What was found:**
- The main function returned None on error instead of raising an exception.
- There was no way to distinguish "no results" from "error occurred."
- Edge case inputs (empty list, None, negative numbers) caused uncaught exceptions with no documentation.
- The function mutated a passed-in list as a side effect, which was not documented.
- Type hints were present but wrong for several functions — they did not match actual behavior.

**Patterns:** The Silent Failure (None on error indistinguishable from no results), The Expert Assumption (assumes developers will read source code to understand behavior), The Punishing Mistake (side effects on parameters can cause bugs far from the call site).

**The fix:** Added custom exception hierarchy, documented edge cases, made side effects explicit or removed them, fixed type hints.

**Lesson:** Library users trust your return values and type hints. If they are wrong, bugs propagate silently through dependent code. Type hints are documentation with teeth — wrong hints are worse than no hints.

---

## Case 13: The Dashboard With No "What Now?"

**Product type:** Web analytics dashboard
**The jobs:** "As a manager, I want to understand our metrics, so that I can make data-driven decisions."

**What was found:**
- The dashboard showed beautiful charts.
- But there was no explanation of what the numbers meant. Is 50% conversion good or bad?
- There was no comparison to previous periods — is this trending up or down?
- There were no alerts for anomalous values.
- There was no way to drill down from a chart into the underlying data.
- Export was CSV only, with raw timestamps (not human-readable dates).

**Patterns:** Visibility gaps (can see metrics, cannot understand them), The Expert Assumption (assumes user knows what "good" looks like), Missing lifecycle (see data → understand → act → verify), Bulk gaps (no export to useful formats).

**The fix:** Added contextual benchmarks, trend indicators (up/down arrows), anomaly highlighting, drill-down capability, export with formatting options.

**Lesson:** Displaying data is the easy part. Making it MEANINGFUL is the hard part. A dashboard that shows numbers without context is just a fancy spreadsheet. Users need: is this good or bad? Is it getting better or worse? What should I do about it?

---

## Case 14: The CLI That Required Reading Source Code

**Product type:** CLI data processing tool
**The jobs:** "As a data analyst, I want to process CSV files from the command line, so that I can clean data before analysis."

**What was found:**
- `--help` listed flags but did not explain what they did or what values were valid.
- The README had one example. It covered the simplest case.
- All other functionality (filtering, joining, aggregating) was discoverable only by reading source code.
- Error messages for invalid input were: "ValueError: invalid literal for int() with base 10: 'abc'"
- There was no documentation for the config file format.

**Patterns:** The Expert Assumption (source code IS the documentation), The Unwinnable Game (cannot discover features without reading code), Visibility gaps (no documentation for advanced features).

**The fix:** Comprehensive help text on every flag, cookbook-style README with common recipes, error messages in domain language, documented config file with examples.

**Lesson:** If a user has to read source code to use your tool, the tool has failed. Help text and documentation are the UI of a CLI. Bad help text = broken UI.

---

## Case 15: The Extension That Activated Everywhere

**Product type:** IDE extension for a specific file format
**The jobs:** "As a developer, I want syntax highlighting and CodeLens for my custom file format, so that I can work more efficiently."

**What was found:**
- The extension activated on ALL file types, not just the custom format.
- It registered a semantic tokens provider globally, causing performance impact on every file.
- CodeLens appeared on every file, even files with no relevant content.
- The activation event was "*" — meaning it started on IDE launch, not just when relevant files were opened.

**Patterns:** The Expert Assumption (developer tested only on their own files), Performance impact that users cannot diagnose ("why is my IDE slow?").

**The fix:** Restricted activation to the specific file extension, made semantic tokens provider file-type-aware, changed activation event.

**Lesson:** Extensions should be minimal in their impact footprint. Activate only when needed. Affect only relevant files. If your extension slows down the entire IDE, users will disable it without knowing which extension is the culprit.

---

## Common Themes Across All Cases

Reading across these cases reveals recurring patterns:

1. **The happy path is always implemented.** Developers build and test the "normal" flow. The edges are where users live.
2. **Installation and first-run are neglected.** The first 60 seconds determine whether a user stays or leaves. Most products fail in those 60 seconds.
3. **Documentation rots faster than code.** Version numbers, shortcuts, screenshots — anything that can drift, will drift.
4. **Safety is an afterthought.** Confirmation dialogs, undo, preview — these are added only after someone gets burned.
5. **Power users are forgotten.** Bulk operations, shortcuts, scripting hooks — the features that keep advanced users loyal — are rarely in v1.
6. **Feedback is assumed.** "The user will know it worked" is the most dangerous assumption in product design.
7. **The second audience is invisible.** Products marketed to "developers AND CI pipelines" often work for one and break for the other.
