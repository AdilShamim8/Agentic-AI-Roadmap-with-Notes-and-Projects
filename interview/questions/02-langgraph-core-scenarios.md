# 02 LangGraph core - interview scenarios

Status: beta | Teaches: [02 LangGraph core](../../02-langgraph-core/) | Part 2 of 2

1. "Whiteboard a workflow: classify a support ticket, then draft a reply only for billing tickets, and archive everything else."
Draw state first: `messages` or `ticket_text`, plus `intent` and `draft`. Nodes: `classify` writes intent; `draft` produces the reply; `archive` records the outcome. Conditional edge `route_by_intent` reads intent - billing to draft, else to archive. Then say the checkable property out loud: single-writer fields, one routing decision in the graph's shape, testable with a stub classifier. Teaches: [04-conditional-workflows](../../02-langgraph-core/04-conditional-workflows.md).

2. "Your agent loops between two nodes and never exits. Diagnose it in front of me."
The exit condition reads a field nobody writes - trace which node should set `done` or `findings_complete`, and either write it or move the condition onto a field that changes. Then install the structural guard: budget field decremented in the node, checked in the edge, so no prompt regression can reintroduce the loop. Close with the eval row - "this input terminates within N steps" - and the diagnosis is complete at all three levels: cause, fix, prevention. Teaches: [05-iterative-workflows](../../02-langgraph-core/05-iterative-workflows.md).

3. "Two parallel branches both write the same state field and you are losing one result. Why, and what are the two fixes?"
No reducer - the writes overwrite in merge order. Fix one: annotate the field with a reducer (append, or merge dicts) so both land. Fix two: give each branch its own field and let the fan-in node read both - clearer when the branches carry different semantics. The trap answer: "add a lock" - the merge is already serialized; the field is simply replace-by-default. Teaches: [03-parallel-workflows](../../02-langgraph-core/03-parallel-workflows.md).

4. "Summarize 1,000 customer reviews with a graph. Design it."
Send-based fan-out: one node emits the batch, Send dispatches a summarize task per review (or per chunk of 50), results merge through a reducer into a list, and a final node synthesizes. Name the failure modes: unbounded fan-out needs a chunk cap; partial failures need per-item error state rather than a dead branch; and the reducer must preserve order or the synthesis sees shuffled results. Teaches: [03-parallel-workflows](../../02-langgraph-core/03-parallel-workflows.md).

5. "You need the agent to pause before sending an email and let an operator edit the draft. Which API and how?"
`interrupt()` in the node before the send: it returns the draft as payload to the caller, the operator edits, and `Command(resume=edited_draft)` continues the node with the edited text, which the send node then uses. The bar: say that resume injects the human value into the interrupted node's execution - the edit replaces the model draft, not a patch after the fact. Teaches: [04-conditional-workflows](../../02-langgraph-core/04-conditional-workflows.md) and [04 Human-in-the-loop](../../03-agents-in-practice/04-human-in-the-loop.md).

6. "The graph runs fine locally and explodes in production with the same input. Where do you look?"
The stateless-looking suspects: checkpoint backend availability (Postgres unreachable - attach failures surface on invoke), thread-id collisions (two users resuming one conversation), and serialization of state fields (an object the checkpointer cannot serialize, fine in-memory, fatal persisted). Order the diagnosis from infrastructure inward, and say the repro tool: same thread id, same input, against the real backend. Teaches: [02-sequential-workflows](../../02-langgraph-core/02-sequential-workflows.md).

7. "Your teammate wants 15 nodes in one graph. Argue for or against."
Against, as drawn: 15 nodes is usually three concerns in one graph. Factor into subgraphs with their own state boundaries - the composite stays legible, the subgraphs test independently, and each gets its own checkpoint semantics. The counter-argument worth conceding: subgraphs add wiring ceremony, so a genuinely linear 15-step pipeline with one state schema is fine as one graph. The bar is naming the factor-by-concern principle, not a node count. Teaches: [01-graph-state-edges-nodes](../../02-langgraph-core/01-graph-state-edges-nodes.md).

8. "A run died after step 4 of 9. The user refreshes. What happens next, and what did you have to build for it?"
With a checkpointer: the graph re-invokes on the same thread and replays from step 4's checkpoint - the user's conversation continues, steps 1-3 do not re-execute or re-bill. What you built: thread-id mapping to sessions, a durable checkpointer backend, and idempotent nodes (side-effecting tools safe to retry). The last clause is the differentiator - replay safety is a node-design discipline, not a framework gift. Teaches: [02-sequential-workflows](../../02-langgraph-core/02-sequential-workflows.md).

9. "When would you reach for the functional API on a real project?"
A linear, state-simple pipeline - ingest, transform, summarize - where StateGraph ceremony buys nothing; the decorated functions read as plain code and the entrypoint/task split is enough structure. The moment routing, fan-out, or complex checkpointing appears, switch - and say the switching cost is low because node logic ports as functions. Teaches: [06-functional-api](../../02-langgraph-core/06-functional-api.md).

10. "Your eval harness reports the graph took 12 steps on a 2-step task. What is that telling you?"
Probably a routing or termination bug, not an eval bug: a conditional edge cycling (tool node back to agent because a tool call was misparsed), or a retry loop from a tool error the model keeps re-attempting. Read the trajectory: the step list names the cycle in seconds. The fix lands in the edge or the tool's error semantics; the number in the eval keeps it fixed. Teaches: [05-iterative-workflows](../../02-langgraph-core/05-iterative-workflows.md) with [06 Evals](../../06-evals-and-observability/).
