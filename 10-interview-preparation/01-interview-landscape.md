# The interview landscape

Module: 10-interview-preparation
Chapter: 01-interview-landscape
Status: beta
Last reviewed: 2026-11-26
Estimated time: 1 hour

## Learning objectives

- Name the rounds in a typical agentic AI engineer loop and what each one screens for
- Understand how the debrief turns round feedback into a hire/no-hire decision
- Recognize the two loop variants (agent-heavy vs platform-heavy) and prepare differently for each

## The standard loop

Most loops for agentic AI engineer roles have four to five rounds, and take three to six weeks from first contact to offer. The [field guide](../field-guide/05-interview-prep.md) covers the baseline; this chapter adds what each round is actually filtering for.

1. Recruiter screen, 30 minutes. Screens: communication, expectations, timeline. Not technical. Most rejections here are self-inflicted: unprepared answers on compensation or location. Chapter 02.
2. Hiring manager round, 45 minutes. Screens: scope of past work, ownership, judgment. The candidate who lists tools loses to the one who describes decisions. Chapter 03.
3. Technical screen, 60 minutes. Screens: can you write graph code under mild time pressure, and is your tool and state design sound. Chapter 04.
4. Take-home assignment, three to seven days. Screens: product taste, code hygiene, eval thinking - on your own time. Chapters 12 and 13.
5. Onsite, three to four hours. System design, more coding or a trace-reading exercise, behavioral, and a deep-dive on the take-home. Chapters 05-11 and 23.

Some companies merge rounds or run them in a different order. Two companies, same title, can weight the rounds completely differently. Ask the recruiter for the loop structure in the first call - a serious recruiter will tell you the rounds and who runs them.

## Two loop variants

Agent-heavy loops (product teams shipping agents) weight system design and product sense. Expect cases like "design a support agent for us" and a long take-home. The eval plan in your answer matters as much as the architecture.

Platform-heavy loops (infrastructure teams building the agent platform) weight the coding screen and operational depth. Expect questions on checkpointing backends, deployment, multi-tenancy, and cost. Your answer should volunteer numbers: requests per second, cost per request, p95 latency.

The failure mode is preparing for the wrong variant. A platform loop does not want to hear a 20-minute riff on prompt patterns; an agent loop does not want your Kubernetes manifest war stories without a product framing. The job posting and the interviewer titles tell you which loop you are in - engineers on product teams interview differently from platform engineers.

## How the debrief decides

Each interviewer files written feedback, usually a score on a small set of axes (technical depth, system design, communication, ownership signal, culture) plus a recommendation. The debrief then argues toward one of:

- Strong hire: overperforming on at least one axis, no red flag on any.
- Hire: meets the bar on every axis, no red flags.
- No-hire: one or more axes below bar, or a single red flag. Red flags are things like "could not explain his own project's architecture," "dismissed evaluation as overhead," or "blamed teammates for the failed project."

Two properties of this decision matter to you. First, a single below-bar round is usually fatal, so your weakest round matters more than your strongest. Second, "no red flags" does as much work as brilliance - the candidate with no mistakes beats the candidate with one brilliant round and one shaky one. Prepare for consistency, not peaks.

## The selection mindset

Interviews are not exams you pass with correctness points; they are risk assessments the panel runs on you. Every answer either adds signal ("this person has done this") or adds risk ("this person might not have"). The chapters that follow are organized around lowering risk per round:

- Say what you have actually shipped, with numbers, and mark the rest as reasoning ("I have not run this at scale; here is how I would reason about it").
- Volunteer the failure modes and the eval plan before being asked. It is the single strongest signal this curriculum can teach, and it is rare in candidates.
- When you do not know, say so, then reason aloud from something adjacent you do know. A confident wrong answer is a red flag; a bounded "here is where my knowledge ends" is a signal.

## Prerequisites

- [The interview process overview](../field-guide/05-interview-prep.md) - the shorter, numbers-first version

## What is next

[02 Recruiter screens](02-recruiter-screens.md), the round most candidates lose before anyone technical looks at them.
