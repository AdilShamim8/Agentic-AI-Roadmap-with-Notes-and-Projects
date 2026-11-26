# Resume and portfolio

Module: 10-interview-preparation
Chapter: 16-resume-portfolio
Status: beta
Last reviewed: 2026-11-26
Estimated time: 1 hour

## Learning objectives

- Write agentic AI resume bullets that survive the six-second scan and the ATS
- Build the portfolio page that makes the GitHub evidence findable
- Cut what does not signal: the skill walls, the certificates, the summaries

## The bullet formula

Every bullet: verb, system, mechanism, number. "Built a customer support agent in LangGraph with a human approval gate on refunds and a 30-row eval set held at 93 percent intent accuracy in CI; deflection and escalation measured monthly." That single bullet tells a technical reader: graphs, interrupts, evals, CI, and product metrics - the entire curriculum in one line.

Compare the anti-patterns: "Experienced with LangGraph and LLMs" (a skill wall line, zero signal); "Responsible for agent development" (a job description, not work); "Improved agent performance" (no mechanism, no number). Mechanics and numbers are the difference; the formula is not decoration, it is the minimum a skeptical reader can verify.

## The resume skeleton

One page, this order:

1. Header: name, location, links - GitHub, portfolio, LinkedIn. No summaries, no photos.
2. Experience, reverse-chronological, three to five bullets each, every bullet on the formula. If your agent work is not your day job yet, the bullets describe the shipped internal tool anyway - "built for the support team" is real experience.
3. Projects (three): the primaries from [15 Project stories](15-project-stories.md), each with the pitch line and its number, linked to the repo.
4. Skills as a single line of grouped nouns: "Python, TypeScript; LangGraph, MCP, A2A; Postgres, Redis; pytest, LangSmith." Walls of logos and 40-item lists read as padding.
5. Education last, one line, unless it is the strongest thing on the page.

## What to cut

- The objective statement. It says what you want; the resume exists to say what you did.
- Certificates, unless the posting names one. Course-completion lists read as beginner markers; shipped projects do not.
- Every technology you would not defend in an interview. The skills line is a promise list, and "I listed it but never used it in anger" is a real interview answer that ends loops.
- The second page. Density beats length, and senior readers stop at one.

## The portfolio page

A single page (GitHub profile README or a static page) with one job: route a reviewer to evidence in under 30 seconds. Contents, in order:

1. One paragraph: what you build (agents in LangGraph, evaluation-first).
2. The three primary projects, each: pitch line, the number, the link, one screenshot or trace excerpt.
3. Links to the curriculum work: the [eval harness](../../projects/10-eval-harness-and-benchmark/README.md), the [retrieval demo](../../examples/retrieval_demo.py), the write-ups.

The screenshot of a LangSmith trace or an eval run output is the highest-signal image available - it shows the artifact working, not a stock robot.

## The ATS facts

Applicant tracking systems mangle creative layouts: columns, icons, headers, tables. Plain single-column Markdown-to-PDF, standard section names, no tables. Keywords matter less than claimed: the loop that matters has a human technical reader, and they are scanning for mechanisms and numbers, not acronyms. Write for the engineer; keep the format dumb enough for the parser.

## The honesty ledger

Keep a private file: every number on the resume with its source and date. "93 percent intent accuracy, 30-row set, run of 2026-10-19" is defensible in the loop; "about 90 percent, roughly" decays into a hedge when an interviewer presses. Numbers you can defend are worth three numbers you cannot.

## What is next

[17 GitHub hygiene](17-github-hygiene.md) - making the profile itself part of the evidence.
