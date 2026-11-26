# Interview guide - Project 02: Customer support multi-agent

Status: beta | For: presenting this project in interviews | Related: [project README](README.md), [project stories](../../10-interview-preparation/15-project-stories.md)

## The pitch

"A supervisor routes customer messages to four specialists - knowledge base, order status, refunds, escalation - with an `interrupt()` approval gate on refunds over $50 and a 30-row golden set held at 93 percent intent accuracy in CI. The gate is structural: the interrupt sits in the graph before the refund tool, so no model swap or prompt regression can route around a human."

## The whiteboard script

1. State: `messages` (reducer-appended), `intent`, `pending_refund` (the structured proposal).
2. The supervisor node - classifies and routes; one conditional edge, named `route_by_intent`.
3. The four specialists as bounded boxes, each with its tool.
4. The refund flow drawn with a pause symbol: propose, `interrupt()`, human approves, `Command(resume=...)`, execute.
5. The checkpointer on Postgres - conversation survives reconnects; the audit trail comes free.

The line that earns the nod: "The refund gate is structural, not prompt-level." It is the sentence interviewers write down.

## The numbers you quote

- 30-row golden set from real ticket categories; 93.3 percent intent accuracy, baseline-gated in CI (the repo's own number - quote yours if you rebuilt it).
- The $50 threshold as a policy constant - risk appetite is a product decision you can discuss.
- Refund idempotency: duplicate-call rejection via a key checked in the tool layer.

## The follow-ups

- "Why multi-agent at all?" The four specialists have divergent tool scopes and the routing is a real classification task - but say the honest boundary: at lower tool counts, a single agent with scoped tools also works, and you chose the split for tool hygiene, not fashion.
- "How do you stop double refunds?" Idempotency key on `issue_refund`; the tool layer rejects duplicates regardless of what the model attempts.
- "What does the escalation agent actually do?" Hands off with a summary to a human queue; the conversation state transfers intact via the checkpointer.
- "Where does RAG fit?" Only in the knowledge-base specialist: scoped retrieval over support docs - [retrieval as a tool](../../04-tools-and-mcp/06-retrieval-as-a-tool.md), never a vector dump into the main context.
- "How would you extend it?" Streaming for UX, then a per-specialist eval split so routing regressions localize to one specialist.

## The red flags

- Drawing the cloud before the state schema.
- "The prompt tells it not to refund twice" - prompt-level safety answers fail this interview on the spot.
- No eval story: this is the canonical project precisely because it carries the full eval discipline.

## What this project proves

The complete production pattern: routing, HITL as structure, persistence, and measured behavior - the strongest single story for agent-product roles.
