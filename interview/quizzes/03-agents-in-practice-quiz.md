# Quiz 03 - Agents in practice

Status: beta | Covers: [03 Agents in practice](../../03-agents-in-practice/) | 10 questions

1. The message-state pattern's default agent shape is:
A) One node that does everything
B) Agent node + tools node + conditional edge on tool calls
C) A supervisor with three specialists
D) A linear pipeline

2. PostgresSaver over SqliteSaver in production because:
A) It is faster per write
B) Concurrency, durability, and operations survive real traffic
C) LangGraph requires it
D) SQLite cannot store messages

3. The difference between checkpointer memory and Store memory:
A) None - two names for one thing
B) Checkpointer: within-conversation state; Store: cross-conversation facts
C) Checkpointer: tools; Store: prompts
D) Store: messages; checkpointer: users

4. ToolNode's job is:
A) Deciding which tool the model should call
B) Executing the tool calls found in the last AIMessage and returning ToolMessages
C) Caching tool results
D) Validating tool schemas at compile time

5. On resume, interrupt() returns:
A) The original payload again
B) The human's value passed via Command(resume=...)
C) Nothing - the node restarts
D) An error if the graph recompiled

6. Review-and-edit HITL means:
A) The human approves a pending action
B) The human edits agent output; the edited version is used downstream
C) The human rewrites the prompt
D) The model self-corrects after feedback

7. Token streaming primarily improves:
A) Total generation time
B) Perceived latency - first token arrives early
C) Accuracy
D) Cost

8. Thread ids and user identity relate as:
A) Same thing
B) One user, many threads; a thread belongs to one user
C) One thread, many users
D) Unrelated - threads are per request only

9. A node with side effects that runs twice after a crash indicates:
A) A framework bug
B) Non-idempotent side effects on replay - the fix is idempotency keys
C) The checkpointer failed
D) The tool raised mid-call

10. Testing graphs without API keys works by:
A) Skipping tests in CI
B) Stub nodes and scripted model layers exercising routing and state
C) Using a free provider
D) Disabling the graph

## Answer key

1. B - the loop is the skeleton ([chapter 01](../../03-agents-in-practice/01-conversational-agents.md)).
2. B - the choice is durability and concurrency, not speed ([chapter 02](../../03-agents-in-practice/02-persistence-and-memory.md)).
3. B - "remembers this chat" vs "remembers the user" ([chapter 02](../../03-agents-in-practice/02-persistence-and-memory.md)).
4. B - dispatch, execute, return as results the model sees ([chapter 03](../../03-agents-in-practice/03-tool-integration.md)).
5. B - the resume value injects into the interrupted node ([chapter 04](../../03-agents-in-practice/04-human-in-the-loop.md)).
6. B - the human controls content, not just the decision ([chapter 04](../../03-agents-in-practice/04-human-in-the-loop.md)).
7. B - streaming hides latency; it does not remove it ([chapter 05](../../03-agents-in-practice/05-streaming-and-ux.md)).
8. B - session mix-ups are the classic bug ([chapter 02](../../03-agents-in-practice/02-persistence-and-memory.md)).
9. B - replay re-executes from the last super-step ([chapter 02](../../03-agents-in-practice/02-persistence-and-memory.md)).
10. B - the repo's keyless demos are this discipline ([chapter 01](../../03-agents-in-practice/01-conversational-agents.md)).
