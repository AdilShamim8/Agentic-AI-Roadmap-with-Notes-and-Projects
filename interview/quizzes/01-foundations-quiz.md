# Quiz 01 - Foundations

Status: beta | Covers: [01 Foundations](../../01-foundations/) | 10 questions

1. The defining property of an agent, versus a workflow, is:
A) It uses tools
B) The LLM decides the control flow
C) It runs in a loop
D) It has a system prompt

2. Temperature set to zero is appropriate for:
A) Creative drafting
B) Routing and extraction steps
C) All agent steps, always
D) Nothing - it breaks the API

3. Structured output beats prompt-asked JSON because:
A) It is cheaper per call
B) The schema is enforced at decode time
C) Prompts cannot describe JSON
D) Models score higher on benchmarks

4. A tool returns an error string. What happens next?
A) The graph raises and the run dies
B) The error becomes the tool result the model sees and adapts to
C) The framework retries three times silently
D) The user sees the raw stack trace

5. The most token-expensive property of agent conversations is:
A) System prompts
B) Tool schemas
C) The full message history resent on every call
D) Streaming overhead

6. Prompt injection is:
A) An attack that overflows the context window
B) Untrusted input that redirects the agent by impersonating instructions
C) A prompt-engineering technique for better results
D) A provider-side content filter

7. The structural defense against a hijacked prompt reaching valuable actions is:
A) Stronger wording in the system prompt
B) Lower temperature
C) Scoped permissions and approval gates in the tool layer
D) Longer few-shot examples

8. "The agent feels warmer" should be implemented as:
A) Temperature raised on all steps
B) Tone in the compose step's prompt only
C) A fine-tune
D) More system prompt adjectives

9. When the context window is exceeded, providers typically:
A) Refuse the call or silently truncate the oldest content
B) Automatically summarize
C) Continue flawlessly
D) Charge extra and continue

10. Fine-tuning, versus prompting, is the right tool when:
A) You need the model to know new facts
B) Behavior is stable, volume is high, and it is about style or format
C) Retrieval is failing
D) The agent keeps calling the wrong tool

## Answer key

1. B - who decides the next step is the dividing line ([chapter 01](../../01-foundations/01-what-is-agentic-ai.md)).
2. B - determinism where correctness is discrete ([chapter 03](../../01-foundations/03-llm-fundamentals.md)).
3. B - decode-time constraint, not advice ([chapter 05](../../01-foundations/05-structured-outputs-and-tools.md)).
4. B - errors are model-visible results; routing on them is the design ([chapter 05](../../01-foundations/05-structured-outputs-and-tools.md)).
5. C - stateless model APIs resend history every turn ([chapter 03](../../01-foundations/03-llm-fundamentals.md)).
6. B - instructions smuggled through untrusted content ([chapter 04](../../01-foundations/04-prompt-engineering.md)).
7. C - enforcement lives where actions execute ([chapter 05](../../01-foundations/05-structured-outputs-and-tools.md)).
8. B - generation-layer property, solved in one place ([chapter 03](../../01-foundations/03-llm-fundamentals.md)).
9. A - history management is your job from day one ([chapter 03](../../01-foundations/03-llm-fundamentals.md)).
10. B - fine-tunes move style, not knowledge ([chapter 03](../../01-foundations/03-llm-fundamentals.md)).
