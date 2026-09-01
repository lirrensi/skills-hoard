---
node_type: story
title: {Short, specific title}
status: active
updated: YYYY-MM-DD
session_type: debug | implementation | migration | incident | investigation | spike | review
tags: []
links:
  relates_to: []
  documents: []
---

# {Title}

## Summary

In one paragraph: what happened, why it mattered, and what the takeaway is.

## Context

What were we trying to do? What was the system supposed to do? Include versions, environments, or relevant constraints.

## Symptom

What did we observe? Error messages, weird metrics, user reports, flaky behavior — capture the raw signal.

## Investigation

Walk through what you tried. Include dead ends. They are often the most useful part.

1. {First hypothesis and how you tested it}
2. {Second hypothesis}
3. {The thing that finally pointed to the real cause}

## Root cause

What was actually going on? Be as specific as possible. If you never fully figured it out, say so explicitly — a `mystery` status is honest and useful.

## Fix / outcome

What did you do? Did it work? Is it temporary or permanent?

## What we learned

- {Durable insight 1}
- {Durable insight 2}

## Follow-ups

- {Link to updated spec, architecture doc, or runbook}
- {Ticket or code change}
- {Thing to monitor or revisit}
