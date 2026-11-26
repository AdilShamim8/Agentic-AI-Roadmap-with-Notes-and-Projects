# System design structure

Module: 10-interview-preparation
Chapter: 05-system-design-structure
Status: beta
Last reviewed: 2026-11-26
Estimated time: 2 hours

## Learning objectives

- Run the agent system design round with a six-part structure that maps to a rubric
- Budget the 45 minutes across the parts instead of drowning in part one
- Connect every architectural choice to the eval and production stories the panel expects

## The six-part answer

The field guide lists the expected coverage; this chapter turns it into a running order with time budget. Use it verbatim until it is muscle memory.

1. Requirements, 5 minutes. Functional: what the agent does, who for, what success looks like. Non-functional: latency, cost per request, volume, uptime, data sensitivity. State one metric you will design against and hold it: "p95 under 4 seconds, cost under half a cent per conversation turn."
2. Architecture, 10 minutes. The graph: nodes, state, edges, the pattern (ReAct, plan-and-execute, supervisor) and one rejected alternative with the reason. Name the state explicitly and say what persists where - messages in state, checkpoints in Postgres, long-term memory in the `Store`.
3. Tools and integration, 8 minutes. The tool list with schemas, which are native vs MCP servers, and the security boundary: who may call what, how tenant scoping is enforced in the tool layer rather than the prompt.
4. Evaluation, 8 minutes. The golden dataset (where the rows come from), the evaluators (exact-match for routing, LLM-judge for generation, trajectory checks for tool misuse), the regression gate in CI, and the baseline number you hold.
5. Production, 7 minutes. Deployment shape (`langgraph build`, containers, Kubernetes), the checkpointer backend, streaming to the client, monitoring (latency, tool-error rate, escalation rate), and cost control (model tiering, caching, turn caps).
6. Failure modes, 7 minutes. The top three: retrieval misses, tool errors, prompt drift. For each: detection signal, mitigation, and the fallback to a human.

## Why this order

Panels score design rounds on axes, not on cleverness: requirements coverage, architecture soundness, evaluation, production awareness, failure-mode honesty. The six parts hit the axes in the order the rubric lists them. Candidates who freestyle spend 25 minutes on architecture, get cut off before evaluation, and receive the feedback "did not consider how to measure success" - the most common design-round rejection, and the cheapest to avoid.

## The moves that score

- Name the state schema out loud. "State is messages, plus a scratchpad of retrieved doc IDs, plus a pending action." Agent design lives and dies in state, and half the field cannot articulate theirs.
- Draw the graph, not the cloud. Boxes for nodes, arrows for edges, one box for the persistence layer. [ARCHITECTURE.md](../ARCHITECTURE.md) is the one-page version of what your whiteboard should look like.
- Reject an alternative on record. "Plan-and-execute would plan once and commit; for this task the loop needs to react to tool results, so ReAct." A choice without a rejected alternative reads as default, not decision.
- Volunteer the numbers. Requests per day, expected tokens per turn, cost per request, p95 target. Rough is fine; absent is not.
- End on evals. When the interviewer says "anything to add?", the answer is the eval plan: "If I shipped nothing else first, I would ship the 30-row golden set and the CI gate, because every other component changes under it."

## The traps

- The hallucinated requirement: designing for scale the interviewer never stated. Ask "what volume are we designing for?" in part one.
- The multi-agent reflex: proposing a supervisor with three specialists for a task one agent and four tools handles. Over-engineering is a rubric line-item, and interviewers press on it deliberately.
- The prompt-only answer: any question about reliability answered with prompt changes and nothing structural (tool scoping, validation, evals) fails the round in agent-heavy loops.
- The invisible human: no escalation path for the failure modes. Every production agent story ends with a human somewhere; put them on the board.

## Drill

Take any prompt ("design an agent that books travel," "design an internal doc assistant") and run the six parts against a clock, alone, out loud, three times. The third run fits the time budget. Then run the full worked cases in chapters 06-10 and compare your board to theirs.

## What is next

[06 Design case: support agent](06-design-case-support-agent.md), the canonical case, worked end to end.
