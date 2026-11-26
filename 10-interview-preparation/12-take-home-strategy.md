# Take-home strategy

Module: 10-interview-preparation
Chapter: 12-take-home-strategy
Status: beta
Last reviewed: 2026-11-26
Estimated time: 1 hour

## Learning objectives

- Scope a take-home to what the rubric actually grades
- Budget the days you have instead of spending them on the wrong part
- Avoid the four failure modes that sink otherwise good submissions

## What the take-home grades

The assignment brief says "build a small agent." The rubric behind it grades five things, roughly in this weight: working code the reviewer can run; sensible architecture (state, tools, loop design); an eval story (some measurement, even 10 rows); code hygiene (readable, typed, a README that says how to run it); and restraint - scope that matches the brief. Polish beyond that is wasted; its absence is fatal.

## Scoping before typing

Read the brief twice, then write the one-paragraph "what I will build" and the explicit non-goals list. Example, for a support-agent brief: in scope - the graph, two tools, the approval interrupt, a 10-row eval; out of scope - auth, streaming, a frontend, Postgres (SQLite or in-memory checkpointer instead). Non-goals stated in the README read as judgment; unstated, they read as gaps.

The repo's projects give calibrated scope targets: the [customer support project](../../projects/02-customer-support-multi-agent/README.md) and its solution show what a complete-but-bounded submission looks like. Match that size and stop.

## The time budget

Take-homes are usually scoped at 4 to 8 hours; candidates spend 20. Spend deliberately, in this order:

1. One hour: the skeleton - state schema, empty nodes, the wiring. Run it.
2. One to two hours: tools and the loop. Run it again; the agent should complete the happy path.
3. One hour: eval - a small CSV, a script that scores it, the number in the README.
4. One hour: README - run instructions, design decisions, non-goals, what you would do with more time.
5. Remaining: the edge cases you listed as in-scope, tests for the tool layer.

The order matters because the rubric's top lines are satisfied by hour four. Everything after is bonus that stops counting once you stop running the code.

## The four failure modes

1. The non-running submission. The reviewer clones it, the command in the README fails, and the score drops past recovery. Prevention: fresh clone, fresh venv, run the exact README command, before submitting. This is the cheapest point on the entire loop.
2. The scope explosion. A frontend, three agents, a vector store - for a brief that asked for one agent and two tools. The reviewer reads it as poor judgment under ambiguity, which is the thing they were testing. Ship the non-goals list instead.
3. The missing eval. An agent submission with no measurement reads as pre-2022 instincts. Ten rows of golden data and a printed score line turn "hobby project" into "engineering artifact." The [eval module](../../06-evals-and-observability/) and `run_evals.py` in [examples/](../../examples/) are the template - copy the shape, not the size.
4. The unreadable README. The reviewer grades what they can find. Run command, one architecture paragraph, the eval number, the decisions you made and why, the non-goals. Six sections, one page.

## Secrets and hygiene

- No real API keys anywhere. `.env.example` with the variable names, `.env` in `.gitignore`, a keyless demo mode if you can manage it (the repo's demos show the pattern - scripted fallbacks so the reviewer without keys still sees the loop run).
- Type hints, lint-clean, no dead code. The reviewer is an engineer; the diff is your interview.
- Commit history in logical steps. A single "final" commit is a signal; a dozen honest ones ("add interrupt before refund tool," "golden set, 10 rows") read as a professional habit. This repo's own history is the model.

## What is next

[13 Take-home presentation](13-take-home-presentation.md) - the walkthrough call, where the submission gets defended.
