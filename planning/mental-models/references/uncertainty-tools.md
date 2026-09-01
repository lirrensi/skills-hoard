# Uncertainty & Probability Tools

How to think clearly when you don't know for sure.

---

## Core Tools

| Tool | What It Is | When to Use |
|------|-----------|-------------|
| **Expected Value** | Probability × Impact. Think in distributions, not point estimates. | Any decision with uncertain outcomes |
| **Base Rates** | What's the statistical average for this class of events? | Before considering specific evidence — start here |
| **Bayesian Updating** | Start with prior belief, update proportionally to evidence | Ongoing learning, forecasting, diagnosis |
| **Calibration** | How well do your confidence levels match reality? (If you say 80%, are you right 80% of the time?) | Self-assessment, prediction, trust in your own judgment |
| **Fat Tails / Tail Risk** | Rare events are more common and more extreme than normal distributions suggest | Risk management, black swans, insurance, investing |
| **Scenario Planning** | Think in multiple possible futures, not one prediction | Strategic planning, uncertainty-heavy decisions |
| **Sensitivity Analysis** | Which assumptions matter most? Vary inputs, see which change the output | Modeling, planning, "what should I worry about?" |
| **Value of Information** | Is it worth gathering more data before deciding? | Research decisions, "should I analyze more or act now?" |

---

## Probability Intuitions (What People Get Wrong)

| Intuition | The Reality |
|-----------|-------------|
| "It's unlikely, so it won't happen" | Unlikely events happen all the time across many trials |
| "It happened, so it was likely" | Hindsight bias — rare events feel predictable after the fact |
| "This specific scenario is probable" | Specific scenarios are almost always less probable than the category |
| "Small samples tell the full story" | Small samples have high variance — don't trust them |
| "Independent events affect each other" | Gambler's fallacy — past coin flips don't change the next one |
| "I can predict the outcome" | Overconfidence — most people are poorly calibrated |

---

## Calibration Practice

| Confidence | Meaning | Calibration Test |
|------------|---------|-----------------|
| 50% | "I'm basically guessing" | Should be right about half the time |
| 70% | "I think this is probably true" | Should be right 7 out of 10 times |
| 90% | "I'm quite sure" | Should be right 9 out of 10 times — and wrong 1 out of 10 |
| 99% | "I'd be shocked if wrong" | Should be wrong 1 in 100 times — if you're never wrong at 99%, you're underconfident |

**Key insight:** If you're never surprised, you're not taking enough risk in your predictions. If you're often surprised, you're overconfident.

---

## Decision-Making Under Uncertainty

### When to decide fast vs slow:

| Condition | Speed |
|-----------|-------|
| Decision is reversible | **Fast** — decide, learn, adjust |
| Decision is irreversible | **Slow** — gather more information |
| Stakes are low | **Fast** — don't overthink |
| Stakes are high + irreversible | **Slow** — but set a deadline to avoid analysis paralysis |
| You have strong base rates | **Moderate** — trust the statistics |
| You're in a novel situation | **Slow** — no reliable base rates |

### The Value of Information Framework:

1. **What's the cost of being wrong?** (downside)
2. **What's the cost of waiting?** (delay cost)
3. **What's the cost of gathering more info?** (research cost)
4. **How much would new info change your decision?** (expected value of information)

If research cost < (probability of changing decision × cost of being wrong) → gather more info.
Otherwise → decide now.

---

## Fat Tails & Black Swans

Normal distributions (bell curves) don't apply to everything. In fat-tailed domains:

- **Averages are meaningless** — one event can dominate all others
- **Past data is unreliable** — the biggest event hasn't happened yet
- **Prediction is impossible** — but preparation is possible
- **Concentration is dangerous** — diversify, avoid single points of failure

**Fat-tailed domains:** finance, wars, pandemics, technology disruption, social media virality, natural disasters.

**Thin-tailed domains:** human height, test scores, manufacturing tolerances.

**Rule of thumb:** If the domain has winners that are 1000x bigger than average, it's fat-tailed. Plan accordingly.
