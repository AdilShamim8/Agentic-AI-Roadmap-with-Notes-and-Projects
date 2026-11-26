# Quiz 05 - Agentic patterns

Status: beta | Covers: [05 Agentic patterns](../../05-agentic-patterns/) | 10 questions

1. ReAct's loop buys:
A) Cheaper runs
B) Adaptivity - each step informed by real observations
C) Deterministic outputs
D) Fewer tools

2. Plan-and-execute beats ReAct when:
A) Steps depend on each other's results
B) Tasks decompose cleanly and steps are independent
C) The model is weak
D) Latency does not matter

3. Reflexion's artifact is:
A) A fine-tuned model
B) Structured lessons written into memory that condition the retry
C) A shorter prompt
D) A cache of answers

4. Supervisor versus swarm, in one line:
A) Same pattern, different names
B) Supervisor routes centrally; swarm agents hand control peer-to-peer
C) Supervisor is always cheaper
D) Swarm is supervised by definition

5. Hierarchical multi-agent solves:
A) Token costs
B) Scaling supervision - each router's scope stays small
C) Evaluation
D) Persistence

6. The map-reduce join's classic failure:
A) Reducers run twice
B) One slow worker stalls the join; partial failures vanish
C) Send cannot parallelize
D) Plans become stale

7. Multi-agent is the wrong answer when:
A) One agent with the right tools covers the task
B) The team is large
C) Users request it
D) Tools exceed ten

8. A clean handoff requires:
A) The full raw history forwarded
B) An explicit task brief with resolved facts and open items
C) A shared model tier
D) Identical system prompts

9. Reflexion at doubled cost is best deployed as:
A) Always-on for every task
B) An escalation policy on first-attempt failure
C) A demo-only feature
D) A replacement for evals

10. Multi-agent evaluation adds, beyond endpoint scores:
A) Nothing new
B) Seam metrics - handoff accuracy, coordination tokens, per-agent trajectories
C) Only cost tracking
D) User satisfaction polls

## Answer key

1. B - at the cost of per-step latency and tokens ([chapter 01](../../05-agentic-patterns/01-react.md)).
2. B - plan once, execute in parallel ([chapter 02](../../05-agentic-patterns/02-plan-and-execute.md)).
3. B - reflection state, not just retries ([chapter 03](../../05-agentic-patterns/03-reflexion.md)).
4. B - legibility vs hops ([chapter 04](../../05-agentic-patterns/04-supervisor.md) and [06](../../05-agentic-patterns/05-swarm.md)).
5. B - the org-chart principle ([chapter 05](../../05-agentic-patterns/06-hierarchical.md)).
6. B - per-item timeout and error capture fix it ([chapter 07](../../05-agentic-patterns/07-map-reduce.md)).
7. A - name the constraint before the split ([chapter 08](../../05-agentic-patterns/08-when-to-use-which.md)).
8. B - contracts, not conventions ([chapter 06](../../05-agentic-patterns/05-swarm.md)).
9. B - gated retry captures most of the gain ([chapter 03](../../05-agentic-patterns/03-reflexion.md)).
10. B - systems can pass endpoints while burning coordination tokens ([chapter 08](../../05-agentic-patterns/08-when-to-use-which.md)).
