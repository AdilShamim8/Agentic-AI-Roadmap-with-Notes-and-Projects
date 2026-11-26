# Quiz 06 - Evals and observability

Status: beta | Covers: [06 Evals and observability](../../06-evals-and-observability/) | 10 questions

1. A dataset is "golden" when:
A) It has 1,000+ rows
B) It is curated from real traffic and versioned
C) The judge scores 100 percent
D) It lives in a spreadsheet

2. Exact-match evaluators suit:
A) Tone
B) Discrete outputs - intents, tool names, argument fields
C) Open-ended summaries
D) Nothing in agents

3. Trajectory evaluation catches what endpoint evals miss:
A) Grammar errors
B) The path - loops, forbidden actions, extra steps
C) Token costs only
D) Provider outages

4. An LLM judge is trustworthy after:
A) One successful run
B) Calibration against human-graded samples, with drift tracking
C) Choosing the largest model
D) Prompting it to be strict

5. CI gating matters for agents specifically because:
A) Builds are slow
B) Behavior shifts from prompts, tiers, and tool descriptions - not just code
C) Providers require it
D) It replaces code review

6. Cost per task outcome differs from cost per request by counting:
A) Only failed requests
B) What a solved problem costs, including retries and loops
C) Provider credits only
D) The user's time

7. The latency number the user actually feels:
A) p99 total
B) Time-to-first-token and visible step count
C) Model queue depth
D) Cold start

8. Refusal correctness measures:
A) How often the model says no
B) Refusing what should be refused AND answering what should be answered
C) User frustration
D) Judge agreement

9. The baseline's job:
A) To be the marketing number
B) To make regressions visible as deltas from a recorded score
C) To cap performance
D) To train the model

10. "Evals first" as a workflow means:
A) Evaluating the team weekly
B) The bug becomes a row before the fix ships
C) Judging everything with LLMs
D) Writing evals after launch when data exists

## Answer key

1. B - reality-sourced and versioned ([chapter 01](../../06-evals-and-observability/01-golden-datasets.md)).
2. B - correctness as fact, not judgment ([chapter 01](../../06-evals-and-observability/01-golden-datasets.md)).
3. B - right answer reached dangerously still fails ([chapter 03](../../06-evals-and-observability/03-trajectory-evals.md)).
4. B - agreement measured, rubric fixed where it diverges ([chapter 02](../../06-evals-and-observability/02-llm-as-judge.md)).
5. B - the change surface is wider than code ([chapter 05](../../06-evals-and-observability/05-ci-regression-suites.md)).
6. B - the efficiency number tiers and loops move ([chapter 06](../../06-evals-and-observability/06-cost-and-latency.md)).
7. B - streaming is the UX answer to latency ([chapter 06](../../06-evals-and-observability/06-cost-and-latency.md)).
8. B - always-answering is the trap this metric catches ([chapter 01](../../06-evals-and-observability/01-golden-datasets.md)).
9. B - "the number moved" becomes a fact ([chapter 05](../../06-evals-and-observability/05-ci-regression-suites.md)).
10. B - the row stays as the regression net ([chapter 01](../../06-evals-and-observability/01-golden-datasets.md)).
