# Starter Catalog

Use this file only when choosing a starter.

Workflow:

1. Match the request to a family.
2. Pick the closest starter in that family.
3. If nothing is close enough, build from scratch.

Do not browse the whole catalog unless the fit is genuinely unclear.

## Hybrid Briefs

For artifacts that should work as a long-read, a focus view, and a slide-like presentation.

| Starter              | File                                                | Best for                                              |
| -------------------- | --------------------------------------------------- | ----------------------------------------------------- |
| Narrative Brief      | `starters/narrative-brief/brief.html`               | Generic story shell, strategy memos, executive briefs |
| Decision Brief       | `starters/decision-brief/decision.html`             | Recommendations, trade-offs, structured decisions     |
| Proposal Comparison  | `starters/proposal-comparison/comparison.html`      | Vendor comparisons, concept bake-offs, option reviews |
| Annotated Review     | `starters/annotated-review/review.html`             | Reviews, markup, redlines, critique                   |
| Approval Brief       | `starters/approval-brief/approval.html`             | Sign-off flows, go/no-go decisions                    |
| Policy Playbook      | `starters/policy-playbook/playbook.html`            | Policies, role-aware handbooks, operating rules       |
| Training Module      | `starters/training-module/module.html`              | Lessons, enablement, workshop-style teaching          |
| Status Readout       | `starters/status-readout/readout.html`              | Weekly updates, program health, leadership reviews    |
| Meeting Brief        | `starters/meeting-brief/meeting.html`               | Meeting pre-reads, agenda + context, meeting records  |
| Evidence Explainer   | `starters/evidence-explainer/explainer.html`        | Claims + proof, methods, trust-heavy narratives       |
| Roadmap Story        | `starters/roadmap-story/roadmap.html`               | Timelines, phased plans, multi-quarter stories        |
| Onboarding Path      | `starters/onboarding-path/onboarding.html`          | Role-based onboarding and enablement journeys         |
| Incident Brief       | `starters/incident-brief/incident.html`             | Incident recaps, postmortems, reliability reviews     |
| Prioritization Board | `starters/prioritization-board/prioritization.html` | Initiative ranking, cut lines, prioritization debates |
| Launch Brief         | `starters/launch-brief/launch.html`                 | Product launches, rollout reviews, launch planning    |

## Living Documents

For browser-native replacements of static office files.

| Starter            | File                                      | Best for                                               |
| ------------------ | ----------------------------------------- | ------------------------------------------------------ |
| Recipe Wizard      | `starters/recipe-wizard/wizard.html`      | Step-by-step recipes, tutorials, guided instructions   |
| Finance Calc       | `starters/finance-calc/calculators.html`  | Financial calculators, planning tools                  |
| Changelog          | `starters/changelog/changelog.html`       | Release notes, version history, upgrade guidance       |
| Resume Portfolio   | `starters/resume-portfolio/resume.html`   | Resume, CV, personal portfolio                         |
| Contract Doc       | `starters/contract-doc/contract.html`     | Contracts, legal docs, redline review                  |
| Cover Letter       | `starters/cover-letter/cover-letter.html` | Cover letters, application tracking                    |
| Interactive Report | `starters/interactive-report/report.html` | Filterable reports, assumptions, drill-down narratives |
| Runbook            | `starters/runbook/runbook.html`           | SOPs, onboarding docs, checklists, team guides         |

## Presentations

For deck-first work that does not need a hybrid shell.

| Starter        | File                                   | Best for                                                    |
| -------------- | -------------------------------------- | ----------------------------------------------------------- |
| Business Deck  | `starters/reveal/business-deck.html`   | Stakeholder presentations, business storytelling            |
| Technical Deck | `starters/reveal/technical-deck.html`  | Technical reviews, code-heavy decks                         |
| Slideshow      | `starters/slideshow/presentation.html` | Lightweight custom slide decks without framework complexity |

## Data + Visualization

For charts, dashboards, maps, and node-link visuals.

| Starter           | File                                            | Best for                                                 |
| ----------------- | ----------------------------------------------- | -------------------------------------------------------- |
| D3 Bar Chart      | `starters/d3/bar-chart.html`                    | Ranked comparisons, bars, labels, simple animated charts |
| D3 Line / Area    | `starters/d3/line-area-chart.html`              | Time series, trend lines, layered data                   |
| Chart Dashboard   | `starters/chart-dashboard/dashboard.html`       | Multi-chart metric views                                 |
| Leaflet Map       | `starters/map/leaflet-map.html`                 | Geo data, markers, map-based storytelling                |
| Cytoscape Network | `starters/cytoscape-network/network-graph.html` | Relationship maps, system connections, knowledge graphs  |

## Tools + Reactive UI

For calculators, mini-apps, interactive canvases, and browser tools.

| Starter       | File                                       | Best for                                       |
| ------------- | ------------------------------------------ | ---------------------------------------------- |
| Alpine UI     | `starters/alpine-ui/interactive-tool.html` | Forms, generators, calculators, interactive UI |
| Preact App    | `starters/preact-app/component-app.html`   | Small component-based apps                     |
| Fabric Canvas | `starters/fabric-canvas/whiteboard.html`   | Whiteboards, drag/drop, drawing tools          |

## Data Exploration

For inspecting and editing structured data.

| Starter         | File                                       | Best for                                     |
| --------------- | ------------------------------------------ | -------------------------------------------- |
| CSV Explorer    | `starters/csv-explorer/csv-viewer.html`    | CSV drag/drop viewing, sorting, searching    |
| JSON Explorer   | `starters/json-explorer/json-tree.html`    | JSON tree inspection and search              |
| Tabulator Table | `starters/tabulator-table/data-table.html` | Interactive tables, spreadsheet-like editing |

## Creative + Browser-Native Visuals

For visual experiments and non-document browser work.

| Starter     | File                                     | Best for                                            |
| ----------- | ---------------------------------------- | --------------------------------------------------- |
| SVG Art     | `starters/svg-art/generative-svg.html`   | SVG-based procedural visuals                        |
| p5 Canvas   | `starters/p5-canvas/generative-art.html` | Generative art, simulations, playful visual systems |
| Three Scene | `starters/three-scene/3d-starter.html`   | 3D scenes and spatial views                         |

## Document Surface

For readable long-form pages without a more specific shell.

| Starter      | File                                  | Best for                                        |
| ------------ | ------------------------------------- | ----------------------------------------------- |
| Markdown Doc | `starters/markdown-doc/document.html` | Articles, notes, readable markdown-driven pages |

## Diagrams

For syntax-first visuals where the source format matters more than a polished shell.

| Family   | Files                     | Best for                                     |
| -------- | ------------------------- | -------------------------------------------- |
| Mermaid  | `starters/mermaid/*.mmd`  | Flows, sequences, states, ERDs, architecture |
| Markmap  | `starters/markmap/*.md`   | Mind maps from markdown outlines             |
| Graphviz | `starters/graphviz/*.dot` | Trees, clusters, dependency and system maps  |

## Quick Picks

If the request sounds like this, start here:

- "make this a readable doc and a presentation" -> Hybrid Briefs
- "replace my PDF / doc / memo" -> Living Documents or Hybrid Briefs
- "show metrics" -> Data + Visualization
- "make a calculator or form" -> Tools + Reactive UI
- "explore this CSV / JSON" -> Data Exploration
- "draw a system / flow / sequence" -> Diagrams
- "make a polished deck" -> Presentations
- "make something weird and browser-native" -> Creative + Browser-Native Visuals
