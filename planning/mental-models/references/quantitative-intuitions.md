# Quantitative Intuitions Library

How numbers, time, and distributions actually behave — and why your intuitions about them are probably wrong.

---

## Distributions & Shape

| Model | What It Is | Why Your Intuition Fails |
|-------|-----------|-------------------------|
| **Power Laws vs Normal Distributions** | Most things aren't bell curves. In power laws, a少数 items dominate (80/20 rule). Wealth, city sizes, startup returns, content virality, earthquakes — all power law. | We're trained to think in averages and bell curves. In power law domains, the average is meaningless and the extremes are everything. |
| **Nonlinearity** | Inputs and outputs aren't proportional. Doubling the input doesn't double the output — it might 10x it or halve it. | We expect linear relationships. "10x effort = 10x result" is almost never true. Small causes can have large effects (and vice versa). |
| **Convexity / Concavity** | Convex = upside bigger than downside (good). Concave = downside bigger than upside (bad). Taleb's barbell strategy: mostly safe +少量 risky bets. | We don't naturally think in terms of payoff shape. A strategy with 90% chance of small gain and 10% chance of huge loss is concave (bad) even though it "usually works." |

---

## Time & Change

| Model | What It Is | When to Use |
|-------|-----------|-------------|
| **Mean Reversion** | Extreme performance tends to return toward the average. Sports Illustrated cover jinx — being on the cover means you just had an outlier performance, which will likely regress. | Evaluating hot streaks, outliers, "track records." Punishing someone for regression after an outlier is unfair. Rewarding someone for regression after a slump is also unfair. |
| **Path Dependence** | Where you can go depends on where you've been. Early choices constrain later options. QWERTY keyboard, technology standards, career paths. | Career planning, technology adoption, relationships. Small early decisions can have outsized long-term effects. But also: don't overestimate lock-in — paths can be changed, just at a cost. |
| **Lindy Effect** | The longer something non-perishable has survived, the longer it's likely to survive. A book that's been read for 100 years will probably be read for another 100. A book published last year? Uncertain. | Book selection, technology bets, tradition, institutions. Trust things that have survived many shocks. Be skeptical of the new and untested. |
| **S-Curves** | Growth starts slow, goes exponential, then plateaus. Technology adoption, skill learning, market maturity, epidemics — all follow S-curves. | Technology adoption (where are we on the curve?), skill learning (the slow start is normal, don't quit), market analysis (is this market饱和?). |
| **Hysteresis** | System doesn't return to original state when cause is removed. You can't un-ring a bell. | Trauma, organizational culture, environmental damage, broken trust. Some things, once changed, stay changed even if you remove the cause. |
| **Temporal Discounting** | We systematically undervalue future rewards vs present ones. $100 today feels worth more than $110 next week, even though that's a 520% annual return. | Habits, saving, health, long-term planning. The discount curve is psychological, not rational. Use commitment devices to fight it. |

---

## Probability & Risk

| Model | What It Is | Why Your Intuition Fails |
|-------|-----------|-------------------------|
| **Regression to the Mean** | Extreme measurements are followed by less extreme ones. This is statistical, not causal. | We see因果 where there's only statistics. "I praised them and they got worse" — maybe they were just回归 to average. "I criticized them and they improved" — same thing. |
| **Fat Tails** | In some domains, rare events are more common and more extreme than normal distributions suggest. The biggest event dominates everything. | We underestimate tail risk. "It's never happened before" doesn't mean it won't. In fat-tailed domains, past data is unreliable for prediction. |
| **Ergodicity** | Ensemble average ≠ time average for a single individual. "Average return" can be positive while every individual path leads to ruin. Russian roulette with 100 chambers and $1 million per pull. | Personal risk, investing, "would you play this game 1000 times?" If you can't survive to play again, the ensemble average is irrelevant. |
| **Base Rates** | The statistical average outcome for this class of events. The outside view. | Before considering specific evidence, start here. "Most startups fail" is a base rate. "But this one is different" is inside view. Both matter, but start with base rate. |

---

## Compounding & Accumulation

| Model | What It Is | When to Use |
|-------|-----------|-------------|
| **Compounding** | Small consistent gains accumulate dramatically over time. 1% daily improvement = 37x in a year. | Learning, investing, relationships, habits. The early阶段 feels slow and pointless. That's normal. The magic happens later. |
| **Diminishing Returns** | Each additional unit of input produces less output. The 10th hour of study teaches less than the 1st. | Resource allocation, optimization, "when to stop." Knowing when to stop optimizing is as important as knowing how to optimize. |
| **Threshold Effects** | Nothing happens until a critical point, then everything changes. Water doesn't gradually boil — it's liquid at 99°C and gas at 101°C. | Tipping points, viral growth, habit formation, skill acquisition. The early stages feel like nothing is working. Keep going until the threshold. |

---

## Measurement & Goodhart

| Model | What It Is | When to Use |
|-------|-----------|-------------|
| **Goodhart's Law** | When a measure becomes a target, it ceases to be a good measure. People optimize for the metric, not the underlying goal. | KPIs, performance reviews, education (teaching to the test), software metrics (lines of code). Any time you measure something, ask: "How could this be gamed?" |
| **McNamara Fallacy** | Making decisions based solely on quantitative metrics because they're easy to measure, while ignoring qualitative factors because they're hard to measure. | "If you can't measure it, it doesn't exist" is dangerous. The most important things (trust, creativity, culture) are often hardest to measure. |
| **Simpson's Paradox** | A trend appears in different groups but disappears or reverses when the groups are combined. Aggregated data can mislead. | Medical studies, university admissions, any time you're looking at aggregate statistics. Always check if the trend holds within subgroups. |

---

## How to Use This Library

These models correct systematic errors in quantitative thinking:

1. **When looking at performance data** → Check for mean reversion, base rates, small sample sizes
2. **When assessing risk** → Check for fat tails, ergodicity, tail risk
3. **When planning over time** → Check for compounding, S-curves, threshold effects
4. **When measuring things** → Check for Goodhart's Law, McNamara fallacy, Simpson's paradox
5. **When evaluating distributions** → Ask "is this normal or power law?" — the answer changes everything

**Key insight:** The most dangerous quantitative error is assuming normal distributions in power law domains. If you're in a power law world (startups, content, careers, markets), the average is meaningless and the extremes are everything. Plan accordingly.
