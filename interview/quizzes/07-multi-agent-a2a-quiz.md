# Quiz 07 - Multi-agent and A2A

Status: beta | Covers: [07 Multi-agent and A2A](../../07-multi-agent-and-a2a/) | 10 questions

1. A2A standardizes:
A) Agent-to-tool access
B) Agent-to-agent discovery and task exchange across runtimes
C) Model serving
D) Prompt formats

2. An agent card contains:
A) The agent's weights
B) Identity, capabilities, skills, endpoints, auth requirements
C) Its training data
D) Its prompt history

3. MCP and A2A in one sentence:
A) Competing standards - pick one
B) MCP: agent-to-tools; A2A: agent-to-agent
C) Both are transport protocols only
D) A2A replaces MCP in v1.0

4. A2A task lifecycle exists because:
A) Agents are stateless
B) Agent work is long-running, interactive, and may need more input mid-task
C) JSON-RPC requires it
D) HTTP is unreliable

5. Cross-framework interop is worth it when:
A) Always - standards are free
B) Agents owned by different teams on different stacks must cooperate
C) Never - one runtime always wins
D) The models differ

6. Multi-agent systems fail in ways single agents cannot, mostly:
A) At the seams - misrouting, context loss, duplicated work
B) In the model weights
C) Only in deployment
D) Never - they are strictly better

7. The A2A 0.2.x to v1.0 migration matters in practice because:
A) v1.0 is faster
B) 0.2.x and v1.0 peers cannot interoperate - versions are deployment facts
C) 0.2.x is deprecated by law
D) It renamed MCP

8. What stops agent B from asking agent A to delete data?
A) Politeness constraints in prompts
B) Per-caller authorization scoped to capabilities, enforced at A's server
C) The protocol forbids deletion
D) Nothing - trust is required

9. A task stuck in input-required for six hours is:
A) The server's bug, always
B) A client-side lifecycle handling gap - watchdogs and timeouts belong to the submitter
C) Expected behavior
D) An auth failure

10. Debugging a failed cross-agent task needs:
A) Luck
B) Propagated trace context and task-level audit records on both servers
C) Only the client logs
D) A shared database

## Answer key

1. B - the delegation boundary ([chapter 03](../../07-multi-agent-and-a2a/03-a2a-protocol.md)).
2. B - the discovery document ([chapter 04](../../07-multi-agent-and-a2a/04-a2a-agent-cards.md)).
3. B - two boundaries, one system ([chapter 05](../../07-multi-agent-and-a2a/05-cross-framework-interop.md)).
4. B - request-response cannot express it ([chapter 03](../../07-multi-agent-and-a2a/03-a2a-protocol.md)).
5. B - organizational boundaries, not fashion ([chapter 05](../../07-multi-agent-and-a2a/05-cross-framework-interop.md)).
6. A - seam engineering is the discipline ([chapter 01](../../07-multi-agent-and-a2a/01-multi-agent-architectures.md)).
7. B - version checks before integration ([chapter 03](../../07-multi-agent-and-a2a/03-a2a-protocol.md)).
8. B - cards advertise; servers enforce ([chapter 03](../../07-multi-agent-and-a2a/03-a2a-protocol.md)).
9. B - the submitter owns lifecycle handling ([chapter 03](../../07-multi-agent-and-a2a/03-a2a-protocol.md)).
10. B - correlation ids across the seam ([chapter 05](../../07-multi-agent-and-a2a/05-cross-framework-interop.md)).
