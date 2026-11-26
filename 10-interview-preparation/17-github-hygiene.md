# GitHub hygiene

Module: 10-interview-preparation
Chapter: 17-github-hygiene
Status: beta
Last reviewed: 2026-11-26
Estimated time: 1 hour

## Learning objectives

- Make the GitHub profile and the portfolio repos pass a technical reviewer's two-minute audit
- Pinned repos, READMEs, commit history, and activity that read as a professional habit
- Avoid the profile smells that quietly down-level a candidate

## The two-minute audit

A technical interviewer who has your GitHub link does this: opens the profile, reads the bio line and pins, clicks the strongest pin, reads its README for 40 seconds, maybe opens one file, then glances at the contribution graph and the commit style. That is the whole audit. Everything below optimizes those two minutes.

## Profile-level

- Bio: one line with the specialty and the stack. "Agentic AI engineer - LangGraph, MCP, evaluation-first" beats a mission statement.
- Pin the three primary projects plus the curriculum repo. Six pins is the maximum; two strong and four stale is worse than three strong.
- The profile README (if you want one): the portfolio page from [16 Resume and portfolio](16-resume-portfolio.md), nothing else.

## Repository-level, per pinned repo

- The README first screen: what it is (one line), the number (eval accuracy, request rate), how to run it (copy-paste command), one screenshot or trace. Reviewers do not scroll; the first screen carries it.
- A real `.gitignore`, no committed secrets, no `.env`, no `egg-info`. Run a secret scan on your own history (`git log -p | grep -i "sk-\|api_key"` for the crude version); leaked-then-deleted keys still show.
- Commit history in logical steps with honest messages. A repo with one "initial commit" of 200 files reads as imported homework; a history that shows the eval set growing from 10 rows to 30 with a message each time reads as an engineer.
- Issues and PRs used on your own repos - the fix queue, the content suggestions - signal that you work in public the way teams work internally.
- MIT or Apache license on anything public you want copied; no license reads as ambiguous.

## The contribution graph

The graph is habit evidence, not volume evidence. A steady line of real commits on two or three projects beats a block-streak of gamey commits. Do not manufacture green squares; do commit the work you actually do, in logical units, as you do it. If you are working through this curriculum, the natural commit pattern is the evidence - and this repository's own history (13 curated commits across an audit, each one a reviewable unit) is the style to imitate.

## The smells that down-level

- Tutorial fingerprints: repos that are the LangGraph tutorial with your name in the README. The fix is the delta - state what you changed and why in the README, or fork quietly without pinning.
- The 40-repo graveyard: half-cloned tutorials and abandoned starters. Archive them; the profile should show intention.
- Credential commits. Grep your history before anyone else does.
- Activity spikes that match interview schedules exactly - recruiters compare timestamps more than you think.

## The curriculum-as-evidence play

If you are using this repo as your foundation, the strongest move is to fork it and do the work in the open: the projects, the eval extensions, the question-bank additions. Your fork's history becomes a months-long public work sample of exactly the skills the role wants - studying in public is hiring signal, not embarrassment. The [CONTRIBUTING.md](../CONTRIBUTING.md) bar gives your commits an editorial standard to meet, and meeting it is demonstrable craft.

## What is next

[18 Company research](18-company-research.md) - the loop prep that starts when the recruiter calls back.
