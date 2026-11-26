# Interview guide - Project 04: Self-healing code agent

Status: beta | For: presenting this project in interviews | Related: [project README](README.md), [project stories](../../10-interview-preparation/15-project-stories.md)

## The pitch

"Run-tests, diagnose, patch, re-run - an agent that fixes failing tests in a repo. It proposes diffs and never applies them: the CI pipeline applies, and after two failed patch attempts it escalates to a human. Autonomy is earned by the strength of the check, and here the check is the test suite itself."

## The whiteboard script

1. State: the failing test output, the diagnosis (structured), the patch draft (a diff), `attempt_count`.
2. The diagnose node - reads the failure, localizes with repo tools (read file, get blame), writes a hypothesis.
3. The patch node - emits a diff into state; the apply step is OUTSIDE the agent, in CI.
4. The re-run node - executes the suite; green exits, red loops back with the new failure.
5. The escalation edge - `attempt_count >= 2` routes to a human with the diagnosis trail attached.

The line that earns the nod: "The agent proposes; the pipeline disposes."

## The numbers you quote

- Two-attempt escalation threshold - a policy constant with a reason (diminishing returns and review cost).
- Fix rate on your test set if measured; otherwise the scoping statement: bugfix-shaped tasks, not architecture.

## The follow-ups

- "What stops it from making things worse?" The patch is a proposal; CI applies and the suite verifies; a failed attempt cannot silently degrade the repo because nothing merges without green.
- "Why two attempts?" Third attempts rarely succeed and burn review context; the threshold is measurable and adjustable - a policy, not folklore.
- "What tasks are out of scope?" Architecture changes, multi-file refactors - anything whose correctness the suite cannot check. Autonomy scales with the check.
- "Is this safe to run on a real repo?" Scoped read/propose tools, no merge rights, sandboxed test execution - the same boundary discipline as any destructive agent.

## The red flags

- Describing it as "an agent that writes code autonomously" - the proposing-not-applying distinction IS the design.
- No escalation path - unbounded retry loops are the failure story this project exists to avoid.
- Claiming general SDLC autonomy; scope honesty is the senior signal.

## What this project proves

Autonomy as a bounded spectrum: verification-driven loops, escalation policy, and the restraint that platform and dev-tools loops screen for hardest.
