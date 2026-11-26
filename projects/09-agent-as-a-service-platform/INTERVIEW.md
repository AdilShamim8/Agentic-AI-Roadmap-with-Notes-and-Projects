# Interview guide - Project 09: Agent as a service platform

Status: beta | For: presenting this project in interviews | Related: [project README](README.md), [project stories](../../10-interview-preparation/15-project-stories.md)

## The pitch

"Agents as a served, multi-tenant product: teams deploy graph definitions, the platform runs them with isolated checkpoints, scoped tool access, and per-tenant cost attribution. The isolation seams are the architecture - namespacing, tool-layer identity, resource accounting - and none of them live in the prompt."

## The whiteboard script

1. The platform boundary: teams submit graph definitions and tool registrations.
2. The serving layer - `langgraph build` images, replicas, queue depth autoscaling.
3. The three isolation seams, drawn as explicit lines:
   - Checkpointer/store namespacing per tenant
   - Tool-layer identity enforcement (session identity into every call, server-side)
   - Per-tenant rate limits and cost metering
4. The platform observability - per-tenant latency, error, and spend dashboards.
5. The eval harness per deployed agent - the platform's regression gate.

The line that earns the nod: "Prompt-level tenant separation is advice, not isolation."

## The numbers you quote

- Per-tenant concurrency caps and queue fairness policy.
- Cost attribution granularity (per request, per task outcome).
- The canary checks that prove isolation on every deploy.

## The follow-ups

- "How do you stop tenant A starving tenant B?" Fair-share queues and per-tenant caps: a tenant's requests queue behind their own limit, not others' work. Split deployments only when isolation is contractual.
- "Who owns the evals - platform or tenants?" Both, by layer: the platform runs the harness and gates; each tenant's golden set is their domain. The platform's job is making the gate unavoidable.
- "What breaks as tenants grow?" Checkpoint storage volume (retention policy is a product decision), state-schema migrations across versions (additive only), and the model-tier fairness question - all three have runbook answers.
- "Why a platform instead of each team shipping their own?" Shared plumbing - auth, metering, checkpoints, eval harness - done once with real rigor; teams keep the judgment layer.

## The red flags

- "We trust our tenants" as an isolation strategy.
- No cost attribution - the first platform complaint is always a bill.
- The eval story delegated to "each team's responsibility" with no harness enforcing it.

## What this project proves

Multi-tenancy as layered enforcement, platform economics, and the operational maturity that platform roles screen for hardest.
