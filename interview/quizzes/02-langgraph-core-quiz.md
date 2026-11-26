# Quiz 02 - LangGraph core

Status: beta | Covers: [02 LangGraph core](../../02-langgraph-core/) | 10 questions

1. In LangGraph, everything starts from:
A) The nodes
B) The state schema
C) The prompt
D) The checkpointer

2. A reducer's job is:
A) Reducing token usage
B) Defining how a node's writes merge into state
C) Collapsing parallel branches into one
D) Compressing the message history

3. Without a reducer on a field written by two parallel branches:
A) The graph fails to compile
B) The second write overwrites the first
C) Both writes merge automatically
D) The field becomes read-only

4. Conditional edges are best used when:
A) The branch is a pure function of state
B) The branch needs a model call mid-node
C) You want to hide routing logic
D) Nodes are unavailable

5. The Send API exists for:
A) Sending messages to external systems
B) Dynamic fan-out - one node dispatched per runtime list item
C) Streaming tokens
D) Resuming interrupts

6. Command() can:
A) Only route to another node
B) Route and carry data, including a resume value from interrupt()
C) Only resume an interrupt
D) Modify state schemas at runtime

7. A checkpointer keyed by thread id gives you:
A) Multi-tenant isolation by default
B) Conversation persistence and replay across invocations
C) Automatic state summarization
D) Distributed transactions

8. After a crash mid-run with a checkpointer attached, re-invocation:
A) Restarts the graph from scratch
B) Replays from the last completed super-step
C) Fails - the thread is poisoned
D) Restores to the beginning of the current node

9. The reliable bound on an iterative loop is:
A) The model deciding to stop
B) Prompt instructions to be concise
C) A budget field checked by the edge, or the recursion limit
D) User patience

10. compile() is where:
A) The graph is optimized into machine code
B) Structure is validated and the checkpointer and runtime pieces attach
C) Prompts are frozen
D) Nodes execute once as a test

## Answer key

1. B - state is the spine; every capability hangs off it ([chapter 01](../../02-langgraph-core/01-graph-state-edges-nodes.md)).
2. B - append, merge, or overwrite semantics per field ([chapter 01](../../02-langgraph-core/01-graph-state-edges-nodes.md)).
3. B - replace-by-default is the clobbering bug ([chapter 03](../../02-langgraph-core/03-parallel-workflows.md)).
4. A - keep nodes about work, edges about routing ([chapter 04](../../02-langgraph-core/04-conditional-workflows.md)).
5. B - map over inputs whose count is known only at runtime ([chapter 03](../../02-langgraph-core/03-parallel-workflows.md)).
6. B - routing and data in one object; the resume shape powers HITL ([chapter 04](../../02-langgraph-core/04-conditional-workflows.md)).
7. B - thread id is the conversation's identity ([chapter 02](../../02-langgraph-core/02-sequential-workflows.md)).
8. B - replay from checkpoint; steps 1..N-1 do not re-bill ([chapter 02](../../02-langgraph-core/02-sequential-workflows.md)).
9. C - deterministic caps, never model judgment ([chapter 05](../../02-langgraph-core/05-iterative-workflows.md)).
10. B - invalid structure fails there, not at first invoke ([chapter 01](../../02-langgraph-core/01-graph-state-edges-nodes.md)).
