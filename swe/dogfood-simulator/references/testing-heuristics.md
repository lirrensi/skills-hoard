# Testing Heuristics by Product Type

Different products need different testing approaches. These are universal heuristics that apply to any product of each type, with no assumptions about specific technologies or frameworks.

---

## CLI Tools

### Installation Experience
- Copy the install command from the README into a clean environment. Run it. Does it work?
- Try installing in a directory with spaces in the path.
- Try installing with different package managers (if multiple are documented).
- Try upgrading after installing. Does it break existing config or state?
- Try uninstalling. Are there leftover files, config, or state?
- Try installing without optional dependencies. Do core features fail gracefully?

### First Run
- Run the tool with no arguments. What happens?
  - Does it crash?
  - Does it show help? Is the help useful?
  - Does it silently do something the user did not expect?
- Run `--help`. Is every subcommand listed? Are flags explained?
- Run `--version`. Does it match the README and package file?
- Try `--help` on a subcommand. Is it specific and useful?

### Core Workflow
- Pick the main job from the README. Can you complete it using only `--help`?
- Try piping input: `echo "data" | tool process`
- Try redirecting output: `tool list > out.txt`
- Try chaining with other tools: `tool list | grep pattern | tool process`
- Try with invalid input: wrong type, missing required arg, typo in flag name
- Try with extremely long input
- Try with empty input
- Try with special characters, emoji, unicode

### State and Config
- Run it twice in a row. Is the behavior consistent?
- Change a config value. Does it take effect?
- Remove the config file. Does it regenerate with sensible defaults?
- Run in a directory that has no prior state. What happens?
- Check: is there a way to see current config? To validate config? To reset?

### Automation / Non-Interactive
- Try running in CI mode (pipe /dev/null to stdin, or equivalent)
- Does it hang waiting for interactive input? Is there a `--yes` or `--non-interactive` flag?
- Do error messages go to stderr? Does normal output go to stdout?
- Are exit codes meaningful? (0=success, non-zero=failure, different codes for different failures?)
- Can output be parsed? Is there a `--json` or `--plain` output mode?

### Long-Running Operations
- Start something that takes a while. Is there a progress indicator?
- Can you cancel it? (Ctrl+C, timeout flag, kill command)
- Does it leave clean state when cancelled?

---

## Web Applications

### Landing and First Impression
- Open the main URL. What do you see in 3 seconds? Is it clear what the product does?
- What is the first thing a user should do? Is it obvious?
- Try on mobile viewport. Is it usable?
- Try with JavaScript disabled. Is there any useful content?
- Try with a screen reader (or imagine one). Can a visually impaired user navigate?

### Primary Workflow
- Complete the main task without reading documentation. Can you?
- Where do you get stuck? How long until you need help?
- Try the workflow backwards: e.g., try to view or edit before creating. Does it guide you?
- Try the workflow partially, leave, and return. Is your state preserved?
- Try the workflow on a slow connection. Does it handle gracefully?

### Navigation
- Can you always get back to where you were?
- Does the browser back button work?
- Are there breadcrumbs or clear location indicators?
- Can you deep-link to a specific page or state?
- What happens if you open two tabs and work in both?

### Forms
- Submit empty. What happens?
- Submit with invalid data. Are errors clear? Are they next to the relevant field?
- Submit with very long data. Does it truncate? Reject? Scroll?
- Submit, then refresh. Does it resubmit? (POST-redirect-GET pattern?)
- Submit, then go back. Is your data preserved?
- Leave the form, come back 30 minutes later. Is your data still there?

### State and Feedback
- After any action, do you know it worked? (Confirmation, toast, visual change?)
- After any action, do you know what to do next?
- If something fails, do you know why and how to fix it?
- Is there a loading state for every async operation?

### Edge Cases
- What happens with a very large dataset (10,000 rows in a table)?
- What happens when the server is slow (simulate via throttling)?
- What happens when the network drops mid-operation?
- What happens with concurrent edits (two users editing the same thing)?

---

## APIs and Libraries

### Getting Started
- Import the library. Does it work? Any unexpected dependencies?
- Call the main function with the simplest possible arguments. Does it return what you expect?
- Is the first example in the README copy-paste runnable?
- Are there types/annotations? Do they match actual behavior?

### Documentation Quality
- Does every public function/endpoint have a description?
- Are parameter types and return types clear?
- Are error conditions documented?
- Is there a "cookbook" or "recipes" section for common tasks?
- Is the changelog accurate and up to date?

### Error Handling
- Pass invalid types. Is the error clear?
- Pass None/null/undefined where not expected. What happens?
- Call methods in the wrong order. Is there guidance?
- Exceed rate limits or quotas. Is the error actionable?
- Induce a network failure. Does it retry? Time out? Crash?

### Consistency
- Do similar functions have similar signatures?
- Do error responses have a consistent shape?
- Is pagination consistent across list endpoints?
- Are enum/constant values consistent in naming and formatting?

