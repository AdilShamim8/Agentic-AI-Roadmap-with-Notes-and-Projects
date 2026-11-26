# 01 Foundations - interview questions (concepts)

Status: beta | Teaches: [01 Foundations](../../01-foundations/) | Part 1 of 2

1. What is an agent, in one sentence, and what distinguishes it from a workflow?
An agent is a system where an LLM decides the control flow - which tool to call, when to stop, what to do next - in a loop. A workflow follows a path fixed by the code author. The interview bar: say "who decides the next step" as the dividing line, not "uses tools." Teaches: [01-what-is-agentic-ai](../../01-foundations/01-what-is-agentic-ai.md).

2. When is a workflow the better choice over an agent?
When the task's steps are known in advance and do not depend on intermediate results: extraction, classification, fixed pipelines. Agents pay cost, latency, and unpredictability for their flexibility; if the branch points are enumerable, code them. The strong answer names the tradeoff, not a preference. Teaches: [01-what-is-agentic-ai](../../01-foundations/01-what-is-agentic-ai.md).

3. What does temperature actually control, and when do you set it to zero?
Temperature scales the logits' softmax distribution - low values concentrate probability on the likeliest tokens, high values flatten it. Zero for deterministic-ish steps: routing, extraction, evaluation. Nonzero for generation where variety is a feature. Follow-up to expect: current Claude models reject temperature 0 outright; know that you set the default and override per step. Teaches: [03-llm-fundamentals](../../01-foundations/03-llm-fundamentals.md).

4. Why does structured output beat prompt-please-emit-JSON?
Because the constraint is enforced at decode time via the API's structured-output or function-calling interface, not begged for in the prompt. Schema-constrained decoding cannot emit invalid JSON; a prompt asking for it can, and does, at exactly the wrong traffic hour. Teaches: [05-structured-outputs-and-tools](../../01-foundations/05-structured-outputs-and-tools.md).

5. A tool call returns an error. Where does the model see it, and what should it do?
The error goes back into the message list as the tool's result; the model then decides - retry with fixed arguments, try another tool, or tell the user. Your job is to make errors informative ("unknown customer" vs "backend down") because the model routes on the difference. The anti-pattern: swallowing errors in the tool layer. Teaches: [05-structured-outputs-and-tools](../../01-foundations/05-structured-outputs-and-tools.md).

6. What is a system prompt's actual job in an agent?
Bound the role: what the agent may do, what it must refuse, the output conventions, the escalation policy. It is the policy document the model consults every turn - which is why "the prompt will prevent dangerous behavior" is the answer that fails loops: policy in the prompt is advisory; enforcement belongs to the tool layer. Teaches: [04-prompt-engineering](../../01-foundations/04-prompt-engineering.md).

7. Name the failure mode of few-shot prompting in production agents.
Distribution drag: the model over-fits to the examples' surface features instead of the rule, and the examples age into the model's context permanently, costing tokens every turn. The strong answer names the alternative: put the invariant in the schema or the tool design, keep few-shot for genuinely open-textured judgment only. Teaches: [04-prompt-engineering](../../01-foundations/04-prompt-engineering.md).

8. Why LangGraph over an agent framework that hides the loop?
Because the graph makes the loop inspectable: nodes, edges, and state are explicit, so debugging, persistence, human-in-the-loop, and evaluation attach to the structure instead of fighting a hidden runtime. The honest version: frameworks that own the loop are fine for demos; the moment you need a checkpoint, an interrupt, or a trajectory eval, you need the loop to be a first-class object. Teaches: [02-why-langgraph](../../01-foundations/02-why-langgraph.md).

9. Tokens: why does an agent's cost per task grow non-linearly with conversation length?
Because most agent APIs resend the full message history on each call - the context is stateless on the model side. A 20-turn tool-using conversation pays for the whole history 20 times. This is the arithmetic behind context trimming, summarization of old turns, and checkpoint design. Teaches: [03-llm-fundamentals](../../01-foundations/03-llm-fundamentals.md).

10. What is a context window, and what actually happens when you exceed it?
It is the maximum input the model attends over in one call; exceed it and the call errors, or the provider silently truncates the oldest content. The design consequence for agents: history management is your job from day one - trim, summarize, or move long-term facts to retrieval and out of the window. Teaches: [03-llm-fundamentals](../../01-foundations/03-llm-fundamentals.md).

11. Give the one-line business case for an agent over a classic ML classifier.
A classifier answers one fixed question; an agent composes capabilities - look up, act, verify, explain - and adapts when the task's steps vary. The cost is reliability engineering, which is the job. Teaches: [01-what-is-agentic-ai](../../01-foundations/01-what-is-agentic-ai.md).

12. What is prompt injection, and what is the structural defense?
An input that treats your prompt as attack surface - instructions smuggled in retrieved documents or user text that redirect the agent. The structural defense is a boundary: untrusted content is data (quoted, never executed), destructive tools require identity and approval in the tool layer, and permissions are scoped so a hijacked prompt has nothing valuable to reach. Teaches: [04-prompt-engineering](../../01-foundations/04-prompt-engineering.md), deepened in [04 Tools and MCP](../../04-tools-and-mcp/).
