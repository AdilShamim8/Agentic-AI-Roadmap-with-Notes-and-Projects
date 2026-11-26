# Trace debugging round

Module: 10-interview-preparation
Chapter: 11-trace-debugging-round
Status: beta
Last reviewed: 2026-11-26
Estimated time: 1 hour

## Learning objectives

- Handle the "read this trace, find the bug" round that mature loops use instead of a second coding screen
- Walk a LangSmith-style trace systematically: steps, tokens, tool calls, errors
- Present a diagnosis with cause, fix, and prevention in under five minutes

## What this round is

The interviewer puts a real (or constructed) agent trace in front of you - a multi-step run with tool calls, a final answer, and something wrong with it: a loop, a wrong tool, an argument hallucinated, a step that never should have run. You have 20 to 30 minutes to find it. The round screens for exactly what the job is on a bad Tuesday: can you read execution, not just write it.

## The systematic read

Run this order every time, and say it as you go:

1. The final answer first. What did the user get? One sentence.
2. The step list. Count the steps, name each one - "plan, search, read, search again, read, compose." Compare against what the graph should have done.
3. The tool calls. For each: the arguments, the result, the token cost. This is where the bugs live: an `order_id` the user never gave, a query that ignores the previous result, a tool called twice with identical arguments.
4. The errors and near-errors. A caught exception, a fallback that fired, a step whose output looks fine but cost 60K tokens.
5. State at the end. What accumulated, what is missing - the message list without the system prompt, a scratchpad that was never cleared.

## The four classic bugs

Know them cold; they cover most constructed traces:

1. The loop: search, read, search again with the same query, read, again. Cause: the loop condition reads a state field no node ever writes, so the exit test never passes; or the prompt never tells the model the answer is sufficient. Fix: a budget field the tool layer decrements, checked in the edge - structural, not promptual.
2. The hallucinated argument: a tool call with `customer_id=1234` that appears nowhere in the conversation. Cause: the model confabulated a value instead of calling the lookup tool first. Fix: schema validation that rejects unknown keys, plus an eval row for this case.
3. The ignored result: the agent calls a tool, gets "no results," and the final answer asserts the fact anyway. Cause: the compose step does not distinguish "tool returned empty" from "tool confirmed." Fix: the compose prompt receives an explicit no-results marker; the evaluator checks refusal on empty.
4. The wrong-but-plausible tool: `search_docs` called when the task needed `get_order_status`. Cause: overlapping tool descriptions. Fix: description rewrites that state exclusions ("does not return order status; use get_order_status"), verified by the intent evaluator.

## Presenting the diagnosis

Five minutes, three parts:

- Cause, named precisely: "The loop condition checks `findings_complete`, but no node writes that field - so the edge never routes to compose."
- Fix, structural first: "Write the field in the synthesis node; independently, cap turns in the edge so the failure cannot recur even if the prompt regresses."
- Prevention: "Add an eval row for this trajectory - the CI gate should have caught it; that is the real miss."

The prevention point is the differentiator. Anyone can spot the loop eventually; the candidate who says "and here is why the eval gate missed it" sounds like the person who prevents the next one.

## Drill

The repo gives you material: run `examples/retrieval_demo.py` or any agent demo with tracing mentally simulated, break one thing on purpose (comment out a state write), and diagnose from the printed steps. Twenty minutes of this per demo builds the reflex.

## What is next

[12 Take-home strategy](12-take-home-strategy.md) - the assignment that runs on your own time and gets judged harder than anything live.
