# 05 Agentic patterns - interview scenarios

Status: beta | Teaches: [05 Agentic patterns](../../05-agentic-patterns/) | Part 2 of 2

1. "Product wants a research assistant: it gets a question, reads 20 sources, writes a cited report. Pick your pattern and defend it."
Plan-and-execute with map-reduce execution: the planner decomposes into sub-questions, workers search and read in parallel (Send per sub-question), the reduce merges findings, one synthesis node writes the report with citations. Defended against ReAct (serial re-deciding wastes latency across 20 sources) and against a single agent (context overflow at 20 documents). Name the guard: per-worker budget and a findings reducer that captures failures per item. Teaches: [02-plan-and-execute](../../05-agentic-patterns/02-plan-and-execute.md) and [07-map-reduce](../../05-agentic-patterns/07-map-reduce.md).

2. "Your supervisor system routes 90 percent of tickets correctly. What is actually broken about that number?"
You do not know which 10 percent, or what the misroutes cost. Break the 90 into a confusion matrix per specialist, weight by risk - a misroute to the refund specialist is not equal to one to the FAQ - and add trajectory rows for the worst confusion cells. The answer's point: a single routing number hides the failure shape, and the failure shape is what you fix. Teaches: [04-supervisor](../../05-agentic-patterns/04-supervisor.md) with [06 Evals](../../06-evals-and-observability/).

3. "The swarm demo looks impressive. Your manager asks if it is production-ready. Answer."
No - and say why in pattern terms: unspecified routing, no seam contracts, no HITL attachment points, coordination cost unmeasured. The production path: supervisor or hierarchical over the same specialists, handoff payloads defined, trajectory evals on the seams. The sentence that lands: "the specialists are probably fine; the control flow is the part that needs engineering." Teaches: [06-swarm](../../05-agentic-patterns/06-swarm.md) and [08-when-to-use-which](../../05-agentic-patterns/08-when-to-use-which.md).

4. "A reflexion loop improved your code-gen agent's pass rate by 5 points but doubled cost. Ship or not?"
Frame it as a tiered decision: default single-pass, reflexion only on failure - the retry loop engages when the first attempt fails validation, capturing most of the 5 points at a fraction of the cost. Ship the gated version, and track "cost per solved task," the metric that settles it. The bar: reflexion as escalation policy, not universal habit. Teaches: [03-reflexion](../../05-agentic-patterns/03-reflexion.md).

5. "Design review: your teammate proposes five specialist agents for a docs assistant. Push back constructively."
The constraint check: one domain, one tool cluster, moderate context - a single agent with retrieval and doc tools covers it; the five-agent split buys parallelism the task does not need and pays five system prompts, four handoffs, and a coordination taxonomy. Offer the measured compromise: single agent now, split later IF the evals show context overflow or tool-selection degradation - a constraint with a trigger, not an architecture as a default. Teaches: [08-when-to-use-which](../../05-agentic-patterns/08-when-to-use-which.md).

6. "One map-reduce worker hangs and the whole report waits. Fix the join."
Per-item timeout at the dispatch layer, so the join sees a timeout result rather than waiting; the reducer treats late/absent as missing data with a marker, and synthesis notes the gap. Then the product question: is a report missing one section better than no report? Usually yes - degrade, flag, and offer a retry for the missing slice only. Teaches: [07-map-reduce](../../05-agentic-patterns/07-map-reduce.md).

7. "Your hierarchical system's top supervisor keeps misrouting between teams. Where is the real bug?"
Usually the team descriptions at the top router, not the specialists: overlapping team charters read as plausible destinations. Fix the boundary descriptions with exclusions (same principle as tool descriptions), or insert a cheap classification step before the supervisor. Verify with the confusion matrix per team - routing is a classification problem with the same machinery. Teaches: [05-hierarchical](../../05-agentic-patterns/05-hierarchical.md).

8. "Handoffs between your two agents lose context - the second re-asks resolved questions. Redesign the seam."
Make the handoff payload explicit: a task brief node that writes what the receiver needs (question, resolved facts, artifacts, open items) into shared state, instead of forwarding raw history. The receiver's system prompt states its assumptions. Say the trade: a good brief costs a model call but saves the receiver's re-derivation and the user's patience. Teaches: [06-swarm](../../05-agentic-patterns/06-swarm.md).

9. "Latency budget: 10 seconds, and the plan-execute-replan flow takes 14. Where do you cut?"
Parallelize execution first (the map side), then cut coordination hops - replan only on divergence, not every cycle; then tier models (planner strong, executor cheap). The number discipline: instrument per-node latency before cutting, because the 14 seconds usually concentrate in two model calls, and cutting the wrong one buys nothing. Teaches: [02-plan-and-execute](../../05-agentic-patterns/02-plan-and-execute.md).

10. "A candidate architecture slide shows 'autonomous multi-agent swarm, self-organizing.' Your one-line review?"
"Self-organizing is not a control flow - show me the routing policy, the seam contracts, and the trajectory evals." Every architecture must be answerable for who decides what and where the human sits; a system that cannot say is a demo, not a design. Teaches: [08-when-to-use-which](../../05-agentic-patterns/08-when-to-use-which.md) and [01-landscape](../../10-interview-preparation/01-interview-landscape.md).
