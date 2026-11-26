# Interview guide - Project 01: Research agent

Status: beta | For: presenting this project in interviews | Related: [project README](README.md), [project stories](../../10-interview-preparation/15-project-stories.md)

## The pitch

"Iterative retrieval with citations and a hard turn budget: the agent decomposes a question, searches, reads, reformulates, and synthesizes a cited summary - and a budget field in state ends the loop deterministically, because 'the model decides when to stop' is not a control flow."

Say it in 30 seconds, then stop. The listener pulls the thread they care about.

## The whiteboard script

Draw in this order, narrating:

1. State: `plan` (sub-questions), `findings` (per sub-question, with source IDs), `budget` (remaining iterations).
2. The plan node - decomposes once, commits the plan to state.
3. The loop: search tool, read tool, a findings node, and the edge back conditioned on `budget > 0`.
4. The synthesis node - composes with per-claim citations; runs on budget exhaustion too, marking gaps.
5. The checkpointer - long runs resume after crashes instead of restarting.

The line that earns the nod: "The recursion limit is the retrieval cap." It compresses the whole reliability story into six words.

## The numbers you quote

- Iterations capped at N (say your number); typical convergence in 2-4.
- Cost per run capped by the budget field - the number is a design constant, not a hope.
- Citation faithfulness on your golden set (if you built the eval - if not, say that is the first addition).

Quote only numbers you observed. Anything else is "designed for, not yet measured."

## The follow-ups

- "How do you stop hallucinated citations?" Per-claim source IDs required by the synthesis schema; the faithfulness evaluator rejects claims without them.
- "What if the loop never converges?" The budget field exhausts; synthesis runs on partial findings and marks the gaps. Deterministic end, honest output.
- "Why plan-and-execute, not ReAct?" The plan commits once and parallelizes; ReAct re-decides per step and serializes.
- "What breaks at scale?" Source drift mid-run - snapshot the extracted text at read time and cite the snapshot.

## The red flags

- Presenting it as "RAG with LangChain" - the design is the loop and the budget, not the vector store.
- No eval story. This project's whole point is controllable iteration; an unmeasured loop is a toy.
- Claiming it "reads the whole internet." Scope honesty: scoped sources, bounded reads.

## What this project proves

Retrieval-as-a-tool judgment, loop control as state design, and citation discipline - the three things a research-agent role screens for.
