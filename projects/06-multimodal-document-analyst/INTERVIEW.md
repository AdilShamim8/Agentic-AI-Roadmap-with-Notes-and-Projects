# Interview guide - Project 06: Multimodal document analyst

Status: beta | For: presenting this project in interviews | Related: [project README](README.md), [project stories](../../10-interview-preparation/15-project-stories.md)

## The pitch

"Routed extraction: documents arrive as mixed PDFs - text, tables, images - and a router sends each element to the right extractor. Per-modality validators run before the merge node, so a bad extraction fails loudly at its layer instead of poisoning the merged result."

## The whiteboard script

1. The router node - classifies each element's modality (structured output, not vibes).
2. The parallel extractors - text, table, image - each emitting a typed partial result.
3. The validators - per-modality schema checks; failures captured per element with markers, not dropped.
4. The merge node - combines validated partials into the document's structured representation.
5. The eval - extraction accuracy per modality, so a table regression is visible as a table regression.

The line that earns the nod: "Validation happens before the merge, so one bad page cannot poison the document."

## The numbers you quote

- Per-modality accuracy on your eval set (field-level, not document-level - the honest metric).
- The routing confusion matrix if you built one; routing here is classification, same machinery.

## The follow-ups

- "Why route at all instead of one multimodal call?" Cost and precision: specialized extractors beat one general call per element type, and routing failures localize to a measurable classifier instead of a mysterious general model.
- "What about page images with diagrams?" Extract text at ingest, defer multimodal indexing to a phase two with its own eval - scope honesty beats hand-waving.
- "How do table extractions fail?" Merged cells, multi-page tables, unit loss - hence the table validator checking row counts and type consistency before merge.
- "Where does the LLM sit?" Routing and the hard extractions; deterministic parsing handles structure the format gives away for free.

## The red flags

- "We send the whole PDF to the model" - the unbounded-context answer.
- No validation layer between extraction and merge.
- Document-level accuracy as the only metric - it hides exactly the per-modality regressions the design exists to catch.

## What this project proves

Structured-output discipline, per-layer validation, and the routing-as-classification mindset that document-heavy roles screen for.
