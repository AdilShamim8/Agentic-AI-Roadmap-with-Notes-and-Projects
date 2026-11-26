# Company research

Module: 10-interview-preparation
Chapter: 18-company-research
Status: beta
Last reviewed: 2026-11-26
Estimated time: 1 hour

## Learning objectives

- Research a company in one focused hour and surface in the loop informed
- Read the team stage from the posting and the interview loop itself
- Ask the questions whose answers actually predict whether the role is good

## The one-hour research block

Per company, before the first technical round:

1. The product, 15 minutes. Use it, or use the demo, or read the docs like a user. In the interview, one sentence of grounded product observation ("the citation links in your assistant are clickable, which most are not") is worth an hour of praise.
2. The engineering blog and talks, 20 minutes. What they have shipped, what they have learned, what they are proud of. Note one post you can reference honestly.
3. The team, 10 minutes. Interviewer names on LinkedIn: their scope, tenure, background. Tenure distribution predicts stage - a founding-team cluster around a new manager is a rebuild; long tenures under stable leadership is a maintenance-or-scale org.
4. The business situation, 10 minutes. Funding stage or earnings, layoff history, the AI bet they have announced. You are checking whether the role survives the next two quarters.
5. The posting, 5 minutes, again. Read the requirements as the team's self-diagnosis: "we need someone to own evals" reads entirely differently from "we need someone to ship the first agent."

## Reading the team stage

The stage decides the job you are actually applying for, whatever the title says:

- Prototype stage (no agent in production). The role is "make it real": evals, deployment, reliability. Highest autonomy, highest risk of the project being cancelled by a pivot.
- Scaling stage (agent shipped, usage growing). The role is "make it hold": cost, latency, multi-tenancy. The eval culture either exists (ask) or you are building it.
- Platform stage (multiple teams, agents everywhere). The role is "make it repeatable": tool servers, standards, the MCP/A2A boundary work. Least ambiguity, most coordination.

Ask which stage, directly: "Is the agent in production today, and what is the next reliability problem on the roadmap?" The answer recalibrates every story you tell - the [project stories](15-project-stories.md) chapter maps platform-loop stories (7, 9) and product-loop stories (1, 2, 10).

## The questions whose answers matter

In the loop, ask two of these, of people who will actually answer:

- "Walk me through what happens when the agent breaks in production at 2 a.m." The answer reveals on-call reality, monitoring depth, and whether they are lying to themselves about reliability.
- "Who owns the eval set, and when did a regression gate last catch something?" If nobody owns it, the team is prototype-stage regardless of what they said.
- "What did the last person in this role move on to?" Legitimate exits are fine; the evasive answer is the signal.
- "What is the decision I would be making in month three?" A real answer means the role has scope; "you would be ramping" means the backlog is undefined and you will be assigned whatever nobody wants.

## The fit ledger

Write four lines per company before the loop: the stage, the one engineering post you can cite, the answer you want to hear on the eval question, and your walk-away condition (comp floor, on-call shape, manager quality). The ledger keeps the process a decision instead of a pursuit - the posture that [20 Offer decision](20-offer-decision.md) requires and that candidates without one cannot fake.

## What is next

[19 Negotiation](19-negotiation.md) - the bands, the anchors, and the timing.
