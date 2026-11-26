# 07 Multi-agent and A2A - interview scenarios

Status: beta | Teaches: [07 Multi-agent and A2A](../../07-multi-agent-and-a2a/) | Part 2 of 2

1. "Your LangGraph research agent must delegate code-execution tasks to the platform team's agent (a different framework). Design the integration."
A2A: the platform agent publishes its card (capabilities: sandboxed code execution; auth: service token), your agent discovers it and submits execution tasks through the protocol, results return as artifacts; long executions ride the task lifecycle with progress. Your side keeps a delegation node in the graph with a timeout and a fallback (refuse-and-explain if the remote is down). The alternative - shared library, shared queue - dies on the ownership boundary: their stack, their deploy cadence. Teaches: [05-cross-framework-interop](../../07-multi-agent-and-a2a/05-cross-framework-interop.md).

2. "Handoffs between your router agent and specialist agents drop the user's order number mid-transfer. Fix it."
The seam payload is implicit - history gets trimmed and the specialist re-derives. Define the handoff contract: a structured brief (user, intent, key entities, open actions) written by a summarize-and-delegate node, validated against a schema before transfer, asserted by a golden row that the specialist's first response references the order number. Contracts are checks, not conventions. Teaches: [02-handoffs](../../07-multi-agent-and-a2a/02-agent-handoffs.md).

3. "Security review: two agents over A2A, and the reviewer asks 'what stops agent B from asking agent A to delete data?'"
Authorization scoped to capabilities: agent A's server enforces per-caller permissions - B's token grants read-and-execute tasks, not destructive ones; destructive capability requires a human-in-the-loop step on A's side regardless of caller. Plus audit: every cross-agent task logged with caller identity. The sentence for the review: the card ADVERTISES capability; the server ENFORCES authorization - those are different layers. Teaches: [03-a2a-protocol](../../07-multi-agent-and-a2a/03-a2a-protocol.md) and [04-agent-cards](../../07-multi-agent-and-a2a/04-a2a-agent-cards.md).

4. "A vendor's A2A server is pinned to 0.2.x; your client is v1.0. Options?"
Three, in preference order: ask the vendor for the v1.0 timeline and pin an interop test to it; run a translation shim on your side (0.2.x wire on one face, v1.0 on the other) with contract tests on both faces; or drop to a plain HTTP integration outside A2A for that one peer. What not to do: downgrade your whole client to 0.2.x for one laggard - the debt compounds. Teaches: [03-a2a-protocol](../../07-multi-agent-and-a2a/03-a2a-protocol.md).

5. "Your three-agent system has no shared memory. Every agent re-fetches the order history. Restructure."
Introduce task-scoped shared state: a delegation orchestrator that holds the working context and passes slices with each task (or a task artifact store agents reference). The principle: fetch once at the seam owner, share deliberately - each agent carries what its role needs, not the whole world. The cost sentence: shared-nothing duplicates IO; share-everything leaks context; the contract is the balance. Teaches: [01-multi-agent-architectures](../../07-multi-agent-and-a2a/01-multi-agent-architectures.md).

6. "An A2A task sits in input-required for six hours. Whose bug is it, and what should have happened?"
The submitting agent must handle the lifecycle: input-required should surface promptly (to a user or an operator) with a timeout and a cancel path - six silent hours is a client-side handling gap. The server's duty was honest state; the client's duty was watching it. The fix: task-watchdog in the delegation node with escalation, and a golden row for the input-required path. Teaches: [03-a2a-protocol](../../07-multi-agent-and-a2a/03-a2a-protocol.md).

7. "Your org chart has five teams, each with an agent. The CTO wants them to 'collaborate.' Where do you start?"
Start with the work, not the topology: which cross-team tasks actually exist (support escalations to billing, research needing data analysis), then the boundary for each - shared MCP tools where the shared thing is data, A2A where the shared thing is delegation across ownership. Reject the five-agent free-mesh: collaboration without contracts is a debugging generator. The honest deliverable: two working seams and a pattern the other three can copy. Teaches: [01-multi-agent-architectures](../../07-multi-agent-and-a2a/01-multi-agent-architectures.md) and [05-cross-framework-interop](../../07-multi-agent-and-a2a/05-cross-framework-interop.md).

8. "Debugging a failed cross-agent task takes you three logs systems and a day. What instrumentation was missing?"
A propagated trace context across the seam (correlation ids on every A2A message, linked spans in both systems), and task-level audit records on both servers. With propagation, the distributed trace shows the handoff, the remote agent's steps, and the failure in one view; without it, every incident is archaeology. Retro-fit it into the protocol layer so nobody opts out. Teaches: [04-agent-cards](../../07-multi-agent-and-a2a/04-a2a-agent-cards.md) with [06 Evals tracing](../../06-evals-and-observability/05-langsmith-tracing.md).

9. "Product asks: 'can our agent call the vendor's agent directly from the user's browser session?' Architect's answer."
No - the browser is a hostile trust boundary: the user would hold service credentials, and the vendor's agent would receive untrusted direct traffic. Route through your backend: your agent authenticates to the vendor server with service credentials, submits tasks on the user's behalf, and owns the session's audit trail. Same protocol, different topology - the security boundary decides where the client lives. Teaches: [03-a2a-protocol](../../07-multi-agent-and-a2a/03-a2a-protocol.md).

10. "Design review: 'let's put an agent mesh in front of every internal API.' Your review comment."
Three sentences: a mesh in front of every API buys delegation semantics where a simple tool call would do; agents belong where judgment is required, not where a schema suffices; and every agent seam adds latency, auth surface, and failure modes - so each one needs a use case that pays for it. Concrete counter-proposal: MCP servers for the API access, agents only at the decision points. Teaches: [08-when-to-use-which](../../05-agentic-patterns/08-when-to-use-which.md) applied to the org.
