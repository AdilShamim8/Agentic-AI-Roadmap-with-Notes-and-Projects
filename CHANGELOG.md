# Changelog

All notable changes to this repository are documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning for the curriculum structure (individual chapters evolve on their own review cycles).

## [0.3.0] - 2026-10-19

### Added

- The 19 example demos the chapters promised but never shipped
  (modules 05-08), including A2A protocol v1.0 demos, real `Send`
  dynamic fan-out, durability with idempotency keys, governance with
  RBAC/audit/PII redaction, and a streaming demo using real graph
  streams
- `08-production/k8s/`: deployment, service, and HPA manifests with a
  README (the chapter's k8s link finally resolves)
- `.env.example`: the environment template the examples always
  referenced
- CI: `.github/workflows/ci.yml` (lint + keyless tests + eval) and
  `.github/workflows/eval-regression.yml` (the PR regression gate
  module 06 documents), plus a PR template
- `projects/01-how-to-pick.md`: the project-selection guide the
  projects index linked to
- A `.gitignore`

### Changed

- Dependencies moved to current versions (Oct 2026): langgraph 1.2.16,
  langchain 1.4.6, mcp 1.30.0, checkpointers as separate packages; the
  full set resolves and co-installs cleanly
- Example code made runnable, lint-clean (ruff), and type-clean
  (mypy): seven demos that carried unreachable mock-langgraph fallbacks
  were rewritten to idiomatic real-API code; tool results use
  ToolMessage; Store values use dict payloads; StructuredTool objects
  are invoked, not called
- Models: every example moved off `gpt-4o` (OpenAI API shutdown
  2026-10-23) and `temperature=0` (the 5.x Claude generation drops it);
  defaults are claude-sonnet-5-5 / claude-haiku-5-5, overridable via
  `EXAMPLES_MODEL`
- Curriculum updated to current protocols: MCP transports and revision
  notes (Streamable HTTP; the 2026-07-28 stateless revision vs the
  2025-11-25 SDK line), A2A chapters rewritten to v1.0.0
  (agent-card.json, message/send, rejected state), deployment flow
  moved to `langgraph build`, SWE-bench corrected to ~97 percent
  (Sep 2026)
- Golden dataset expanded to a real 30 rows; `run_evals.py` loads it
  and runs keyless in CI with an honest 93.3 percent baseline
- 43 chapters re-reviewed and re-dated `Last reviewed: 2026-10-19`

### Fixed

- All 29 broken internal links (21 dead example references, the
  missing k8s directory, stale projects-index claims, STYLING.md's
  nonexistent analysis/ examples)
- All 25 dead external URLs (old langgraph docs site, MCP and A2A
  spec URLs, Anthropic research pages, GitHub docs slugs); the sample
  report cites real sources instead of example.com placeholders
- The core-demo graph bug (an edge from a node that never existed -
  the graph never compiled as shipped) and its chapter example
- ROADMAP/README phase claims (nine phases, statuses synced with
  chapter statuses; Phase 6 done now that the CI gate ships)

## [0.2.0] - 2026-07-27

### Added

- New information architecture organized by outcome (modules 01 through 09) instead of by day
- Field guide section modeled on Alexey Grigorev's AI Engineering Field Guide
- Ten portfolio-grade project specifications in [projects/](projects/)
- Six role-specific learning paths in [learning-paths/](learning-paths/)
- Templates for chapters, projects, eval rubrics, and learning paths in [_templates/](_templates/)
- Reference implementations in [examples/](examples/)
- Interview prep and job market analysis sections
- `STYLING.md` enforcing minimalist, density-first formatting
- `MAINTAINERS.md` documenting the editorial bar and maintainer roles
- `ROADMAP.md` with per-phase status badges

### Changed

- Renamed all folders to kebab-case with zero-padded numbers (was `Day 04 Sequential Workflows in LangGraph`, now `02-langgraph-core/02-sequential-workflows.md`)
- Rewrote README to under 4,000 characters (was 36,000); moved depth into linked documents
- Pinned all dependencies in `pyproject.toml` (was unpinned `pip install` instructions)
- Replaced unsourced statistics with sourced claims or removed them

### Removed

- The "Day 0 through Day 9" calendar structure (replaced by outcome-organized modules)
- The ASCII box-drawing roadmap diagram (replaced by a Mermaid diagram in ROADMAP.md)
- The six full-width for-the-badge shields from the README (replaced by plain text)
- References to the old repository name `Agentic-AI-Roadmap-with-Notes-Using-LangGraph`

## [0.1.0] - 2026-05-15

### Added

- Initial release with Day 0 through Day 9 of LangGraph tutorials
- README, CONTRIBUTING, LICENSE
- Ten Jupyter notebooks covering sequential, parallel, conditional, and iterative workflows
