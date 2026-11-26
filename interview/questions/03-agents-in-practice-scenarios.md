# 03 Agents in practice - interview scenarios

Status: beta | Teaches: [03 Agents in practice](../../03-agents-in-practice/) | Part 2 of 2

1. "Users report the agent forgets what they said three messages ago. Where is the bug?"
Walk the memory ladder: checkpointer attached at all (no persistence - each invoke is fresh); correct thread id passed per user-session (right checkpointer, wrong key - sessions collide or split); and history actually in state (a node overwriting messages instead of the reducer appending). The diagnosis order matters: infrastructure, then keying, then state mechanics. Teaches: [02-persistence-and-memory](../../03-agents-in-practice/02-persistence-and-memory.md).

2. "Support agents handle refunds. Legal says every refund needs a named human approver. Wire it in."
`interrupt()` before the refund tool call, payload carrying the structured proposal (order, amount, reason); the approval UI records who approved; `Command(resume=...)` carries the decision plus approver identity into the node, and the tool executes only on approval with the approver written into the audit record. The three extras that make the answer senior: idempotent refund (no double-execution on replay), the rejection path routes to an apology node, and the audit trail lives in the checkpointer by construction. Teaches: [04-human-in-the-loop](../../03-agents-in-practice/04-human-in-the-loop.md).

3. "The chat UI shows nothing for 8 seconds, then the whole answer. Fix the experience."
Event and token streaming: stream tokens for the first-token latency, and graph events for the tool phases ("checking your order..."). The structural part of the answer: stream from the model node during generation and surface tool-node events as status, so the user sees progress while the loop works. If the 8 seconds are one long tool call, that is the tool's problem - bound it. Teaches: [05-streaming-and-ux](../../03-agents-in-practice/05-streaming-and-ux.md).

4. "Your agent must remember that this customer prefers email summaries and has two open orders - across sessions and weeks."
That is Store memory, not checkpoints: facts written under a user-scoped namespace, retrieved at session start into the system prompt or as tool access. Say the write discipline: facts the model can cite and update (a preference changes), a TTL or recency policy so stale facts decay, and a view of what retrieval returns - the agent should know what it remembers and be able to re-check. Teaches: [02-persistence-and-memory](../../03-agents-in-practice/02-persistence-and-memory.md).

5. "An engineer on your team wants the model to pick which of 40 tools to use. You say no. Why, and what do you propose?"
Tool bloat degrades selection accuracy - wrong-tool rates rise with schema count - and bloats every call's tokens. Propose: group and scope - dynamic loading so each request binds the 5-10 relevant tools (by intent, tenant, or MCP server), or compose mega-tools (one `order_actions` tool with an action enum). The principle: the tool list is an interface you design, not a pile you accumulate. Teaches: [03-tool-integration](../../03-agents-in-practice/03-tool-integration.md).

6. "A node with side effects runs twice after a crash. Why, and what is the fix?"
Replay from checkpoint re-executes from the last completed super-step - and an interrupted side-effecting step can run twice on continuation. The fix is idempotency: the side effect carries a key (request id, transaction token) the downstream system deduplicates, and the node is written so re-execution converges. The bar: own the discipline - "the framework gives you replay; it does not give you idempotent side effects." Teaches: [02-persistence-and-memory](../../03-agents-in-practice/02-persistence-and-memory.md).

7. "QA cannot reproduce a routing bug that customers hit weekly. What do you hand them?"
The trajectory, not the code: a run with tracing on, the step list, the exact input, and the state at the misroute - the [trace-debugging method](../../10-interview-preparation/11-trace-debugging-round.md). Plus the regression net: the offending input as an eval row with the expected route, so the fix and every future change is checked against it. Teaches: [06-langgraph-studio](../../03-agents-in-practice/06-langgraph-studio.md).

8. "Product wants the agent to feel present: typing indicators, intermediate status, partial answers. What is the plumbing?"
Event streaming to a websocket: node-start events drive status messages, tool events drive action labels ("checking order..."), and token deltas from the generate node render incrementally. Frontend holds a buffer per message and commits on message-complete. The trap to name: streaming does not make the graph faster - it makes the wait visible and shorter-feeling; the latency budget itself is a separate fix. Teaches: [05-streaming-and-ux](../../03-agents-in-practice/05-streaming-and-ux.md).

9. "You ship to 200 users. Checkpoint table grows unboundedly. Policy?"
Retention with purpose: per-thread TTL sized to product reality (support conversations expire in 30 days; research projects live longer), archival of old threads rather than hard deletion if audits matter, and vacuum/monitoring on the store. The interview bar: retention is a product decision with a number, not a DBA chore - say whose call it is. Teaches: [02-persistence-and-memory](../../03-agents-in-practice/02-persistence-and-memory.md).

10. "The demo works in Studio and fails in the deployed app. Rank your suspects."
Environment first: keys and config the deployed runtime lacks; then serialization - state fields Studio tolerates that the real checkpointer rejects; then concurrency - local sequential, deployed parallel, exposing a reducer-less field; then the graph version mismatch - code deployed behind the API is not the code you ran. Each suspect has a two-minute check; run them in order and the failure usually surfaces by suspect three. Teaches: [06-langgraph-studio](../../03-agents-in-practice/06-langgraph-studio.md) and [08 Production](../../08-production/).
