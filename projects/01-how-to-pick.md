# How to pick a project

Pick by goal, then by background, then by time. Do not pick by difficulty stars alone - a hard project you abandon teaches less than a moderate project you ship.

## Pick by goal

- If your goal is a job-ready portfolio: build three projects, not ten. One single-agent system (01, 05, or 06), one multi-agent or data-heavy system (02, 03, 07, or 08), and one eval-focused project (10). Three shipped projects with evals beat ten half-finished ones.
- If your goal is to fill a specific skill gap: pick the project that exercises that gap. RAG and retrieval: 03. MCP and tool ecosystems: 05. Streaming and async: 07. Cross-framework interop: 08. Evaluation: 10.
- If your goal is to learn a pattern you just read about: pick the cheapest project that uses it. Reflexion: 04. Multi-agent handoffs: 02 or 08. Human-in-the-loop: 02 or 07.

## Pick by background

- From ML engineering or backend: you already know production. Pick projects that stress the new material: 04 (self-healing code agent) or 10 (eval harness).
- From data science or analytics: pick projects that stress engineering rigor: 02 (customer support multi-agent) or 07 (anomaly monitor).
- From data engineering: 03 (knowledge manager) and 07 (anomaly monitor) map directly to your pipeline instincts.
- From frontend: 02 and 09 let you build the UI layer that most candidates skip.

See your [learning path](../learning-paths/) for the two projects recommended for your specific background.

## Pick by time

- 1-2 weeks available: 01 (research agent).
- 2-3 weeks: 02, 03, 06.
- 3-4 weeks: 04, 05, 07, 10.
- 4-6 weeks: 08, 09. These are product-scale; only start them if you can carry a longer project.

## The rules that apply to every pick

1. Read the spec twice before writing code. The eval rubric is part of the spec, not an appendix.
2. Build your own implementation before opening the reference solution in [projects/-solutions/](-solutions/).
3. Ship it. A deployed project with a live URL is worth several local-only ones in an interview.
4. Write the README while you build, not after. It explains the architecture, the eval results, and the trade-offs you made.

## Sequencing

Start with 01 unless a learning path says otherwise. It exercises the full core loop - tools, multi-step reasoning, structured output, evaluation - at the lowest complexity. After 01, follow your goal: portfolio builders go 01 -> 02 -> 10; skill-gap fillers go straight to the project that exercises the gap.
