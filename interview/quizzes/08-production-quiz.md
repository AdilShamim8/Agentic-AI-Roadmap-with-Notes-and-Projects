# Quiz 08 - Production

Status: beta | Covers: [08 Production](../../08-production/) | 10 questions

1. The current deployment flow for LangGraph services:
A) Deprecated base images with hand-wired servers
B) `langgraph build` producing a deployable image with the API, checkpoints, streaming included
C) Serverless functions only
D) Manual VM provisioning

2. Production checkpointer choice is an infrastructure decision because:
A) It affects prompt quality
B) It holds user state - durability, concurrency, and operations are storage problems
C) It changes model routing
D) Providers require Postgres

3. Agent deploys differ from stateless web deploys mainly at:
A) Image size
B) The stateful layer - checkpoint compatibility and resumed conversations across versions
C) Port numbers
D) Nothing

4. Multi-tenant isolation is correctly done at:
A) The prompt - "you are serving tenant X"
B) Checkpointer namespacing, tool-layer identity enforcement, and per-tenant resource accounting
C) Separate deployments, always
D) The model tier

5. The highest-impact cost lever, typically:
A) Caching headers
B) Model tiering per step plus bounded tool outputs
C) Shorter system prompts
D) Fewer replicas

6. Governing a regulated agent means, concretely:
A) Longer legal disclaimers
B) Audit trails, eval records per version, data boundaries, and fast rollback
C) Blocking all tools
D) On-prem models only

7. The first alerts on day one of an agent service:
A) CPU and memory
B) Tool-error rate, escalation/refusal spikes, p95 per turn, queue depth, cost per hour
C) Disk usage only
D) None - observe first

8. Secrets belong:
A) In the image for speed
B) Injected at runtime from a secrets manager, scoped per service
C) In the repo, encrypted
D) In the checkpointer

9. Tool-layer retries with backoff are for:
A) The model to see and adapt to
B) Transient backend failures the model never sees
C) Every error, always
D) Billing retries

10. Continuous improvement for a shipped agent is:
A) Quarterly rewrites
B) The weekly loop: sample traces, cluster failures, new golden rows, fix, gate
C) User surveys only
D) Model upgrades when benchmarks move

## Answer key

1. B - the old base-image flow is the dated answer ([chapter 01](../../08-production/01-langgraph-platform.md)).
2. B - the state store is the product's memory ([chapter 02](../../08-production/04-checkpointing-and-durability.md)).
3. B - additive state migrations or explicit ones ([chapter 02](../../08-production/04-checkpointing-and-durability.md)).
4. B - prompt-level separation is advice, not isolation ([chapter 04](../../08-production/04-checkpointing-and-durability.md)).
5. B - classification does not need a frontier model ([chapter 03](../../08-production/05-cost-optimization.md)).
6. B - provable, versioned, reversible ([chapter 05](../../08-production/06-governance-and-safety.md)).
7. B - tool errors spike first; loops burn money ([runbooks](../../08-production/runbooks/)).
8. B - never in image or repo ([SECURITY.md](../../SECURITY.md)).
9. B - semantic errors route to the model; transient ones hide in the layer ([chapter 02](../../08-production/04-checkpointing-and-durability.md)).
10. B - maintenance with measurement discipline ([chapter 07](../../08-production/07-continuous-improvement.md)).
