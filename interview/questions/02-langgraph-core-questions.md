# 02 LangGraph core - interview questions (concepts)

Status: beta | Teaches: [02 LangGraph core](../../02-langgraph-core/) | Part 1 of 2

1. What is state in LangGraph, and why does everything start there?
State is the typed schema every node reads from and writes to - the single shared object the graph passes between steps. It starts there because every other capability hangs off it: reducers define accumulation, checkpointers persist it, interrupts pause on it, and evals read trajectories from it. An answer that starts from nodes instead of state is the tell of a tutorial-level relationship with the library. Teaches: [01-graph-state-edges-nodes](../../02-langgraph-core/01-graph-state-edges-nodes.md).

2. What is a reducer, and what breaks without one?
A reducer defines how a node's output merges into state - `add_messages` appends instead of overwrites. Without one, each write replaces the field, so message history vanishes and parallel branches overwrite each other's results. The interview bar: name the exact failure, not just "it merges." Teaches: [01-graph-state-edges-nodes](../../02-langgraph-core/01-graph-state-edges-nodes.md).

3. Conditional edges vs putting the branch inside the node - when do you choose which?
The edge when the branch is a pure function of state that belongs in the graph's shape (visible, testable, drawn on the board); the node when the decision needs side effects or model calls mid-computation. The principle worth saying: keep nodes about work, edges about routing - the graph's readability is the asset. Teaches: [04-conditional-workflows](../../02-langgraph-core/04-conditional-workflows.md).

4. How does parallel execution interact with state?
Branches execute concurrently and their writes merge back through reducers - which is why parallel graphs need reducer-annotated fields or they clobber. Fan-out patterns pair with fan-in nodes that wait for all branches. The follow-up to expect: "what if branches return different schemas?" - then they write different fields, or an aggregator normalizes. Teaches: [03-parallel-workflows](../../02-langgraph-core/03-parallel-workflows.md).

5. What is the functional API, and when is it preferable to building graphs?
It decorates plain Python functions as graph steps - `@entrypoint` and `@task` - without explicit StateGraph wiring. Preferable when the flow is linear or the state shape is simple; the explicit graph earns its boilerplate when you need drawn structure, conditional routing, or checkpointing of complex shapes. The bar: name both and the crossover, not a preference. Teaches: [06-functional-api](../../02-langgraph-core/06-functional-api.md).

6. What does a checkpointer persist, and what does a thread id mean?
The checkpointer persists state at each super-step, keyed by thread id - the conversation's identity across invocations. Same thread id resumes the conversation; a new one starts fresh state. The production consequence: thread ids are your user-session mapping, and Postgres-backed checkpoints are what survive restarts. Teaches: [02-sequential-workflows](../../02-langgraph-core/02-sequential-workflows.md) and [03 Agents in practice](../../03-agents-in-practice/).

7. Why is an iterative loop in a graph not an infinite-loop risk? What bounds it?
The graph loops only while the conditional edge routes back - and the bound you actually rely on is structural: a budget field decremented per iteration, checked by the edge, or the recursion limit. "The model decides to stop" is the answer panels push back on; the deterministic cap is the interview answer. Teaches: [05-iterative-workflows](../../02-langgraph-core/05-iterative-workflows.md).

8. What is a super-step, and why does it matter for debugging?
It is one full pass of the graph - all nodes scheduled in that step execute and their writes merge. It matters because errors, logs, and traces are organized by step: "the failure is in step 3 after the tool branch" is how you speak about execution, and time-travel debugging rewinds to super-step boundaries. Teaches: [01-graph-state-edges-nodes](../../02-langgraph-core/01-graph-state-edges-nodes.md).

9. Send API - what problem does it solve that plain parallel edges do not?
Dynamic fan-out: parallel edges are fixed at graph build time, but Send dispatches to a node once per item in a runtime list - map over N documents when N is only known at execution. The map-reduce pattern over unbounded inputs is built on it. Teaches: [03-parallel-workflows](../../02-langgraph-core/03-parallel-workflows.md).

10. Command - what is it and which two jobs does it do?
Command is how a node redirects execution while returning state: it can route (goto) and carry data in one object, including back from an interrupt with resume. The bar: connect it to the human-in-the-loop story - approval flows are Command(resume=...) returning the human's decision into the node that called interrupt. Teaches: [04-conditional-workflows](../../02-langgraph-core/04-conditional-workflows.md).

11. Why compile a graph? What changes at compile time?
`compile()` turns the builder into a runnable object - validating structure, wiring the checkpointer and the runtime pieces. The useful detail: compilation is where you attach interrupt configuration and persistence, and an invalid edge or unresolvable node reference fails there, not at first invoke. Teaches: [01-graph-state-edges-nodes](../../02-langgraph-core/01-graph-state-edges-nodes.md).

12. A node raises mid-run with a checkpointer attached. What does the user see on retry?
State as of the last completed super-step: the invocation replays from the checkpoint, not from scratch. This is the recovery story for crashes - and the reason "checkpoint on Postgres" is the production answer for anything user-facing. Teaches: [02-sequential-workflows](../../02-langgraph-core/02-sequential-workflows.md).
