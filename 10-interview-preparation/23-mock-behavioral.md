# Mock: behavioral

Module: 10-interview-preparation
Chapter: 23-mock-behavioral
Status: beta
Last reviewed: 2026-11-26
Estimated time: 45 minutes

## Learning objectives

- Watch STAR answers land inside two minutes with the follow-up survived
- See the difference between an owned failure story and a disguised success story
- Drill the three questions that end otherwise-passing loops

## How to read the transcript

The interviewer asks four questions, chosen from the [STAR bank](14-behavioral-star-bank.md) families that fail most often: ownership, a wrong decision, an agent-specific incident, and the motivation question. Commentary marks the moves that scored and the places the same answer goes wrong in real loops.

## The transcript

Interviewer: "Tell me about a project you shipped end to end."

Candidate: "The support agent for our internal helpdesk. About 40 percent of tickets were password resets and software requests - pure deflection value. I built a single-agent system in LangGraph: identity verification as a server-side tool, the reset action executing directly, installs queued to the approval flow. I wrote a 30-row golden set from last quarter's actual tickets and held the line at 93 percent intent accuracy in CI before we opened it to users. Deflection settled at about 30 percent of those categories in month one, and the eval gate caught two regressions when we swapped model tiers. Next step when I left was Postgres checkpointing for multi-session memory."

[Commentary: two minutes, STAR with the weight on Action and Result, three numbers that survive follow-ups. Note what is absent: no tool inventory, no team chronology, no adjectives. The "next step" sentence signals ongoing ownership of a system that is no longer hers - interviewers notice.]

Interviewer: "What was the hardest bug?"

Candidate: "The agent called the reset tool twice for one request - the second call fired after the user confirmed, because the resume path re-entered the node that had already executed. The symptom was a duplicate email; the cause was my node doing both propose and execute. The fix was structural: propose and execute became separate nodes, and the edge after resume routes to execute only. I added a trajectory eval row - 'a reset request results in exactly one reset call' - so the CI gate owns it now, not my memory."

[Commentary: an owned failure with a mechanism, a fix, and a prevention. The last clause - "not my memory" - is the engineering-culture signal managers write down. The wrong version of this answer: "a weird race condition that was hard to find," no cause, no prevention.]

Interviewer: "Tell me about a technical decision you got wrong."

Candidate: "I shipped the first version with no eval set - it was a two-week pilot and I optimized for the demo. A prompt tweak in week two silently broke the escalation path; users got confident refusals instead of a human handoff, and it ran four days before anyone noticed. That one is on me: I treated evaluation as overhead during a pilot, which is exactly when regressions are cheapest to catch and most expensive to be seen by users. The golden set and the CI gate came out of that week, and the incident is the reason the eval module exists in my current project at all."

[Commentary: real cost, full ownership, one sentence of reflection, zero self-flagellation, and a durable artifact named. This answer, told this way, is worth more than a success story - the panel is hiring the person who made the mistake, not the mistake.]

Interviewer: "Why agentic AI?"

Candidate: "Because it is the first time the engineering problem and the interesting problem are the same one: making a system that plans be reliable enough to touch users. I like that the hard parts are mine - state design, tool boundaries, evaluation - not a vendor's roadmap. And I like that the feedback loop is short: you can measure an agent's behavior this week and change it next week. The eval work is what convinced me to stay; once you instrument the loop, it is real engineering."

[Commentary: a product-and-craft answer, no hype vocabulary, no 'change the world', and it happens to be true of this repo's whole approach. The wrong version mentions 'transformative' or the salary, and everyone in the room hears it.]

## The three loop-enders

1. The disguised success story for "tell me about a failure." Interviewers hear the disguise instantly - the question tests honesty, not resilience. Have a real one with a real cost.
2. The teammate villain. Any story where the failure was "the data team" or "the backend guy" reads as not-yet-senior. Recast: the miscommunication was the failure, and your part in it leads the sentence.
3. The answer that is about the technology instead of the decision or the person. Behavioral rounds score people-signal; a four-minute architecture monologue scores zero on every axis being graded.

## The drill

Take the four questions in this transcript. Record yourself answering each, two minutes, once a day for three days. On day three, have someone interrupt you mid-answer with "what would your manager say about that?" - the follow-up drill. If you can finish that sentence without pausing, the round is ready.

## What is next

[24 Four-week sprint](24-four-week-sprint.md) - the plan that assembles everything into a calendar.
