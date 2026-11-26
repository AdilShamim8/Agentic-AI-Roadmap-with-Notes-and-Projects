# Design case: internal docs RAG

Module: 10-interview-preparation
Chapter: 09-design-case-docs-rag
Status: beta
Last reviewed: 2026-11-26
Estimated time: 1 hour

## Learning objectives

- Design the retrieval system that replaces naive vector search in agent answers
- Enforce tenant and access scoping structurally, not in the prompt
- Solve freshness and citation, the two requirements that fail in production

## The prompt

"Design an agent that answers employee questions about internal documentation - policies, runbooks, product specs. Ten thousand employees, thousands of documents, strict access control."

## Part 1 - Requirements

Functional: answer with citations to the source doc and section; refuse when the docs do not cover it. Non-functional: p95 under 4 seconds, access control at document granularity (a finance doc is invisible to everyone else), and freshness - the answer must reflect the current doc version, not last quarter's.

## Part 2 - Architecture

Retrieval as a tool, not a pipeline: the agent decides whether and what to search, reformulates, and can search again with different terms. That decision - search or answer from what you have - is the whole point of tool-shaped retrieval, and it is what this repo teaches in [04 Tools and MCP, chapter 06](../04-tools-and-mcp/06-retrieval-as-a-tool.md). State: messages plus a scratchpad of retrieved doc IDs so the agent knows what it has seen. The answer node receives only tool results, never direct index access.

## Part 3 - Tools and the index

`search_docs(query, scope)` where scope is derived from the caller's identity server-side. The index: embeddings for semantic recall plus keyword/BM25 for exact terms - hybrid, because part numbers and error codes do not embed usefully. Chunking at heading boundaries with the doc title and section path attached to each chunk. The filter chain runs before ranking: identity group, document ACL, freshness timestamp. A stale-document policy: re-embed on change events from the docs system; if the event pipeline is down, search results carry the doc's last-updated date and the agent can surface staleness instead of hiding it.

## Part 4 - Evaluation

Golden set: real questions with the expected source doc. Evaluators: retrieval hit rate (the expected doc in the top k), answer faithfulness (LLM-judge, per-claim citation check), refusal correctness (questions the docs do not answer must produce "no coverage" - confabulation here is a firing-level bug, say that plainly), and access checks: canary questions with forbidden documents that must never appear, run on every deploy.

## Part 5 - Production

The agent runs on the platform (`langgraph build`, Kubernetes), Postgres checkpointing for conversation continuity. The index lives on managed vector infra with the ACL filter pushed into the query, never post-filtered. Cost: query classification drops simple lookups ("what is the PTO policy") to a cache; only ambiguous questions pay for the loop. Observability: zero-answer rate (the metric that tells you the index has gaps), refusal rate, and p95.

## Part 6 - Failure modes

1. Permission leak: blocked structurally by the pre-rank filter and tested by the canary set - "tested by canary" is the sentence the panel wants.
2. Confident wrong answer from a stale doc: staleness surfaced in results; critical policies get a "verify against source" link on the answer.
3. Zero-answer on vocabulary mismatch (employees say "expense claim," docs say "reimbursement request"): hybrid search plus a synonym layer; the zero-answer-rate metric tells you when to extend it.

## The follow-ups

- "Why not fine-tune on the docs?" Access control, freshness, and citations all break; retrieval keeps all three. Also the docs change weekly and a fine-tune does not.
- "Multi-tenant?" The scoping story is identical - tenant replaces identity group. [The retrieval demo](../examples/retrieval_demo.py) shows the tenant-scoped tool shape, keyless.
- "What about images and diagrams in the docs?" Capabilities answer: extract text at ingest, defer multimodal indexing to a second phase with its own eval - do not hand-wave it into phase one.

## What is next

[10 Design case: anomaly monitor](10-design-case-anomaly-monitor.md) - the streaming case, where latency is the design.
