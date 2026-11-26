# Technical screens

Module: 10-interview-preparation
Chapter: 04-technical-screens
Status: beta
Last reviewed: 2026-11-26
Estimated time: 2 hours

## Learning objectives

- Know the three coding-screen formats for agent roles and drill for each
- Write graph code a reviewer can read: state, reducers, tools, interrupts
- Talk while coding so the screen produces signal instead of silence

## What the screen actually is

Sixty minutes, one interviewer, and a problem small enough to have a working answer. For agentic roles the problem is almost always one of three shapes. Screens exist to answer one question about you: when you write code, is the design visible in the code, or is it a pile of calls that happens to work?

## Shape 1: build a small graph

Typical prompt: "Build a workflow that takes a user question, classifies it, routes support questions to a tool-using agent, and routes anything else to a canned response." The expected artifact is a LangGraph graph, not an if-chain.

What the reviewer reads for, in order:

1. State design: a typed state with `add_messages` where messages accumulate, plus a `route` or `intent` field. If your state is a bare dict, you lose the room.
2. Reducers used correctly: appending messages via the reducer instead of overwriting.
3. Conditional edges named after the thing they decide: `route_by_intent`, not `decide`.
4. A tool node wired to the agent, and tool errors handled rather than assumed away.

Drill it: build it in under 25 minutes, talking, from [02 LangGraph core](../../02-langgraph-core/) and [03 Agents in practice](../../03-agents-in-practice/). The demos `conditional_edges_demo.py` and `agent_with_tools_demo.py` in [examples/](../../examples/) are the reference shape.

## Shape 2: tool design

Typical prompt: "Here is a function that queries orders. Wrap it as an agent tool and tell me what you would change about its interface." The expected moves:

- Write the schema (docstring or Pydantic) so an LLM can call it: short name, typed args, description that says what it returns and what it cannot do.
- Fix the interface: coarse return shape, no pagination, no tenant scoping, error cases hidden as empty results. Volunteer the fix before being asked - "this returns the whole order history; I would add a limit and a status filter to keep payloads bounded."
- State the security property: who is allowed to call it, and how it fails when the agent calls it with someone else's tenant.

## Shape 3: extend the code in front of you

Some screens hand you a small broken or incomplete agent and ask for a feature or a fix: add a checkpointer, add an approval step before a destructive tool, add a retry on one node. The reviewer is testing whether you can read unfamiliar graph code - trace the state schema, the edges, the reducers before you edit. Say the trace out loud: "State is messages plus pending order; the conditional edge sends to tools when the last message has tool calls; I will add the interrupt in the refund node before the call."

## Talking is half the screen

Silence converts a passing solution into a coin flip, because the reviewer only hears the design. Narrate at the block level, not the keystroke level: "State first, then the nodes, then the wiring, then the edge cases." When you are stuck, say the specific thing you are deciding: "I can put the routing logic in the node or in the conditional edge; I will put it in the edge so the node stays pure."

If you do not remember an exact API name, say the shape you want and move on: "the resume-call here - `Command(resume=...)` in the current API." Reviewers forgive vocabulary slips; they do not forgive silent flailing.

## The anti-patterns that fail screens

- Writing 40 lines before stating the state schema. Always state state first.
- No error path anywhere: tools that cannot fail, edges that cannot be missed, one happy line through the graph.
- Prompt-hacking in the screen: a design question answered with "I would tune the prompt" and nothing structural.
- Skipping the run: if the environment runs code, run it. A graph that has never executed is a hypothesis.

## What is next

[05 System design structure](05-system-design-structure.md) - the round that carries the most weight in agent-heavy loops.
