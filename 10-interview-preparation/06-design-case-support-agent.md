# Design case: support agent

Module: 10-interview-preparation
Chapter: 06-design-case-support-agent
Status: beta
Last reviewed: 2026-11-26
Estimated time: 1 hour

## Learning objectives

- Produce a complete six-part design for the canonical e-commerce support agent
- See the follow-up questions interviewers use to test depth on this case
- Map the case to the repo chapters that back each part

## The prompt

"Design a customer support agent for an e-commerce company. It should handle order status, returns, and refunds. Refunds over $50 need human approval."

## Part 1 - Requirements

Functional: answer order-status questions, start returns, issue refunds under $50, escalate everything else to a human agent. Non-functional: p95 first token under 2 seconds, cost under half a cent per conversation, and a full audit trail per action. Volume, asked out loud: assume 20,000 conversations per day, 70 percent order status.

## Part 2 - Architecture

A single ReAct-style agent with scoped tools, not a multi-agent system - the task is one domain with four actions, and the tool count does not justify a supervisor. State: `messages` with the reducer, plus `pending_refund` carrying the structured proposal awaiting approval. The refund flow interrupts (`interrupt()`), surfaces the proposal to a human, and resumes with `Command(resume=...)`. Checkpointing on Postgres so a conversation survives reconnects; the same checkpointer gives you the audit trail.

## Part 3 - Tools

Four native tools with typed schemas: `get_order_status(order_id, customer_id)`, `start_return(order_id, reason)`, `issue_refund(order_id, amount, reason)`, and `handoff_to_human(reason, summary)`. Order tools enforce tenant and identity checks in the tool layer - the customer_id comes from the session, never from the model. If the org runs other agents against the same order systems, expose the tools as an MCP server once and let each agent consume it; otherwise native tools are the simpler call. The destructive tool (`issue_refund`) is gated by the interrupt, not by a prompt instruction.

## Part 4 - Evaluation

Golden dataset built from real ticket categories: 30-plus rows of `input, expected_intent, expected_tool, expected_args`. Exact-match on intent and tool call; LLM-judge on the response text for tone and completeness; a trajectory check that a refund over $50 never executes without a resume event. Baseline the numbers before shipping (the repo's [eval module](../../06-evals-and-observability/) and `run_evals.py` are this part, working) and gate changes in CI.

## Part 5 - Production

`langgraph build` image, Kubernetes deployment, two replicas, the Postgres checkpointer on managed Postgres. Token streaming to the chat client so the first-token target is met. Monitoring: tool-error rate, escalation rate, refund volume per day, p95 per turn. Cost control: the model tier drops to a cheaper class when intent is order-status - the deterministic 70 percent.

## Part 6 - Failure modes

1. Wrong-tool call on refund: detected by the trajectory eval; blocked by the approval gate regardless.
2. Order system outage: tool errors surface as a graceful "cannot reach order systems right now" plus auto-escalation, not a retry loop.
3. Prompt drift after a model update: caught by the CI eval gate before it reaches users.

## The follow-ups

- "How do you stop it from refunding the same order twice?" Idempotency key on `issue_refund`, checked in the tool layer, rejected as a duplicate.
- "The CFO wants refund leakage numbers." Refund volume per day with mean and p99 amount, plus the approval rejection rate - all derivable from the checkpointer.
- "Where does RAG fit?" Only for policy questions: the returns policy is a retrieval tool scoped to a policy index, which is [retrieval as a tool](../../04-tools-and-mcp/06-retrieval-as-a-tool.md), not a vector search over the whole chat.

## What is next

[07 Design case: research agent](07-design-case-research-agent.md) - the case where the loop, not the tools, is the hard part.
