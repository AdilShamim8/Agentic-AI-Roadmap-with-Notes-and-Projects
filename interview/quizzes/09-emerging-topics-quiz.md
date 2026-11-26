# Quiz 09 - Emerging topics

Status: beta | Covers: [09 Emerging topics](../../09-emerging-topics/) | 10 questions

1. The "agent OS" refers to:
A) A Linux distribution for agents
B) The consolidating substrate - tool protocols, interop, memory, sandboxing, observability
C) One vendor's product
D) A model architecture

2. Long-horizon memory research points toward:
A) Bigger context windows only
B) Structured episodic/semantic/procedural memory with offline consolidation
C) Storing everything in prompts
D) Fine-tuning facts into weights

3. Autonomous SDLC agents are bounded today by:
A) Model size
B) Verification strength - tests and review are the leash
C) Token costs only
D) Provider terms

4. Agentic browsing remains hard because:
A) Browsers are slow
B) Dynamic UIs, auth/session security, and non-deterministic pages break replay
C) HTML is deprecated
D) Models cannot read

5. Self-improving agents, today, concretely are:
A) Models editing their own weights
B) Eval-and-trace pipelines feeding prompt and tool refinements, with a gate
C) Autonomous prompt rewriting without review
D) A vendor feature

6. The new safety surface agents add beyond chatbots:
A) Rudeness
B) Action capability, persistence, cross-agent composition, autonomy at scale
C) Higher token costs
D) Context windows

7. "Evaluation is the bottleneck" because:
A) Models stopped improving
B) Behavioral systems change under prompts, tiers, and tool drift - measurement rate-limits shipping
C) Judges are expensive
D) Users demand numbers

8. The layer platforms will absorb first:
A) Your eval sets
B) Plumbing - model access, orchestration primitives, protocol serving, hosting
C) Your domain tools
D) Your approval policies

9. A safe overnight autonomous run requires:
A) A strict prompt
B) Read-and-propose tool scopes, morning-window approvals, budget caps, anomaly halts
C) A bigger model
D) Human observers

10. The senior engineer's posture through platform churn:
A) Chase every release
B) Loose interfaces at protocol boundaries, tight measurement - golden sets and gates as firm assets
C) Avoid all protocols
D) Specialize in one vendor

## Answer key

1. B - direction, not product ([chapter 01](../../09-emerging-topics/01-agent-os-and-kernels.md)).
2. B - consolidation beyond interaction time ([chapter 02](../../09-emerging-topics/02-long-horizon-memory.md)).
3. B - autonomy scales with the check, not the model ([chapter 03](../../09-emerging-topics/03-autonomous-sdlc.md)).
4. B - treat the page as a flaky tool ([chapter 04](../../09-emerging-topics/04-agentic-browsers.md)).
5. B - improvement with a regression gate ([chapter 05](../../09-emerging-topics/05-self-improving-agents.md)).
6. B - action-capable systems at scale ([chapter 06](../../09-emerging-topics/07-safety-and-alignment.md)).
7. B - capability outruns measurement ([chapter 06](../../09-emerging-topics/07-safety-and-alignment.md)).
8. B - judgment compounds; plumbing does not ([chapter 01](../../09-emerging-topics/01-agent-os-and-kernels.md)).
9. B - autonomy is a spectrum set by scopes and budgets ([chapter 06](../../09-emerging-topics/07-safety-and-alignment.md)).
10. B - platforms eat plumbing ([chapter 10 of the field guide](../../field-guide/02-skills-that-matter.md)).
