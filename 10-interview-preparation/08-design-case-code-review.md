# Design case: code review

Module: 10-interview-preparation
Chapter: 08-design-case-code-review
Status: beta
Last reviewed: 2026-11-26
Estimated time: 1 hour

## Learning objectives

- Design the multi-agent case interviewers actually ask, without over-engineering it
- Place the human escalation point where review quality actually breaks
- Separate the find-issues job from the verify-issues job and justify the split

## The prompt

"Design a system that reviews pull requests: finds bugs and security issues, leaves comments, and does not waste senior engineers' time."

## Part 1 - Requirements

Functional: on PR open, review the diff and changed-file context, post comments, block on high-confidence critical issues. Non-functional: review completes within the CI window (10 minutes), false-positive rate low enough that engineers keep reading the comments - the product is trust, and one bad week of noise kills adoption. Explicit constraint: it proposes, humans dispose on anything destructive.

## Part 2 - Architecture

Pipeline, not a free-form agent. Diff chunking, then parallel per-file analysis (map-reduce), then a verifier pass, then a single reviewer node that deduplicates and composes the PR comment. The verifier is the load-bearing choice: the first pass finds candidate issues with recall bias; a second, cheaper agent (or deterministic checks - lint rules, AST patterns) verifies each candidate and drops the noise before it reaches humans. This is the pattern from [05 Agentic patterns](../../05-agentic-patterns/) map-reduce chapter: generation and verification want different prompts, different temperatures, often different model classes.

State: the diff chunks, candidate issues with file/line and confidence, verified issues, and the final comment. No persistence between PRs beyond aggregate stats.

## Part 3 - Tools

Read-only repository tools: `get_diff(pr)`, `read_file(path, ref)`, `get_blame(path, line)` for context, and `post_comment(pr, comments)`. Exposed as an MCP server so the same review agents serve any repo host or framework that speaks the protocol. Security posture worth saying out loud: the agents get read on the repo and write on PR comments only; they never get merge rights, and the workflow enforces the block, not the agent.

## Part 4 - Evaluation

This is where most candidate answers go silent; have the full answer. Golden set: historical PRs with known-issue labels - 30-plus diffs where a human found a real bug. Evaluators: precision (comments that were real issues), recall (known issues caught), and severity calibration (did criticals get marked critical). Regression gate in CI on the review system itself. Track the live metric that decides product success: comment dismiss rate, which is the market telling you about false positives.

## Part 5 - Production

Runs inside CI as a job; `langgraph build` image, one worker per PR, stateless between runs. The 10-minute window forces chunk-level parallelism and a hard turn cap per file. Cost control: cheap model for the find pass, strong model only for verify and compose. Observability: precision and recall over time, per-file-type breakouts (the agent is probably worse at generated code and migrations - say so).

## Part 6 - Failure modes

1. Noise spiral: dismiss rate climbs, engineers ignore comments - caught by the dismiss-rate metric, fixed by tightening the verifier threshold.
2. Context miss: the bug is in the interaction of two files, each chunk reviewed alone - mitigation: a second pass over the whole-diff summary for cross-file issues.
3. The agent blocks a critical-but-wrong issue: blocks only on the deterministic rule layer; model-found criticals comment, humans block.

## The follow-ups

- "Why not one agent with all the tools?" Chunk parallelism and the verify step want separate prompts; one agent serializes and blurs find with verify.
- "Where does the human go?" Escalation is inverted here: humans are the verifier of last resort, and the system's job is to spend their attention only on high-confidence criticals.
- "Ship order?" Rules first, find pass second, verify third, full autonomy never.

## What is next

[09 Design case: internal docs RAG](09-design-case-docs-rag.md) - retrieval as a tool, the case this repo teaches end to end.
