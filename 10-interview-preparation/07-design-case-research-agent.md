# Design case: research agent

Module: 10-interview-preparation
Chapter: 07-design-case-research-agent
Status: beta
Last reviewed: 2026-11-26
Estimated time: 1 hour

## Learning objectives

- Design the iterative-retrieval loop that research tasks actually need
- Control loop cost with a turn cap instead of hoping the model stops
- Handle citation grounding, the requirement that fails most research agents

## The prompt

"Design a research agent that takes a question, reads web and internal sources, and produces a cited summary. Users are analysts; accuracy matters more than speed."

## Part 1 - Requirements

Functional: decompose the question, search, read, refine, and synthesize a summary with per-claim citations. Non-functional: a run may take minutes, so it is a background job with progress streaming, not a chat. Cost cap per run. Explicit non-goal: exhaustive coverage - the agent answers the question and stops.

## Part 2 - Architecture

Plan-and-execute, not ReAct: research rewards a plan committed to state before the loop starts, then a worker loop that revises. State: the plan (sub-questions), findings per sub-question with source IDs, and a budget field counting iterations. The loop condition checks the budget - the recursion limit is the retrieval cap. When the budget exhausts without convergence, the synthesis node runs on what exists and marks gaps, rather than looping forever. Long runs checkpoint on Postgres so a crashed run resumes instead of restarting.

## Part 3 - Tools

`web_search(query)`, `read_page(url)` with a content extractor and a token cap, and `search_internal(index, query)` for the company corpus. The MCP question: expose search and read as MCP tools so any agent in the org reuses them - this is the clean MCP case, one server, many consumers. Anti-pattern to call out: an agent that fetches the raw HTML and asks the model to find things in it; the extraction happens in the tool, and the model sees text and a token budget.

## Part 4 - Evaluation

The golden set is question-plus-expected-source-set. Evaluators: citation faithfulness (every claim maps to a cited source - LLM-judge with a strict rubric), coverage (the expected sources appear), and a refusal check (unanswerable questions produce "insufficient sources" rather than confabulation). A trajectory check that read-to-search ratios stay sane, because a runaway loop of reads is the failure mode.

## Part 5 - Production

Background execution: the client submits a job, the graph runs on a worker, progress streams over websockets. Model tiering: a cheap model class for extraction and summarization of single pages, the strong model only for planning and final synthesis. Cost per run capped by the budget field; monitoring shows the distribution, because cost blowups here are quiet.

## Part 6 - Failure modes

1. The model asserts what the sources do not say: the citation-faithfulness evaluator catches it; synthesis prompt requires per-sentence source IDs.
2. Source drift mid-run (page changes between read and cite): snapshot the extracted text at read time; cite the snapshot.
3. The infinite loop: the budget field ends it deterministically - the answer to "how do you stop it?" must never be "the model decides."

## The follow-ups

- "Parallelize?" Yes - sub-questions fan out (map-reduce), each with its own budget; the reducer merges findings.
- "Same agent for academic papers?" The corpus changes; the loop does not. Swap the search tools and the citation format. That generality is the point of tools-as-boundary.
- "Why not fine-tune instead of the loop?" A fine-tune does not fix coverage; retrieval does. Say it in one sentence and move on.

## What is next

[08 Design case: code review](08-design-case-code-review.md) - where the human escalation is the architecture.
