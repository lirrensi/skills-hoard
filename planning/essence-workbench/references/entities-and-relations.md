# Entities and relations

This essence models who or what matters in the source and how those things connect. Use it when the source describes systems, organizations, ecosystems, or networks.

## Use when

- The source describes a system of actors, objects, concepts, or components linked to each other.
- The future reader will need stable identities and explicit relationship labels.

## Do not use when

- The source is mostly a category hierarchy and belongs in a taxonomy.
- The main value is prerequisites, chronology, or stakeholder stance rather than network structure.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve stable names, relation direction, and important attributes, but do not turn the graph into diagram layout instructions or visual grouping notes here.

## Best editable shape

Prefer YAML.

```yaml
essence: entities-and-relations
entities:
  - id: <stable-id>
    name: <entity name>
    type: <person|org|place|thing|concept>
    attributes:
      <key>: <value>
relations:
  - from: <entity-id>
    relation: <verb phrase>
    to: <entity-id>
    evidence:
      - <source note>
```

## What good entities-and-relations content does

- Models the real domain cleanly enough that later edits stay stable.
- Separates identity, attributes, and relationships instead of blending them.
- Uses relation labels that say what the connection actually means.

## Common failure modes

- Inconsistent naming that creates duplicate entities.
- Vague relations like "related to" that hide structure.
- Flattening complex systems into disconnected lists.

## Preserve from the source

- Original terminology, roles, and important attributes.
- Direction, type, and strength of relationships when known.
- Evidence for non-obvious links.

## Pre-save checks

- Each entity has a stable identity and is not a disguised attribute.
- Each relation is explicit enough to be interpretable later.
- Alias conflicts, duplicates, and missing directions are resolved.
