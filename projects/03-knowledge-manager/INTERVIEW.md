# Interview guide - Project 03: Knowledge manager

Status: beta | For: presenting this project in interviews | Related: [project README](README.md), [project stories](../../10-interview-preparation/15-project-stories.md)

## The pitch

"Capture-in-passing memory: an agent that stores facts, notes, and documents with the `Store` API - namespaced per user, retrievable in any later conversation, with scoped search so a query returns what that person is allowed to see. The design problem is not storing; it is what retrieval returns six weeks later."

## The whiteboard script

1. The state boundary: conversations are threads (checkpointer); long-term memory is the `Store` with namespaces.
2. The capture node - extracts structured facts from the running conversation (typed schema: fact, source, timestamp).
3. The retrieval tool - scoped search over the namespace, returns facts with provenance, not a blob.
4. The write policy - update-in-place for volatile facts (preferences), append for episodic; recency ranking on retrieval.
5. The eval - memory rows where the correct answer depends on a newer fact outranking an older one.

The line that earns the nod: "Memory needs a schema and a lifecycle, or it becomes a swamp."

## The numbers you quote

- Namespace scoping per user; retrieval top-k with recency weighting.
- Your memory-eval numbers if built; otherwise the design target stated as designed-for.

## The follow-ups

- "How is this different from a checkpointer?" Checkpoints hold this conversation; the Store holds facts about the user that outlive every conversation - "remembers the chat" vs "remembers the user."
- "What if a stored fact is wrong now?" Write policy updates volatile classes in place; provenance and timestamps let retrieval prefer the newest; the failure story is the year-old preference - and the memory-eval row that catches it.
- "Multi-tenant?" Namespace per tenant enforced server-side; canary queries in the eval proving cross-tenant reads never happen.
- "Why not just a vector DB over everything?" Recall without structure returns plausible-but-stale context; typed facts with decay behave.

## The red flags

- Presenting memory as "we store everything and embed it" - the swamp answer.
- No retrieval scoping story in a multi-user context.
- Claiming memory solves personalization without a freshness policy.

## What this project proves

Store-vs-checkpointer literacy, memory schema design, and the long-term thinking that memory-centric roles screen for.
