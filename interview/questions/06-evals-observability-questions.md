# 06 Evals and observability - interview questions (concepts)

Status: beta | Teaches: [06 Evals and observability](../../06-evals-and-observability/) | Part 1 of 2

1. What is a golden dataset, and what makes it "golden"?
The curated set of input-expected-output rows the system is regression-tested against - questions with expected intents, tool calls, or answer properties. Golden means curated from reality (real tickets, real questions), not synthesized from the author's imagination; and versioned, so a score means a score against a known set. The repo's own 30-row set with its 93.3 percent baseline is the reference example. Teaches: [01-golden-datasets](../../06-evals-and-observability/02-golden-datasets.md).

2. Exact-match vs LLM-as-judge: when is each the right evaluator?
Exact-match for discrete, checkable outputs - intent labels, tool names, argument fields - where correctness is a fact. LLM-judge for open-ended outputs - tone, completeness, faithfulness - where correctness is a judgment, with a strict rubric prompt and spot-checked agreement with human grades. The bar: name the judge's own failure mode (leniency drift, position bias) and its control (calibration against a human-labeled subset). Teaches: [02-llm-as-judge](../../06-evals-and-observability/03-llm-as-judge.md).

3. What is a trajectory evaluation?
It checks the path, not just the endpoint: which nodes fired, which tools were called in what order, whether a forbidden action occurred. Endpoint evals pass systems that reached the right answer dangerously - 12 steps, a blocked tool attempted, a refund proposed without approval. Trajectory evals catch what the endpoint hides. Teaches: [03-trajectory-evals](../../06-evals-and-observability/04-protocol-evals.md).

4. What does tracing give you that logging does not?
Structure aligned with execution: spans per node and per tool call, inputs and outputs linked into the run's causal chain, token costs per step. Logs answer "what did I print"; traces answer "what did the run do and where did it go wrong" - the debugging unit for agents, and the substrate trajectory evals read from. Teaches: [04-langsmith-tracing](../../06-evals-and-observability/05-langsmith-tracing.md).

5. Why do agent regressions need CI gating instead of spot checks?
Because agent behavior shifts with prompt edits, model tier swaps, and tool description changes - none of which are code in the traditional sense. Without a gate, the regression ships silently and surfaces as user complaints. The gate's design: fast (a minute), keyless or cheap (deterministic checks by default), and blocking on the metrics you declared. Teaches: [05-ci-regression-suites](../../06-evals-and-observability/07-regression-suites-in-ci.md).

6. What are the two cost metrics that matter, and how do they differ?
Cost per request (what the customer's interaction costs - the product-economics number) and cost per task outcome (what a solved problem costs - the efficiency number that reflexion tiers and model tiers move). Reporting only the first hides that retries and loops burn money; reporting only the second hides volume. Teaches: [06-cost-and-latency](../../06-evals-and-observability/06-cost-and-latency.md).

7. What latency numbers do you track for an agent, and which one does the user feel?
p50 and p95 per turn, time-to-first-token, and per-node latency. The user feels time-to-first-token and the count of intermediate steps - which is why streaming and progress events are UX answers to latency problems, not decorations. Teaches: [06-cost-and-latency](../../06-evals-and-observability/06-cost-and-latency.md).

8. How do you evaluate a refusal?
As a first-class correct behavior with its own rows: questions the system must not answer (out of scope, no coverage, forbidden) with expected refusal - and confabulation as the failure. The metric: refusal correctness - refusing what should be refused, answering what should be answered. Systems optimized only on answer quality learn to always answer; that is the trap this metric exists to catch. Teaches: [01-golden-datasets](../../06-evals-and-observability/02-golden-datasets.md).

9. What is the baseline's job in an eval suite?
To make regressions visible: the recorded score the current score is judged against, so "we changed the prompt and the number moved from 93.3 to 88" is a fact, not a feeling. The discipline: baselines update deliberately, with a changelog entry - not silently whenever someone re-runs the suite. Teaches: [05-ci-regression-suites](../../06-evals-and-observability/07-regression-suites-in-ci.md).

10. Judge calibration - concretely, how do you trust an LLM judge?
Sample pairs, human-grade them, measure agreement (percent agreement and where they diverge), fix the rubric prompt where they diverge, re-run. Track judge drift over time - judges get lenient with their own model family's outputs. An uncalibrated judge is a random number generator with good formatting. Teaches: [02-llm-as-judge](../../06-evals-and-observability/03-llm-as-judge.md).

11. What does "evals first" mean as a workflow, not a slogan?
Write the failing case as a row before writing the fix: the bug report becomes an eval row, the fix becomes the change that turns the row green, and the row stays forever as the regression net. This is the discipline that separates teams that ship agent improvements from teams that ship agent churn. Teaches: [01-golden-datasets](../../06-evals-and-observability/02-golden-datasets.md).

12. Online vs offline evaluation - what is the difference and what does each catch?
Offline runs the golden set against a candidate build pre-merge; online measures live traffic - dashboards, sampled trace review, user feedback. Offline catches regressions before users; online catches what the golden set missed (distribution drift, novel inputs) and feeds back into new golden rows. The loop between them is the whole system. Teaches: [05-ci-regression-suites](../../06-evals-and-observability/07-regression-suites-in-ci.md) and [07-continuous-improvement](../../08-production/07-continuous-improvement.md).
