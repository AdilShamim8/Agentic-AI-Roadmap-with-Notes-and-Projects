# Project stories

Module: 10-interview-preparation
Chapter: 15-project-stories
Status: beta
Last reviewed: 2026-11-26
Estimated time: 2 hours

## Learning objectives

- Turn each portfolio project into a two-minute interview story with a number
- Match projects to the question families that recur in loops
- Adapt one project deep-dive for three depths: recruiter, manager, engineer

## Why stories need manufacturing

A project README is written for a reader with time; an interview story is spoken for a listener in two minutes. The gap between them is the work of this chapter: for each project, fix the situation, the decision, the number, and the failure - then practice saying it.

The mapping below covers all ten projects in [projects/](../../projects/). Each entry: the one-line pitch, the decision worth telling, and the question families it serves. The numbers cited are the repo's real baseline figures (93.3 percent on the 30-row set) where they apply; substitute your own measured numbers if you rebuilt the project - never quote a number you did not observe.

## The ten stories

1. [Research agent](../../projects/01-research-agent/README.md). Pitch: iterative retrieval with citations and a turn budget. Decision: the budget field ends the loop deterministically - "the model decides when to stop" is the answer panels reject. Serves: ownership, judgment, agent-specific families. Its failure story: the budget-exhausted run that synthesized gaps instead of looping - tell it as a feature.

2. [Customer support multi-agent](../../projects/02-customer-support-multi-agent/README.md). Pitch: routing plus approval-gated refunds, 30-row golden set, 93.3 percent intent accuracy. Decision: the refund gate is `interrupt()` before the tool call, structural against model swaps. Serves: everything - this is the canonical story; its eval gate answers question 18 cold.

3. [Knowledge manager](../../projects/03-knowledge-manager/README.md). Pitch: capture-in-passing with the `Store`, scoped retrieval. Decision: memory namespaces per user, not one global pile. Serves: judgment, agent-specific (16, 17). Failure story: cross-session memory that recalled stale preferences - fixed by namespace plus a recency field.

4. [Self-healing code agent](../../projects/04-self-healing-code-agent/README.md). Pitch: run-tests, diagnose, patch, re-run loop. Decision: the patch step proposes a diff, never applies it - the CI applies. Serves: ownership, integrity (24), agent-specific (15, 16). The escalation threshold (two failed patch attempts, then human) is a policy you can defend in one sentence.

5. [MCP universal agent](../../projects/05-mcp-universal-agent/README.md). Pitch: one agent, N tool servers over the MCP protocol. Decision: streamable HTTP with a manifest, tools discovered not hardcoded. Serves: judgment, collaboration - the "tools as a boundary" story that platform loops want.

6. [Multimodal document analyst](../../projects/06-multimodal-document-analyst/README.md). Pitch: routed extraction (text, tables, images) with structured outputs. Decision: per-modality validators before the merge node. Serves: pressure (22 - you learned the document models fast), ownership.

7. [Anomaly monitor](../../projects/07-anomaly-monitor/README.md). Pitch: rules tier plus agent investigation per incident. Decision: the LLM never sits in the hot path - cost arithmetic spoken aloud. Serves: judgment, agent-specific, and any "scale" question. This is the story for platform-heavy loops.

8. [Cross-framework network](../../projects/08-cross-framework-network/README.md). Pitch: A2A between a LangGraph agent and an agent from another stack. Decision: the protocol boundary at the agent card, shared task state. Serves: collaboration, motivation (26) - the interop war story.

9. [Agent as a service platform](../../projects/09-agent-as-a-service-platform/README.md). Pitch: multi-tenant agent serving, checkpointer isolation, per-tenant cost. Decision: tenant scoping in the tool layer and the checkpointer namespace, not the prompt. Serves: ownership, scale, judgment. The strongest story for platform roles.

10. [Eval harness and benchmark](../../projects/10-eval-harness-and-benchmark/README.md). Pitch: the 30-row set, evaluators, CI gate, 93.3 percent baseline. Decision: honest baseline instead of a cherry-picked number. Serves: agent-specific (17, 18) and the manager round's "how does the team decide between shipping and evaluating." For every other story, this is the eval appendix - quote its number.

## The three depths

Recruiter depth: the pitch line plus the number, 20 seconds. Manager depth: pitch, decision, result, 90 seconds, no architecture vocabulary. Engineer depth: the whiteboard version - state schema, tools, the graph, the failure mode, 5 minutes at the ready. Every story above should be speakable at all three depths from the same facts.

## Assembly instructions

Pick three projects as primaries (support, anomaly monitor, eval harness is the strongest triangle: product, platform, reliability). Write each as six STAR bullets. For the other seven, keep the one-line pitch and the decision sentence - enough to route a surprise question onto a real project instead of a hypothetical.

## What is next

[16 Resume and portfolio](16-resume-portfolio.md) - where these stories get compressed onto one page.
