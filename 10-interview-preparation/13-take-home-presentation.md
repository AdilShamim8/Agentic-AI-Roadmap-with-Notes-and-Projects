# Take-home presentation

Module: 10-interview-preparation
Chapter: 13-take-home-presentation
Status: beta
Last reviewed: 2026-11-26
Estimated time: 1 hour

## Learning objectives

- Structure the walkthrough call so the rubric lines get hit on schedule
- Answer the deep-dive questions reviewers use to test authorship
- Handle the "what would you do with more time" question as an opportunity

## The walkthrough call

Thirty to sixty minutes with one or two engineers who have read your submission. They want to know three things: did you actually build it; can you defend the decisions; and what is it like to work with you when the artifact is under discussion. The call is won in the first ten minutes and lost in the last ten - the opener proves authorship, the closer proves judgment.

## The five-minute opener

Do not tour the code file by file. Open with the decisions:

1. The one-line framing: "A single-agent support flow with two scoped tools, an approval interrupt on the refund action, and a 10-row eval that scores intent and tool choice."
2. The decision you are proudest of and why: "The refund gate is structural - `interrupt()` before the tool call - because prompt-level instructions do not survive a model swap."
3. The number: "The eval runs at 9 of 10 on intent, and the miss is the billing-vs-shipping ambiguity, which I documented rather than fixed."

Then stop talking and let them choose the thread. Reviewers with questions want to ask them; an unprompted ten-minute code tour reads as anxiety.

## The deep-dive questions

Authorship probes, and the answers that hold:

- "Why this state schema?" Point at the fields and their writers: "Messages accumulate through the reducer; `pending_action` is written only by the proposal node and cleared only by the resume handler - single-writer fields, so the state machine stays checkable."
- "What happens if the tool fails?" Have the actual path: "The tool returns a structured error, the agent tells the user and offers escalation; the retry policy is one retry in the tool layer, not the model's decision."
- "Why not multi-agent?" The brief did not justify it: "Two tools and one domain - the coordination cost buys nothing. If the domain split, I would split it."
- "Change this design decision" (they pick one, e.g., swap the model tier): reason live, out loud, from cost and latency: "Dropping to a cheaper class for the intent step is safe because it is classification; the compose step I would keep strong because it is user-facing."

If you did not write a line someone asks about, say so in plain words: "I adapted that reducer from the LangGraph docs pattern; here is why it fits." Honesty survives; bluffing does not, and reviewers deliberately ask about the part you are weakest on.

## Live coding on your own base

Half of walkthroughs include "extend it live": add a tool, add an eval row, add the feature you de-scoped. The winning move is the one you prepared: you listed the extension in the README's "with more time" section, so you have thought about it. Ten minutes of typed, narrated work on a codebase you know cold is the strongest authorship proof available.

## "What would you do with more time?"

Have exactly three items, ordered, each one sentence with a reason:

1. The eval that would catch the documented miss: "Twenty more rows, weighted toward the ambiguous categories, because the 10-row set under-samples them."
2. The persistence upgrade: "Postgres checkpointer - in-memory loses conversations on restart."
3. The product edge: "Streaming responses, because first-token latency is the UX complaint the real system gets."

Three, not ten. A list of ten reads as no judgment; three ordered items with reasons reads as exactly what they would ask you to do next quarter.

## The close

Ask one question that only the reviewer can answer: "What did the strongest submission you have seen do that mine did not?" You get a rubric hint for next time, and the question itself signals that you think in feedback loops.

## What is next

[14 Behavioral STAR bank](14-behavioral-star-bank.md) - the 30 questions that recur across every loop.
