# Taxonomy

This essence organizes material into categories and hierarchy. Use it when the source defines classes, families, levels, or a classification system.

## Use when

- The source defines categories, levels, families, or inclusion boundaries.
- The reader needs a stable classification tree rather than a network graph or narrative.

## Do not use when

- The main value is relations between named entities rather than parent-child grouping.
- The source is really comparing options or preserving recurring themes instead of classification logic.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve boundaries, scope notes, and stable labels, but do not add menu design, page hierarchy, or visual grouping instructions here.

## Best editable shape

Prefer YAML.

```yaml
essence: taxonomy
taxonomy:
  - name: <category>
    children:
      - name: <subcategory>
        children: []
    definition: <what belongs here>
```

## What good taxonomy content does

- Creates categories people can actually use consistently.
- Gives the hierarchy a reason to exist beyond aesthetics.
- Clarifies what belongs where and why.

## Common failure modes

- Overlapping categories with fuzzy boundaries.
- Catch-all buckets that hide classification problems.
- Naming schemes that drift across levels.

## Preserve from the source

- Category intent, inclusion and exclusion boundaries, and examples.
- Stable labels or IDs when continuity matters.
- Ambiguous items, synonyms, and deprecated labels.

## Pre-save checks

- Categories are distinguishable enough to classify reliably.
- The hierarchy is supported by the source, not invented for neatness.
- Scope notes prevent obvious misclassification.
