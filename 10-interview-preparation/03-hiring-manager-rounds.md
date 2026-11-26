# Hiring manager rounds

Module: 10-interview-preparation
Chapter: 03-hiring-manager-rounds
Status: beta
Last reviewed: 2026-11-26
Estimated time: 1 hour

## Learning objectives

- Run the hiring manager round around scope and ownership rather than tools
- Answer "walk me through your project" at the level the manager is listening for
- Handle the questions that probe judgment: disagreement, failure, leaving

## What the manager is screening

The hiring manager owns the outcome of your first year. Their round screens for three things the technical rounds under-weight: scope (have you owned problems this size), judgment (do you make decisions the way this team makes decisions), and coachability (can this person take a correction without breaking). The manager also reads for whether they want to be in your weekly one-on-one for a year. That last part is not removable from the process, so be a tolerable version of yourself for an hour: engaged, direct, not performed.

## "Walk me through your project"

This is the center of the round, and the level you answer at decides it. The manager is listening for: did you own the problem, or the task? Answer at the problem level.

Structure the answer in four moves, using a project from [projects/](../projects/) you actually built:

1. The problem and who had it: "Support was spending most of its time on order-status and returns, and the team wanted deflection on tier one without touching refund decisions."
2. The shape of your solution and one rejected alternative: "A single ReAct-style agent with scoped tools, and human approval on refunds. I considered a multi-agent split but the tool count did not justify it."
3. The measurement: "I built a 30-row golden set from real ticket categories and held the line at 93 percent intent accuracy before shipping; escalation rate dropped from 12 to 8 percent in the first month." (Substitute your real numbers; the structure is the point.)
4. What you would do next: "Streaming UX was the next ask, then Postgres checkpointing for multi-session memory."

Two minutes, and every sentence carries a decision or a number. If the manager wants depth, they will pull the thread - have the depth ready (chapter 15 maps all ten projects to this shape).

## The judgment questions

Managers probe judgment with the same handful of questions. Prepare one real story each, told without villains:

- "Tell me about a disagreement with a technical decision." The winning shape: you disagreed, you made your case with evidence, the decision went against you, you implemented it well, and the outcome taught you something specific. Losing the argument gracefully is the point of the question.
- "Tell me about a failure." Pick a real one with a real cost, then spend more time on the fix and the durable change than the failure. "We shipped without a regression eval and a prompt change silently broke the escalation path; I added a CI eval gate and a 30-row set, and it caught two regressions later" is a complete answer.
- "Why are you leaving?" The honest, forward answer: what you want next that the current role does not have. Never the grievance version.

## Questions the manager answers well

Ask these - each one produces information you cannot get elsewhere:

- "What does the first 90 days look like for this role?"
- "What is the current state of the agent system I would be working on - prototype, in production, or somewhere between?"
- "How does the team decide between shipping and evaluating?" The answer tells you whether the eval culture this curriculum treats as non-negotiable exists there.

## Red flags this round

- Describing your work in tool names ("we used LangGraph and MCP") instead of problems and outcomes.
- Every failure story is someone else's fault.
- No questions at the end. Managers read it as low interest in this job specifically, not as humility.

## What is next

[04 Technical screens](04-technical-screens.md), the live-coding round.
