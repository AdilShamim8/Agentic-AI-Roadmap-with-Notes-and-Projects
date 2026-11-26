# Interview guide - Project 07: Anomaly monitor

Status: beta | For: presenting this project in interviews | Related: [project README](README.md), [project stories](../../10-interview-preparation/15-project-stories.md)

## The pitch

"Two tiers: a streaming rules layer that scores every event in milliseconds, and an agent tier that wakes per incident - pulls the correlated window, investigates with tools, and composes the alert with a recommendation. The LLM never sits in the hot path; the bill tracks incident rate, not event rate."

## The whiteboard script

1. The event stream on the left, high-volume, constant.
2. Tier one: rules and rolling aggregates - millisecond latency, no LLM.
3. The incident trigger - an anomaly becomes an incident, deduplicated and rate-limited.
4. The agent tier per incident: state holds the window, findings, and draft alert; tools query history; a hard turn cap bounds the investigation.
5. The alert path - one page per incident, severity-ordered, recommendation advisory and dismissible.

The line that earns the nod: the cost arithmetic. "At 50,000 TPS, even one cent per call is half a million dollars an hour - so the model runs per incident, not per event." Say the multiplication out loud; panels remember candidates who multiply.

## The numbers you quote

- Event rate (your stream's), incident rate (what the agent actually bills against).
- The false-page target (under 10 percent) and how the golden set measures it.
- Dedup window and alert rate limits.

## The follow-ups

- "Can the LLM do tier one?" No - the arithmetic above. Tier one is rules and cheap models; judgment is per-incident.
- "What about false negatives?" The recall number is a published choice the business makes with you, revisited monthly - not an engineering secret.
- "Why is the recommendation advisory?" On-call can dismiss; the feedback loop (useful/noise) feeds the eval set - recommendation correctness is measured, not assumed.
- "How do you avoid alert storms?" Dedup and rate limits in the workflow layer, correlated anomalies as one incident - the workflow, not the agent, owns paging.

## The red flags

- The LLM in the hot path, at any price.
- No dedup story - alert storms are the product-killing failure.
- Precision and recall mentioned without the golden set that measures them.

## What this project proves

Latency-tiered architecture, cost arithmetic spoken fluently, and alert-quality thinking - the platform-loop story.
