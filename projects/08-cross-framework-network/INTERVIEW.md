# Interview guide - Project 08: Cross-framework network

Status: beta | For: presenting this project in interviews | Related: [project README](README.md), [project stories](../../10-interview-preparation/15-project-stories.md)

## The pitch

"A2A between two agents that do not share a runtime: a LangGraph agent and an agent from another stack, discovering each other's capabilities from agent cards and delegating tasks through the protocol's lifecycle. The seam is the design: task briefs, contract conformance, and what happens when the remote side is slow or wrong."

## The whiteboard script

1. Two boxes, different runtimes, the A2A line drawn between them.
2. The agent card on the remote side - capabilities, endpoints, auth requirements.
3. The task lifecycle - submitted, working, input-required, completed - and your client's handling of each state, especially input-required.
4. The delegation node in your graph: submit, watch with a timeout, consume the artifact, handle failure.
5. The distributed trace - correlation ids propagated across the seam.

The line that earns the nod: "The contract is the protocol - no shared process, no shared state."

## The numbers you quote

- Task timeout and retry policy constants.
- Contract-test coverage of the payloads crossing the seam.

## The follow-ups

- "Why not just a REST call?" At one integration, REST is simpler - A2A earns its place at the ownership boundary: different teams, different deploy cadence, discovery, and a task lifecycle instead of request-response. Say the crossover.
- "What if the remote agent is malicious?" Per-caller authorization at the server; your delegation sends only what the task needs; audit records on both sides; the injected-instruction case is bounded by what you granted.
- "Version skew?" The 0.2.x-to-v1.0 lesson: versions are deployment facts - contract tests pin the wire format, and a shim bridges a laggard peer.
- "How do you debug a cross-agent failure?" The propagated trace: one view, both runtimes, the handoff and the remote steps in sequence. Without it, every incident is archaeology.

## The red flags

- Selling the mesh instead of the seam - one well-defined delegation beats five vague ones.
- No timeout/lifecycle story for remote work.
- "The agents collaborate" without naming what crosses the boundary and who owns it.

## What this project proves

Protocol literacy and seam engineering - the interop judgment that platform and multi-team environments screen for.
