# Taxonomy Guidelines

## Goal

Taxonomy exists to improve retrieval, coverage, and future thinking.
It is not decoration.

## Start simple

Begin with a small top level that reflects how someone will later look for material.
Good first-cut categories often include:

- concepts
- components or subsystems
- procedures
- troubleshooting or edge cases
- examples or case patterns
- tools, environments, or dependencies

Use a different top level if the domain naturally wants one.

## Boundary rule

For every node, write:

- what belongs here
- what does not
- nearby nodes it is often confused with

This matters more than achieving perfect hierarchy.

## Synonym rule

Track common alternate names, abbreviations, and user-language labels.
Future retrieval often depends on these more than the formal preferred label.

## Relationship rule

When useful, record relationships beyond parent-child:

- related to
- prerequisite for
- often confused with
- contrast with
- implemented by

Do not over-formalize if the corpus is still young.

## Growth rule

Split a node when one of these happens:

- it becomes too large to browse comfortably
- it mixes multiple kinds of retrieval questions
- users keep searching within it for clearly separable subtopics

Merge nodes when:

- boundaries are artificial
- repeated cross-linking shows they are functionally one area
- the distinction creates more confusion than clarity

## Coverage checks

Review taxonomy quality by asking:

- which nodes are empty or thin
- which nodes are overloaded
- which recurring user questions have no clean home
- which synonyms keep appearing but are not represented

Use these findings to update `gaps.md`.
