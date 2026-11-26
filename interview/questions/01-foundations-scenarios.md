# 01 Foundations - interview scenarios

Status: beta | Teaches: [01 Foundations](../../01-foundations/) | Part 2 of 2

1. "Your extraction agent occasionally emits JSON with a missing field. The prompt already says the field is required. Fix it."
Move the invariant from prompt to schema: use structured output with the field typed and required at the API level, so decode-time constraints reject the omission. Then add an eval row for the failing input so the fix is regression-checked. Anything that stays prompt-level is advice to the model, not a contract with it. Teaches: [05-structured-outputs-and-tools](../../01-foundations/05-structured-outputs-and-tools.md).

2. "A support bot answers correctly 95 percent of the time. The remaining 5 percent confabulate a policy. Walk me through your response."
First, characterize the 5 percent: are they questions the knowledge source covers (retrieval or grounding failure) or does not cover (the model filling silence)? For the first, fix retrieval and require citations per claim. For the second, teach refusal: the answer step must distinguish "not found" from "found," and unanswerable questions route to a human. The metric you propose: refusal correctness on a known-unanswerable set - confabulation is the failure mode that ends products. Teaches: [04-prompt-engineering](../../01-foundations/04-prompt-engineering.md) and [the docs-RAG case](../../10-interview-preparation/09-design-case-docs-rag.md).

3. "Marketing wants 'the agent to feel warmer.' Engineering wants determinism. Who wins?"
Both, in different layers: warmth is a generation-layer property (tone in the system prompt, higher temperature on the compose step only); determinism is a routing-and-tools property (structured outputs, low temperature, typed schemas on every decision that gates an action). The mistake is solving one with the other's tools - "we lowered the temperature so it is more professional" mutates the product answer. Teaches: [03-llm-fundamentals](../../01-foundations/03-llm-fundamentals.md).

4. "Your agent's cost doubled this month. Where do you look first?"
Token arithmetic: which steps resend the longest histories, which tool results return unbounded payloads, which turns retry. The classic culprits, in order: tool results without limits, no trimming of old turns, and a reasoning model used for classification. Fix structurally - bound the tools, summarize history, tier the models - and add cost per request to the dashboard so the next doubling announces itself. Teaches: [03-llm-fundamentals](../../01-foundations/03-llm-fundamentals.md).

5. "A user pasted instructions into a chat box and your agent followed them. What broke, and what do you change?"
A prompt-injection surface: user input was treated as authoritative instruction. Changes, in order of strength: move authority out of the prompt (the session carries identity and permissions, the tool layer enforces them), quote untrusted text as data in the context, require approval for destructive actions regardless of instructions, and add an eval row pair - the injection input and the required refusal trajectory. Teaches: [04-prompt-engineering](../../01-foundations/04-prompt-engineering.md).

6. "Why is your router an LLM call at all - why not regex?"
Say the honest boundary: regex wins when the intents are lexically stable and few; the LLM earns its cost when phrasing varies or intents overlap ("where is my stuff" is status; "my stuff never came" is a complaint). The strong answer proposes the hybrid: cheap deterministic rules for the obvious 80 percent, the model for the residue, and the router's confusion matrix in the eval set so the boundary is measured, not vibes. Teaches: [01-what-is-agentic-ai](../../01-foundations/01-what-is-agentic-ai.md).

7. "The CEO asks whether to fine-tune instead of prompting. Your answer in three sentences?"
Fine-tuning moves style and format into weights - good when behavior is stable and volume is high; it does not add knowledge and does not fix retrieval or tool errors. Prompting and schemas iterate in hours and keep the behavior inspectable. Ship the prompted system, measure, and fine-tune the one hot path where the evals show the model consistently failing a stable task. Teaches: [03-llm-fundamentals](../../01-foundations/03-llm-fundamentals.md).

8. "You inherit an agent with no system prompt discipline - ten prompts in code, all different. First week?"
Inventory and consolidate: one system prompt as the policy document, per-step prompts only where the step's task genuinely differs. Then version the prompts in files, not string literals, so review and rollback are possible, and add the eval set before touching the text - otherwise you cannot tell consolidation from regression. Teaches: [04-prompt-engineering](../../01-foundations/04-prompt-engineering.md).

9. "Your agent must answer in the user's language and keep structured metadata in English. How?"
Two channels: the user-facing generation follows the input language; the machine-facing artifacts (tool calls, structured outputs, eval labels) are pinned to English schemas. The failure to name: letting the user's language leak into tool arguments or eval sets - it breaks matching and creates silent eval drift. Teaches: [05-structured-outputs-and-tools](../../01-foundations/05-structured-outputs-and-tools.md).

10. "Product asks for a confidence score on every agent answer. What do you actually give them?"
Not a raw token logprob - it correlates weakly with correctness and calibrates worse. Give them a proxy that is real: a groundedness evaluator score (does the answer cite sources that exist), a retrieval hit indicator, and an abstention path when grounding is weak. Confidence as a product number must be measured behavior, not model self-report. Teaches: [05-structured-outputs-and-tools](../../01-foundations/05-structured-outputs-and-tools.md) with [06 Evals](../../06-evals-and-observability/).
