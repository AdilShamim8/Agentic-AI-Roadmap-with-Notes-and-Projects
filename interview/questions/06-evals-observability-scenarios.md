# 06 Evals and observability - interview scenarios

Status: beta | Teaches: [06 Evals and observability](../../06-evals-and-observability/) | Part 2 of 2

1. "You inherit an agent with zero evaluation. Build the practice in week one."
Start from reality: pull the last 100 real requests, cluster them into task families, and write 30 golden rows weighted to the top families - real inputs, expected behavior, with unanswerable cases included. Add the cheap evaluators first (intent and tool exact-match), run the suite in CI keyless, and record the honest baseline. The trap to name: building the perfect 500-row judge-based suite in week one and shipping no gate at all - a small gate now beats a great gate never. Teaches: [01-golden-datasets](../../06-evals-and-observability/02-golden-datasets.md).

2. "A prompt change bumped the golden set from 93 to 96 but users complain more. What is going on?"
The golden set's distribution is not the traffic's distribution: the change fixed measured cases and broke unmeasured ones - or the judge drifted. Diagnose: segment live complaints by task family, map them onto golden rows, and find which family the set under-represents. The fix: new rows from the actual complaints, then re-run both scores. The principle: the suite is a model of your users, and model drift is a suite bug. Teaches: [01-golden-datasets](../../06-evals-and-observability/02-golden-datasets.md).

3. "Design the eval gate for a refund-approving support agent. What must it block?"
Three layers: endpoint (intent and tool exact-match on the 30-row set), trajectory (a refund over the threshold never executes without an approval-resume event; no duplicate refund calls), and response (LLM-judge on tone and completeness, sampled). Gate blocks on the first two always, the third on a threshold. The sentence that lands: the trajectory row IS the security test - prompt-level policy has no gate. Teaches: [03-trajectory-evals](../../06-evals-and-observability/04-protocol-evals.md).

4. "Your judge disagrees with your own grades 20 percent of the time. Fix the judge."
Calibrate by disagreement analysis: bucket the disagreements - leniency (judge passes what you fail), rubric ambiguity (both defensible), position bias. Fix the rubric prompt per bucket - concrete anchors, required evidence quotes, a forced fail condition. Re-run against the human-labeled set until agreement is in the low single digits, and re-calibrate quarterly. Teaches: [02-llm-as-judge](../../06-evals-and-observability/03-llm-as-judge.md).

5. "Cost per request rose 40 percent this week. Walk the investigation in traces."
Group runs by task family and compare token spend per node against last week: the usual suspects are a tool returning more, a new step in the trajectory (loop or retry), or a model-tier change. The trace view answers in minutes because cost is per-span; the log view cannot answer at all. Land the fix structurally - bound the tool, cap the loop, or re-tier the step - and add the cost metric to the gate so the next 40 percent announces itself. Teaches: [06-cost-and-latency](../../06-evals-and-observability/06-cost-and-latency.md).

6. "The team wants to ship a new model tier because it 'feels better.' What do you demand?"
The comparison run: golden set on both tiers, side by side, plus cost and latency per task family, plus the trajectory check (new tiers sometimes change tool-call habits). Feel is a hypothesis; the suite is the test. If it is genuinely better on the metrics, ship and update the baseline with a changelog entry. Teaches: [05-ci-regression-suites](../../06-evals-and-observability/07-regression-suites-in-ci.md).

7. "Users cannot tell you what went wrong - only 'it got dumb.' Build the observability that catches it."
The user-felt metrics: task completion (did the conversation end resolved), escalation rate, time-to-first-token, and step count per task. Dashboard them by task family and day; alert on step-count and escalation anomalies, which are the early symptoms of routing or tool regressions. Then the loop: sampled trace review weekly, complaint inputs into golden rows. "It got dumb" is usually a 3-step task becoming an 11-step task - only trajectory metrics see it. Teaches: [04-langsmith-tracing](../../06-evals-and-observability/05-langsmith-tracing.md).

8. "Sales asks for 'an accuracy number' for the agent's quarterly review. What number do you give, and what caveats travel with it?"
The defensible composite: task-level accuracy on the golden set (with set size and date), refusal correctness, and the live task-completion rate - three numbers, not one, because each answers a different question. Caveats that travel: the set is a sample of real traffic, not all of it; the judge is calibrated but not human; and the trajectory gate covers the destructive path. One number without caveats is how the next quarter's slide becomes a lie. Teaches: [01-golden-datasets](../../06-evals-and-observability/02-golden-datasets.md) and [02-llm-as-judge](../../06-evals-and-observability/03-llm-as-judge.md).

9. "Your CI eval takes 25 minutes and developers are bypassing the gate. Rescue it."
Tier the suite: the blocking tier is fast and deterministic (exact-match rows, trajectory checks against recorded traces) under five minutes; the slow tier (judge-based, sampled) runs nightly or pre-release. Then make bypassing harder than waiting - the gate that gets skipped is the gate that was too big. The repo's own design is the template: keyless, minute-scale, blocking on facts. Teaches: [05-ci-regression-suites](../../06-evals-and-observability/07-regression-suites-in-ci.md).

10. "An intern asks: why not evaluate in production only, with user feedback? Answer like a mentor."
Because user feedback is late, biased (only the angry respond), unlabeled, and unethical as a first line - users are not your test harness, they are the people the harness exists to protect. Production measures what the offline suite missed and feeds it rows; the offline gate is what keeps the known regressions from ever meeting a user. Both, in that order of obligation. Teaches: [07-continuous-improvement](../../08-production/07-continuous-improvement.md).
