# 07 Multi-agent and A2A - interview questions (concepts)

Status: beta | Teaches: [07 Multi-agent and A2A](../../07-multi-agent-and-a2a/) | Part 1 of 2

1. What is A2A, and what does it standardize?
The Agent2Agent protocol (v1.0 wire format): a standard for agents in different runtimes to discover each other (agent cards), exchange tasks, and negotiate execution - over JSON-RPC-shaped messaging. It standardizes the agent-to-agent boundary the way MCP standardizes the agent-to-tool boundary. Teaches: [03-a2a-protocol](../../07-multi-agent-and-a2a/03-a2a-protocol.md).

2. What is an agent card?
The discovery document an A2A server publishes: identity, capabilities, skills, endpoints, auth requirements. It is what a remote agent reads to decide whether and how to delegate work - the protocol's answer to "what can you do, and how do I address you." Teaches: [04-agent-cards](../../07-multi-agent-and-a2a/04-a2a-agent-cards.md).

3. MCP vs A2A in one sentence each - and why a system needs both?
MCP: an agent's standardized access to tools and data. A2A: standardized collaboration between agents across runtimes. A system needs both because the boundaries differ - a LangGraph agent with MCP tools delegating to a different framework's agent is both boundaries at once. Teaches: [05-cross-framework-interop](../../07-multi-agent-and-a2a/05-cross-framework-interop.md).

4. What is a handoff, and what makes a clean one?
Transferring control of a task to another agent with its needed context. Clean means the payload is explicit (task brief, resolved facts, artifacts), the receiving agent's role is known from its card, and the user experience is continuous - the seam is engineering, not user-visible. Teaches: [02-handoffs](../../07-multi-agent-and-a2a/02-agent-handoffs.md).

5. What does "task" mean in A2A, and why is the lifecycle not just request-response?
A task is the unit of delegated work with its own state machine - submitted, working, input-required, completed, failed - because agent work is long-running and interactive: the remote agent may need more input mid-task, stream progress, and outlive the original request. Request-response cannot express any of that. Teaches: [03-a2a-protocol](../../07-multi-agent-and-a2a/03-a2a-protocol.md).

6. When is cross-framework interop actually worth the protocol overhead?
When agents owned by different teams on different stacks must cooperate - your LangGraph order agent and the vendor's support agent - and a shared protocol beats N bespoke integrations. Not worth it inside one runtime you control: native function calls and shared state are simpler and faster. The bar: A2A for organizational boundaries, not architectural fashion. Teaches: [05-cross-framework-interop](../../07-multi-agent-and-a2a/05-cross-framework-interop.md).

7. How do multi-agent architectures fail that single agents cannot?
At the seams: misrouting (work lands on the wrong agent), context loss at handoff, duplicated work when ownership is ambiguous, and blame diffusion - no single agent holds the full picture, so end-to-end debugging is harder. The design response: explicit contracts, trajectory tracing across seams, and a supervisor or owner-of-record for the task. Teaches: [01-multi-agent-architectures](../../07-multi-agent-and-a2a/01-multi-agent-architectures.md).

8. What security questions does an A2A deployment raise that single-agent systems do not?
Caller authentication between agents, authorization per capability (what may a remote agent ask this one to do), input validation across trust boundaries (their prompt is your untrusted input), and auditability of cross-agent delegation - who asked whom to do what, when. Teaches: [03-a2a-protocol](../../07-multi-agent-and-a2a/03-a2a-protocol.md) and [04-agent-cards](../../07-multi-agent-and-a2a/04-a2a-agent-cards.md).

9. How does evaluation extend to an A2A network?
Cross-seam trajectory: the distributed trace of a task across both agents - handoff accuracy (right agent), contract conformance (payloads as declared), and end-to-end task outcome. Each agent keeps its own golden set; the network adds the integration set that exercises the protocol path. Teaches: [05-cross-framework-interop](../../07-multi-agent-and-a2a/05-cross-framework-interop.md) with [06 Evals](../../06-evals-and-observability/).

10. What is the interop alternative when teams control both sides?
Shared infrastructure: one runtime, one state store, native calls - cheaper and more debuggable than any protocol. The protocol earns its place at the trust or ownership boundary; inside one team's system it is usually ceremony. Teaches: [01-multi-agent-architectures](../../07-multi-agent-and-a2a/01-multi-agent-architectures.md).

11. Give the one-line deployment story for an A2A participant.
The agent serves its card and task endpoints over HTTP with auth; a client (another agent or an orchestrator) discovers the card, submits a task, and drives it to completion through the lifecycle - no shared process, no shared state, the contract is the protocol. Teaches: [03-a2a-protocol](../../07-multi-agent-and-a2a/03-a2a-protocol.md).

12. What did the A2A 0.2.x to v1.0 migration change in practice?
The wire format stabilized (v1.0.0): consistent message and task structures, the agent-card shape settled, and the older experimental transport idioms deprecated. In practice: clients and servers pinned to 0.2.x cannot interoperate with v1.0 peers, so versions are a deployment fact to check - this repo's own solutions carry version notes on exactly this. Teaches: [03-a2a-protocol](../../07-multi-agent-and-a2a/03-a2a-protocol.md).
