# Mock: system design

Module: 10-interview-preparation
Chapter: 22-mock-system-design
Status: beta
Last reviewed: 2026-11-26
Estimated time: 1 hour

## Learning objectives

- Watch the six-part structure run against a live design prompt
- See the recovery moves when the interviewer pushes off the script
- Steal the closing line that ties design rounds up

## The setup

The prompt: "Design an internal IT-helpdesk agent: employees ask for password resets, VPN access, and software installs. Some actions are low-risk, some are not." The candidate uses the six parts from [05](05-system-design-structure.md). Time-stamped, so you can see the budget hold.

## The transcript

[00:00] Candidate: "Before I draw anything: what volume, and what is the risk split - which actions can be fully automated versus which need a human today?"

[Commentary: requirements opened by asking, not assuming - the volume answer (3,000 employees, about 500 tickets a day) and the risk answer (password resets are self-service-able today, installs need license approval) arrive in the first two minutes because they were requested.]

[00:05] "Success metric first: deflection of the low-risk tickets with zero security incidents, p95 under 4 seconds. Non-goals: I am not building the approval workflow itself - that exists in the ITSM tool - the agent calls it."

[Commentary: the success metric and the non-goal are stated before any architecture. The non-goal sentence about the ITSM tool is the one that earns the nod from an interviewer who has seen candidates rebuild ServiceNow inside the agent.]

[00:10] "Architecture. One agent, not multi - three intents and a handful of tools do not justify coordination overhead. State: messages, plus a `pending_action` holding the structured action awaiting execution, plus the requester's identity from the session. ReAct-style loop, because tool results change what the agent does next. Checkpointing on Postgres: the ticket survives the handoff to a human."

[Commentary: pattern chosen with the alternative named, state schema spoken out loud, persistence placed with a reason. Three rubric lines in four sentences.]

[00:20] "Tools. `verify_identity(session)` - server-side, no model involvement. `reset_password(account)` - low-risk, executes directly. `request_install(account, software, justification)` - writes to the ITSM queue, executes but does not approve. `get_policy(topic)` - scoped retrieval over the IT policy docs, the same retrieval-as-a-tool shape. Identity and authorization run in the tool layer; the model can request actions, never grant them."

[Commentary: the security sentence at the end is the differentiator. The risk split from minute one is now embodied in the tool list - reset executes, install queues. This is requirements-to-architecture traceability, visible.]

[00:30, the interruption] Interviewer: "The security team wants every install action reviewed by the requesting employee's manager, in chat, not in the ITSM queue."

Candidate: "Then the install tool becomes an `interrupt()` - the agent proposes the install, the graph pauses with the structured proposal, the manager gets a chat prompt with approve/reject, and `Command(resume=...)` carries the decision back. The ITSM queue still gets the approved request. One change, in one place - the tool's risk class decides the mechanism, and the mechanism is structural, not a prompt instruction the model could skip."

[Commentary: the mid-flight requirement change is deliberate - interviewers test whether the architecture absorbs change or collapses. The candidate absorbed it by pointing at where risk classes map to mechanisms. Note the resume answer never blames the new requirement.]

[00:40] "Evaluation. Golden set from last quarter's tickets: 30-plus rows of input, expected intent, expected tool, expected args. Exact-match on intent and tool; an evaluator that an install request NEVER executes without a resume event in the trajectory; an LLM-judge on the response text for tone and completeness. Baseline before shipping, and the gate runs in CI on every change."

[Commentary: the trajectory check tied to the new security requirement, volunteered without being asked. This is the "evals match the architecture" line that most design answers lack.]

[00:50] "Production: `langgraph build`, Kubernetes, two replicas, managed Postgres for the checkpointer. Streaming to the chat client. Monitoring on tool-error rate, deflection rate, and install approval latency - that last one is the manager's experience, and it is where this system will get quietly killed if it is slow. Cost: intent classification drops to a cheap model class; password resets are the 60 percent and they need no reasoning at all."

[Commentary: monitoring chosen from the product's politics, not the dashboard's convenience. The model-tiering sentence has arithmetic behind it, stated without being asked.]

[01:00, the close] Interviewer: "Anything you would add?"

Candidate: "The one thing I would ship first is the eval gate and the canary: three questions whose correct behavior is 'refuse and route to a human,' run on every deploy. Everything else here can degrade gracefully; silent wrong automation in IT is how this project gets cancelled in month two."

[Commentary: the close restates the eval-first identity in the product's own stakes. Design rounds are remembered by their last minute; this one earns it.]

## The recovery moves worth memorizing

- Interrupted with a new requirement: point at where the risk class maps to the mechanism, absorb, move on.
- Asked about scale you did not plan for: "At that volume the fan-out changes - per-intent subgraphs and a queue in front of the graph" - a stated delta, not a redesign.
- The blank: "Give me ten seconds to place this against the state schema" - silence named as thinking reads as thinking; silence unnamed reads as drowning.

## What is next

[23 Mock: behavioral](23-mock-behavioral.md) - the round that is easy to pass and easy to fail on one story.
