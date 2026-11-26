# 05 Agentic patterns - interview questions (concepts)

Status: beta | Teaches: [05 Agentic patterns](../../05-agentic-patterns/) | Part 1 of 2

1. ReAct in one sentence, and what its loop actually buys?
Reason-then-act: the model emits a tool call (act), observes the result, and repeats until it can answer (reason). It buys adaptivity - each step informed by real observations instead of a prewritten plan. The cost sentence to attach: every step pays latency and tokens, and termination needs a structural cap. Teaches: [01-react-pattern](../../05-agentic-patterns/01-react-pattern.md).

2. Plan-and-execute: what is the split, and when does it beat ReAct?
A planner commits a step list once; an executor runs the steps (often in parallel); a replanner handles surprises. It beats ReAct when the task decomposes cleanly and steps are independent - batch research, checklists - because planning once is cheaper than re-deciding per step, and parallel execution compounds the win. It loses when steps depend on each other's results. Teaches: [02-plan-and-execute](../../05-agentic-patterns/02-plan-and-execute.md).

3. Reflexion - what is reflected upon, and what is the artifact?
The agent critiques its own failed attempt and writes the critique into memory as structured lessons, which condition the retry. The artifact is persistent reflection state - not just "try again." The honest caveat: it multiplies cost per retry and works best when failures are diagnosable, so it is a pattern for hard tasks, not a default. Teaches: [03-reflexion](../../05-agentic-patterns/03-reflexion.md).

4. What does a supervisor do in a multi-agent system, and what is its alternative?
The supervisor is a router node that reads state and assigns work to specialist sub-agents, iterating until done. The alternative is peer handoff (swarm): agents pass control directly to each other based on their own judgment. Supervisor = legible control flow and a natural place for policy; swarm = fewer hops and less central reasoning, harder to audit. Teaches: [04-supervisor](../../05-agentic-patterns/04-supervisor.md) and [06-swarm](../../05-agentic-patterns/06-swarm.md).

5. What problem does a hierarchical organization of agents solve?
Scaling supervision: a top supervisor routes to team supervisors, each owning a domain - so any single router's context and tool list stays small. It is the org-chart pattern applied to control flow: delegation with clear boundaries, at the cost of more total steps. Teaches: [05-hierarchical](../../05-agentic-patterns/05-hierarchical.md).

6. Map-reduce over an agent task: give the shape and the failure mode.
Fan out one node's work to N parallel workers (Send per item), merge results through a reducer, synthesize once. The failure mode is heterogeneous completion: one slow worker stalls the join, and partial failures must be represented in state rather than dropped. The production answer: per-item timeout and error capture so the reduce sees "completed 47, failed 3," not a dead branch. Teaches: [07-map-reduce](../../05-agentic-patterns/07-map-reduce.md).

7. When is multi-agent the WRONG answer, and how do you say that in an interview?
When one agent with the right tools covers the task: multi-agent adds coordination cost, handoff failure modes, and debug surface. The bar answer: "I start single-agent and split when a measured constraint appears - context overflow, divergent tool scopes, or independent parallelizable work - and I can name the constraint." That sentence signals judgment better than any architecture diagram. Teaches: [08-when-to-use-which](../../05-agentic-patterns/08-when-to-use-which.md).

8. What actually gets passed between agents in a handoff?
The conversation state the next agent needs: trimmed history or a task brief, plus shared scratchpad fields - not the full raw context, and not nothing. The design work is the contract: what the receiving agent can assume, and what it must re-derive. The failure mode to name: context amnesia at the seam - the receiver re-asks what the sender already resolved. Teaches: [06-swarm](../../05-agentic-patterns/06-swarm.md).

9. Where does human-in-the-loop sit in a supervisor topology?
At the supervisor's decision points - approve, redirect, or veto before specialists act - and at the specialists' destructive tools. The design rule: HITL attaches to routing decisions and gated actions, not to observation, or the human becomes the bottleneck the multi-agent spend was avoiding. Teaches: [04-supervisor](../../05-agentic-patterns/04-supervisor.md).

10. What distinguishes a pattern's implementation cost from its ongoing cost?
Implementation cost is the wiring - the graph structure, the handoff contracts. Ongoing cost is the runtime tax - extra model calls, tokens per coordination step, latency per hop, and debugging surface. Reflexion is cheap to wire, expensive to run; supervisor is moderate wiring, moderate run; hierarchical is expensive both. Choosing on wiring cost alone is the junior mistake - name both. Teaches: [08-when-to-use-which](../../05-agentic-patterns/08-when-to-use-which.md).

11. How does evaluation differ for a multi-agent system vs a single agent?
You evaluate the seams as well as the endpoints: task-level outcomes (same golden set), plus trajectory metrics per agent - handoff accuracy (did work land on the right specialist), and seam efficiency (steps and tokens spent on coordination vs work). A multi-agent system can pass endpoint evals while burning 3x tokens in coordination, and only the trajectory view shows it. Teaches: [08-when-to-use-which](../../05-agentic-patterns/08-when-to-use-which.md) with [06 Evals](../../06-evals-and-observability/).

12. "Emergent behavior" in a swarm - what is the engineering stance?
Skepticism with instrumentation: the behavior is real (routing decisions compound) but not designed, so the stance is measure first - trajectory traces, handoff graphs - and add structure (supervisor checkpoints, tool scopes) where the emergent path misbehaves. Betting the product on unspecified emergence is the failure story interviewers are fishing for. Teaches: [06-swarm](../../05-agentic-patterns/06-swarm.md).
