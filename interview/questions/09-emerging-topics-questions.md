# 09 Emerging topics - interview questions (concepts)

Status: beta | Teaches: [09 Emerging topics](../../09-emerging-topics/) | Part 1 of 2

1. What is the "agent OS" idea, and what problem is it pointing at?
The emerging layer that standardizes what every agent runtime needs: tool protocols (MCP), interop (A2A), memory conventions, sandboxing, and observability - the operating-system-like substrate under agents. The problem: every team currently rebuilds the same plumbing. The interview stance: name it as a direction, not a product - the components exist, the consolidation is the trend. Teaches: [01-agent-os](../../09-emerging-topics/01-agent-os.md).

2. Long-horizon memory - what is beyond the Store today?
Structured, queryable memory that survives tasks and months: episodic (what happened), semantic (facts distilled), and procedural (what worked) - with retrieval policies, decay, and write discipline. The research frontier the question is fishing for: agents that consolidate their own memory offline (sleep-time consolidation) instead of only writing at interaction time. Teaches: [02-long-horizon-memory](../../09-emerging-topics/02-long-horizon-memory.md).

3. What is an autonomous SDLC agent, and what bounds it today?
An agent that owns a slice of the software lifecycle - issue to patch to tests to PR - with verification loops as its safety net. Bounds: verification strength (tests are the leash), review (the PR gate), and task scoping (bugfix-shaped tasks yes, architecture-shaped tasks not yet). The honest sentence: autonomy scales with the strength of the check, not with the model. Teaches: [03-autonomous-sdlc](../../09-emerging-topics/03-autonomous-sdlc.md).

4. Agentic browsing - what can it actually do, and what remains hard?
It drives a real browser: navigate, read state, click, fill - enabling agents to act on the web built for humans. Hard parts: dynamic UIs that change under the agent, auth and session security (credentials holding), anti-bot friction, and non-deterministic page behavior that breaks replay. The design answer: treat the page like a flaky tool - bounded steps, verification of outcomes, human handoff on anomaly. Teaches: [04-agentic-browsers](../../09-emerging-topics/04-agentic-browsers.md).

5. Self-improving agents - what is real today versus research narrative?
Real: feedback loops where evals and traces feed prompt and tool refinements; offline consolidation of memory; automatic test generation hardening the agent's own harness. Narrative: models editing their own weights or capabilities without human-gated verification. The interview line: self-improvement today is a data-and-eval pipeline, and the eval gate is the difference between improvement and drift. Teaches: [05-self-improving-agents](../../09-emerging-topics/05-self-improving-agents.md).

6. What new safety surfaces do agentic systems add beyond chatbot risk?
Action capability (tools that change the world), persistence (memory that outlives the session and accumulates influence), composition (protocols that let agents act on each other's behalf), and autonomy-at-scale (a bad policy executing 10,000 times before a human looks). The bar: safety today is alignment-of-incentives at the tool boundary - scoped permissions, approval gates, audit trails - not model-level guarantees. Teaches: [06-safety-and-alignment](../../09-emerging-topics/06-safety-and-alignment.md).

7. Why do experts keep saying evaluation is the bottleneck for agent progress?
Because capability outruns measurement: models improve, but no team can ship confidently without knowing what changed - and behavioral systems change under prompt edits, model swaps, and tool drift. The eval practice is the rate-limiter on everything else in the field. This is also why every chapter in this curriculum treats evaluation as load-bearing; an interview answer that says this plainly signals field literacy. Teaches: [06-safety-and-alignment](../../09-emerging-topics/06-safety-and-alignment.md) with [06 Evals](../../06-evals-and-observability/).

8. What is the outlook question you should be able to answer: which parts of an agent stack get absorbed by providers, and which stay yours?
The absorbed layer: model access, basic orchestration primitives, protocol plumbing, hosting - commoditized into platforms. The durable layer: your tools and data boundaries, your eval set and baselines, your domain trajectories, your human-approval policy - the parts encoding judgment about your business. The strategic sentence: platforms eat plumbing; judgment compounds. Teaches: [01-agent-os](../../09-emerging-topics/01-agent-os.md).

9. What is a "society of agents" and why does coordination research matter for it?
Populations of specialized agents - across vendors and owners - discovering and delegating work through protocols. Coordination matters because the failure modes compound: misaligned incentives between agents you do not own, cascading errors through delegation chains, and trust boundaries nobody audited. The A2A deployment scenarios in [07](../../07-multi-agent-and-a2a/) are the early, governed version of this. Teaches: [01-agent-os](../../09-emerging-topics/01-agent-os.md) and [07 Multi-agent and A2A](../../07-multi-agent-and-a2a/).

10. What should a senior engineer do differently because of where the field is going?
Hold interfaces loose and measurement tight: adopt protocols at the boundaries (MCP, A2A) rather than hard-coded integrations, keep the eval harness and golden sets as the firm asset, and let the model and platform layers churn underneath. Plus: invest in the human-approval topology now, because action-capable systems only get more autonomous, and the gates you build this year are the ones that scale. Teaches: [07-continuous-improvement](../../08-production/07-continuous-improvement.md) and the [architecture view](../../ARCHITECTURE.md).
