# Interview guide - Project 10: Eval harness and benchmark

Status: beta | For: presenting this project in interviews | Related: [project README](README.md), [project stories](../../10-interview-preparation/15-project-stories.md)

## The pitch

"The measurement machine itself: a 30-row golden set from real traffic, exact-match evaluators for intents and tool calls, an LLM-judge for open-ended responses, and a CI gate that blocks regressions before users see them. The baseline is honest - 93.3 percent - because a cherry-picked baseline is a lie you have to keep living."

## The whiteboard script

1. The golden set - rows of input, expected intent, expected tool, expected args; sourced from reality, versioned.
2. The evaluators - exact-match for the discrete fields; the judge with a strict rubric, calibrated against human grades.
3. The runner - loads the CSV, executes, scores, writes the report.
4. The CI gate - the suite runs keyless and fast; the baseline is recorded; movement is a fact.
5. The feedback loop - production complaints become new rows; the suite models the users.

The line that earns the nod: "A gate that gets skipped is a gate that was too big - so it runs in minutes, keyless, blocking."

## The numbers you quote

- 30 rows, 93.3 percent intent accuracy baseline (the repo's real numbers - quote yours if you rebuilt).
- Judge agreement with human grades after calibration (single-digit disagreement or keep calibrating).
- Gate runtime in CI (minutes).

## The follow-ups

- "Thirty rows is small." Curated-from-reality beats large-and-synthetic for regression work; the set grows where the traffic is, and the complaint loop decides where that is. Say the growth policy, not an apology.
- "Why exact-match at all?" Discrete correctness is a fact; the judge is for judgment. Mixing them muddles both.
- "How do you know the judge is right?" Calibration: human-graded sample, disagreement analysis, rubric fixes, re-run - and quarterly recalibration, because judges drift lenient.
- "What made it into the gate vs nightly?" Facts block (exact-match, trajectory checks); judgment samples (judge on a subset). Five minutes or developers bypass it.

## The red flags

- Presenting evals as a report someone reads weekly instead of a gate something enforces.
- The uncalibrated judge - a random number generator with good formatting.
- A baseline that moved silently after a re-run.

## What this project proves

The eval-first identity: measurement as engineering discipline, gates as culture, honesty as policy - the strongest story for reliability-focused roles, and the appendix every other project quotes.