### Side Effects
- Does any function mutate its arguments?
- Does any function have hidden state or global configuration?
- Does any function perform I/O that is not documented?
- Is there any "magic" behavior that surprises you?

---

## IDE Extensions

### Installation
- Install from marketplace or VSIX. Does it activate?
- Does it show a welcome message or onboarding?
- Are the commands visible in the command palette?
- Does the extension activate only for relevant file types, or globally?

### Core Feature
- Use the main feature the extension provides. Does it work?
- Try it in different file types. Does it behave consistently?
- Try it with no file open. Does it handle gracefully?
- Try it with a very large file. Is it performant?

### UI and Interaction
- Are keyboard shortcuts documented? Do they work? Do they conflict with defaults?
- Is there a settings page? Can users customize behavior?
- Are there status bar items, decorations, or CodeLens that are clear?
- Do actions provide feedback? (Notification, status bar message, etc.)

### Safety
- Can a user undo an action performed by the extension?
- Are there destructive actions without confirmation?
- Does the extension ask for more permissions than it needs?

### Discoverability
- Can a user find all features through the command palette?
- Is there a README or in-editor help?
- Are features grouped logically in menus?

---

## Browser Extensions

### Installation
- Install from store or load unpacked. Does it work?
- Are the permissions reasonable? Does it request more than it needs?
- What happens when you first install? Is there onboarding?

### Popup / UI
- Click the extension icon. What happens?
- Is the popup usable at different sizes?
- What happens when you click outside the popup? Does it close cleanly? Lose state?

### On Real Pages
- Use the extension on various websites. Does it break any?
- Does it interfere with normal browsing?
- Does it work on popular sites (search engines, social media, email)?
- What happens on pages with dynamic content (SPAs, infinite scroll)?

### Configuration
- Can users configure the extension? Where?
- Can users disable specific features without uninstalling?
- Is there a way to report issues or get help?

---

## Desktop Applications

### Installation
- Is the installer size reasonable?
- Does installation require admin privileges unnecessarily?
- Are there bundled dependencies that should be opt-in?
- Is there an uninstaller? Does it clean up completely?

### First Launch
- Does the app open quickly?
- Is there a welcome screen, tutorial, or sample data?
- Are the defaults sensible for a new user?

### Core Workflow
- Complete the primary task. How many clicks? How many decisions?
- Is there a "quick start" path that skips configuration?
- Can you pick up where you left off after closing and reopening?

### Window Management
- Does the app remember window size and position?
- Does it handle multiple monitors correctly?
- Does it handle minimize to tray / background?

### Performance
- Does the app feel responsive?
- Does it handle large files or datasets?
- Does it consume unreasonable CPU/memory at idle?

### Accessibility
- Can you navigate entirely by keyboard?
- Are there keyboard shortcuts for common actions?
- Is the text readable at high DPI / different scaling settings?

---

## Mobile Applications

### Installation
- Is the app size reasonable?
- Does it request permissions at appropriate times, or all at launch?
- Can you use the app without granting all permissions?

### First Launch
- Is there a tutorial or onboarding that can be skipped?
- Are defaults sensible?
- Does it work in airplane mode / offline?

### Navigation
- Can you always go back?
- Is the back button behavior consistent with platform conventions?
- Are you ever stuck in a screen with no clear exit?

### Input
- Are touch targets large enough? (Minimum 44x44 pt)
- Does the keyboard not cover input fields?
- Are forms scrollable when the keyboard is visible?

### Platform Conventions
- Does it follow iOS/Android design patterns?
- Does it support dark mode?
- Does it respect system font size settings?

---

## General: How to Approach Any Product

### The First 60 Seconds
This is the critical window. Ask:
1. Did installation work from the documented command?
2. Did the first run produce something useful, or an error?
3. Did I know what to do next, or was I lost?

### The Happy Path
Pick the ONE thing the product claims to do best. Complete it. Ask:
1. Could I do it without reading beyond the README?
2. Did I hit any surprises, dead ends, or confusions?
3. Did the product communicate what happened at each step?

### The Reality Path
Now try a slightly messier version of the same task:
1. What if I skip a step? Does it guide me back?
2. What if I do things out of order? Does it handle it?
3. What if I make a typo? Is the error helpful?
4. What if I have to stop and resume? Is state preserved?

### The Power User Path
Now try what an advanced user would do:
1. Can I do this in bulk? (10, 100, 1000 items)
2. Can I automate this? (script, API, CLI flags)
3. Can I customize this? (settings, preferences, config)
4. Can I export or share my results?

### The Unexpected Path
Try what "nobody would do" — because someone will:
1. Run the wrong command in the wrong directory
2. Click the wrong button because it looked like the right one
3. Type garbage into every field
4. Close the app mid-operation
5. Run two instances concurrently
