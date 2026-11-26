# 08 Production - interview questions (concepts)

Status: beta | Teaches: [08 Production](../../08-production/) | Part 1 of 2

1. What does the LangGraph deployment story look like today - and what replaced the old base-image flow?
The `langgraph build` flow: a project definition (graph modules, dependencies), built into a deployable image serving the graph over a standard API - checkpoints, streaming, task queues included. It replaced the deprecated base-image approach; an answer still describing pulling a generic SDK image and hand-wiring the server dates the candidate. Teaches: [01-langgraph-platform](../../08-production/01-langgraph-platform.md).

2. Why does the checkpointer choice become an infrastructure decision in production?
Because it holds user conversation state: durability (restarts, deploys), concurrency (many threads at once), and operations (backup, retention, vacuum) are all storage problems. MemorySaver is a test double; production means SqliteSaver only for single-writer edge cases, PostgresSaver for real systems. Teaches: [02-docker-and-checkpointing](../../08-production/02-docker-and-checkpointing.md).

3. What does deploying a graph to Kubernetes actually involve - the parts list?
A container image with the graph definition and deps, a deployment with replicas, the checkpointer's Postgres reachable by service, readiness checks that warm the model clients, HPA on queue depth or request rate, and config/keys via secrets - never in the image. The bar: name the stateful piece (Postgres) as the part that makes the deploy different from a stateless web app. Teaches: [02-docker-and-checkpointing](../../08-production/02-docker-and-checkpointing.md) and the repo's k8s manifests.

4. Multi-tenancy in an agent serving platform: what are the isolation seams?
Three layers: checkpointer namespacing per tenant (thread and store keys scoped), tool-layer authorization (identity flows from the session into every tool call, enforced server-side), and resource accounting (per-tenant rate limits and cost attribution). The failure to name: prompt-level tenant separation - "you are serving tenant X" - which is advice, not isolation. Teaches: [04-multi-tenant-considerations](../../08-production/04-multi-tenant-considerations.md).

5. What are the cost-control levers in production agents, ranked by impact?
Model tiering per step (classification on cheap models, reasoning on strong), context discipline (trim, summarize, avoid resending history bloat), tool output bounding, and caching repeated lookups. Then turn caps and budget fields so runaway loops cap themselves. The bar: rank with reasons - most candidates list levers without an impact order. Teaches: [03-cost-optimization](../../08-production/03-cost-optimization.md).

6. What does governance mean for an agent in a regulated environment?
The audit trail (who approved what, every destructive action attributable - which the checkpointer's structure gives you), the eval record (what was measured before release, per version), data boundaries (which tenants' data trained nothing, stayed in which region), and rollback (a version that can be reverted in minutes, not days). Teaches: [05-governance-and-compliance](../../08-production/05-governance-and-compliance.md).

7. Blue-green or rolling for agent deploys - what is the specific wrinkle?
The checkpointer schema and state compatibility: a rolling deploy runs two graph versions against one state store, so state migrations must be additive (new optional fields, no renamed keys) or versioned. The wrinkle unique to agents: in-flight conversations resume on the new code - a node whose semantics changed mid-conversation is a real failure mode, so semantic compatibility is the deploy question, not just the schema one. Teaches: [01-langgraph-platform](../../08-production/01-langgraph-platform.md).

8. What are the on-call alert thresholds you would set on day one of an agent service?
Tool-error rate (the earliest symptom of integration decay), escalation or refusal spikes (behavioral regressions the endpoint metrics miss), p95 per turn and time-to-first-token (UX contracts), queue depth, and cost per hour (a loop burning money is an incident, not a bill). Day one also gets the runbook entries: what each alert means and the first three diagnostic steps. Teaches: [06-runbooks-and-incident-response](../../08-production/runbooks/) and [observability](../../06-evals-and-observability/).

9. What does "continuous improvement" concretely mean for a shipped agent?
The weekly loop: sample traces, classify failures, convert the top failure families into golden rows, fix what the rows expose, and let the gate hold the line. Plus the monthly loop: rebalance the golden set toward current traffic, recalibrate the judge, review cost and latency trends. It is maintenance with a measurement discipline - the difference between an agent that ages well and one that quietly rots. Teaches: [07-continuous-improvement](../../08-production/07-continuous-improvement.md).

10. Secrets in an agent deployment: what is the correct shape?
Injected at runtime from a secrets manager into the process environment; never in the image, never in the repo (`.env` git-ignored, `.env.example` carrying only the names); scoped per service (the agent does not hold the database admin's key); and rotated with the consumers updated by config, not redeploy. The repo's `.env.example` plus gitignore is the hygiene floor; production adds the manager. Teaches: [02-docker-and-checkpointing](../../08-production/02-docker-and-checkpointing.md) and [SECURITY.md](../../SECURITY.md).

11. What is the retry discipline for a production agent?
Retry at the tool layer with backoff for transient backend failures (the model never sees these); let the model see and adapt to semantic errors (unknown customer, invalid argument); cap graph-level retries so a poisoned conversation routes to a human instead of looping. The anti-pattern: blanket try-again at the HTTP layer, which turns every bug into a triple-billed bug. Teaches: [02-docker-and-checkpointing](../../08-production/02-docker-and-checkpointing.md).

12. Latency budget for a chat agent: name the components and their typical order.
Model first-token (hundreds of ms to seconds - the dominant term), tool execution (varies wildly; must be bounded), model continuation per step, and network overhead. The design consequence: streaming hides the model term, progress events hide the tool term, and neither fixes a slow tool - that is the tool's own budget. Teaches: [03-cost-optimization](../../08-production/03-cost-optimization.md) and [streaming](../../03-agents-in-practice/05-streaming-and-ux.md).
