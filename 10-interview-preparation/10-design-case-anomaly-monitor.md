# Design case: anomaly monitor

Module: 10-interview-preparation
Chapter: 10-design-case-anomaly-monitor
Status: beta
Last reviewed: 2026-11-26
Estimated time: 1 hour

## Learning objectives

- Design the real-time case where the event loop, not the LLM, is the backbone
- Keep the LLM out of the hot path and justify where it does run
- Define alert quality as a measurable target, the metric this product lives or dies on

## The prompt

"Design a system that monitors payment transactions, detects anomalies, and alerts the on-call engineer with a summary and recommended action. 50,000 transactions per second."

## Part 1 - Requirements

Functional: score every transaction in-stream, group related anomalies, and produce actionable alerts with a summary, evidence, and a recommendation. Non-functional: detection latency under 5 seconds end to end, alert precision high enough that on-call opens the page (target: under 10 percent false pages), and a hard budget for LLM calls - at 50K TPS the model cannot see every event, and the interviewer is waiting to see whether you notice.

## Part 2 - Architecture

Two tiers, and the tiering is the answer. Tier one: streaming stats and rules - rolling aggregates, thresholds, a simple model - in the stream processor, millisecond latency, no LLM. Tier two: an agent that wakes on tier-one anomalies, pulls the correlated window (recent transactions for the same merchant, card, or account), investigates with tools, and composes the alert. The agent runs per incident, not per event; the event loop runs always. [05 Agentic patterns](../05-agentic-patterns/) framing: this is a supervisor that dispatches on incident, with investigation sub-agents and a hard turn cap.

State per incident: the anomaly window, the investigation findings, and the draft alert. Incidents checkpoint; a five-minute-old incident resuming after a crash is normal operation, not an error.

## Part 3 - Tools

`query_window(filter, span)` against the transaction store, `get_entity_history(merchant_id or account_id)`, `get_rules(entity)`, and `post_alert(channel, severity, payload)`. The alert tool is the destructive one: it pages a human, so it fires once per incident, after dedup, and the workflow - not the agent - enforces rate limits on paging.

## Part 4 - Evaluation

Alert quality is the product. Golden set: historical incidents with labels (real fraud, real outage, benign) plus benign windows that must stay silent. Evaluators: detection recall on labeled incidents, alert precision (the false-page rate), and recommendation correctness - the LLM-judge scores whether the recommended action matched the post-incident review. A "silence evaluator" over benign windows catches the failure mode of an over-alerting change. All of it gated in CI like any other regression.

## Part 5 - Production

Stream processor (the existing kafka/flink-shaped infra; name whatever you know) for tier one. Agent tier on Kubernetes via `langgraph build`, autoscaled on incident queue depth, Postgres checkpointing. Observability is the product's mirror: alert volume by severity, false-page rate over time, and the human feedback loop - on-call marks alerts useful or noise, which becomes eval rows. Cost: the LLM bill tracks incident rate, not TPS, which is the entire payoff of tiering.

## Part 6 - Failure modes

1. Alert storm from one upstream outage: dedup and rate limits in the workflow layer; correlated anomalies become one incident.
2. The agent's recommendation is confidently wrong: recommendation is advisory on-call can dismiss; feedback loop feeds the eval set.
3. Tier one quietly degrades (threshold drift): the recall evaluator on the golden incident set catches it in CI before the on-call engineers do.

## The follow-ups

- "Can the LLM do tier one?" No: 50,000 TPS at even a cent per call is 500K dollars an hour; say the arithmetic out loud - panels remember candidates who multiply.
- "What about false negatives?" The recall number is a choice you make with the business, published, and revisited monthly; pretend there is a knob, because there is.
- "Why an agent at all instead of template alerts?" The investigation - correlating entities, pulling history, tailoring the recommendation - is what template alerts cannot do, and it runs per incident where the cost is sane.

## What is next

[11 Trace debugging round](11-trace-debugging-round.md) - the round that replaces a second coding screen in mature loops.
