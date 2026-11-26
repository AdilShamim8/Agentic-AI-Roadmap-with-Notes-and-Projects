# 03 Agents in practice - interview questions (concepts)

Status: beta | Teaches: [03 Agents in practice](../../03-agents-in-practice/) | Part 1 of 2

1. What is the message-state pattern, and why is it the default agent shape?
A graph whose state is essentially a message list accumulated with `add_messages`: the agent node appends model output, the tools node appends tool results, the conditional edge routes on whether the last message has tool calls. It is the default because the loop - model, tools, model, until no calls - is the ReAct skeleton, and message accumulation is exactly what the reducer gives you. Teaches: [01-conversational-agents](../../03-agents-in-practice/01-conversational-agents.md).

2. MemorySaver, SqliteSaver, PostgresSaver - how do you choose?
By what must survive: MemorySaver dies with the process (tests, demos); SqliteSaver is a single-file, single-writer convenience (local, prototypes); PostgresSaver is concurrent, backed up, and restartable (production). The bar: say the concurrency and durability line, and that swapping is a constructor change because the interface is shared. Teaches: [02-persistence-and-memory](../../03-agents-in-practice/02-persistence-and-memory.md).

3. Checkpointer memory vs Store memory - what is the difference?
The checkpointer holds within-conversation state - each thread's messages and fields, resumed by thread id. The Store holds cross-conversation memory - facts about the user or the world, keyed by namespace, retrieved into any thread. Confusing them is the most common interview wobble in this module: "remembers this chat" vs "remembers the user." Teaches: [02-persistence-and-memory](../../03-agents-in-practice/02-persistence-and-memory.md).

4. What does ToolNode actually do?
Executes the tool calls found in the last AIMessage: binds arguments, runs the functions, returns ToolMessages with the results. It is the standard middle of the agent loop, and knowing it exists - rather than hand-rolling the call dispatch - signals real usage. The follow-up to expect: how errors are returned (as tool result messages the model sees, not exceptions the graph dies on). Teaches: [03-tool-integration](../../03-agents-in-practice/03-tool-integration.md).

5. When do you load tools dynamically instead of binding them all at compile time?
When the tool set is per-request - tenant-specific, permission-scoped, or discovered from a registry/MCP server at runtime. The cost of binding everything: schema bloat in every call and a wider surface for wrong-tool selection, so dynamic loading is a precision AND a security tool. Teaches: [03-tool-integration](../../03-agents-in-practice/03-tool-integration.md).

6. What does interrupt() return, and where does the value come from?
It returns the payload you pass it when the graph pauses - and on resume, it returns the human's value injected via Command(resume=...). The mental model worth saying: the node call suspends mid-execution and re-executes with the resume value on continuation, so side effects before the interrupt must be idempotent. Teaches: [04-human-in-the-loop](../../03-agents-in-practice/04-human-in-the-loop.md).

7. Approval vs review-and-edit - give a real example of each.
Approval: the agent proposes "refund $50 to order ABC," the human clicks approve, resume carries yes and the refund node executes. Review-and-edit: the agent drafts the customer email, the human edits the text, resume carries the edited draft and the send node uses it verbatim. The distinction is what the human controls - the decision to act, or the content of the action. Teaches: [04-human-in-the-loop](../../03-agents-in-practice/04-human-in-the-loop.md).

8. Token streaming vs event streaming - what is the difference and when does each matter?
Token streaming yields generation incrementally - it matters for perceived latency in chat UX (first token fast). Event streaming yields graph events - node starts, tool calls - which powers progress UI ("checking your order...") and observability. The bar: name what each is FOR; the best answer notes they compose - tokens inside events. Teaches: [05-streaming-and-ux](../../03-agents-in-practice/05-streaming-and-ux.md).

9. What is LangGraph Studio for, and what does it see that a terminal cannot?
Visual debugging: the graph drawn, state at each super-step, step-through execution, time travel to earlier checkpoints. The terminal shows prints; Studio shows the run's actual shape - which node fired, what the edge decided - which is where routing bugs become visible in seconds. Teaches: [06-langgraph-studio](../../03-agents-in-practice/06-langgraph-studio.md).

10. A tool raises an exception. What are your three options in the graph, and which is the default?
Return the error as the tool's result message (default - the model adapts), catch and route to a failure node (for known-unrecoverable cases), or let it propagate (rarely right in production). The eval hook: a trajectory row asserting the failed call does not retry more than once. Teaches: [03-tool-integration](../../03-agents-in-practice/03-tool-integration.md).

11. How do you test an agent graph without API keys?
Two layers: run the graph with stub nodes - deterministic functions replacing model calls - to test routing and state mechanics; and run the real graph against a recorded or scripted model layer for loop shape. This repo's demos are keyless by design (scripted fallbacks) for exactly this discipline; the eval suite runs in CI with no secrets. Teaches: [01-conversational-agents](../../03-agents-in-practice/01-conversational-agents.md) and the repo's keyless examples.

12. Thread ids and user identity - how do they relate, and what is the classic bug?
Thread id is the conversation key, identity is the user - one user has many threads; one thread belongs to one user. The classic bug: thread id reused across users (session mix-up, data bleed between customers). The fix is server-side: thread ids minted per conversation, validated against the session, never taken from client input. Teaches: [02-persistence-and-memory](../../03-agents-in-practice/02-persistence-and-memory.md).
