"""LLM-as-judge demonstration with a versioned rubric.

Implements the judge from chapter 06/03: a multi-dimensional rubric, a
versioned judge prompt, and a structured-output score. The judge must
be a different model family from the actor to avoid self-preference
bias; this demo uses Claude for the actor and Claude with a different
model for the judge only because a second provider key is not always
available - in production, cross families (e.g. Claude judging GPT).

Run:
    python examples/llm_judge_demo.py

Environment:
    ANTHROPIC_API_KEY - required (the judge is an LLM call)
    EXAMPLES_MODEL - optional actor model override
    JUDGE_MODEL - optional judge model override
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.runnables import Runnable
from langchain_core.tools import tool
from pydantic import BaseModel, Field

load_dotenv()

MODEL = os.environ.get("EXAMPLES_MODEL", "claude-sonnet-5-5")
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")

RUBRIC_VERSION = "v1.0.0"


class AnswerScore(BaseModel):
    """Structured output the judge must return."""

    correctness: int = Field(
        description="Score 1-5: does the answer address the question correctly?"
    )
    completeness: int = Field(
        description="Score 1-5: does it provide all needed information?"
    )
    tone: int = Field(description="Score 1-5: is it polite and professional?")
    explanation: str = Field(description="One sentence explaining the scores.")


JUDGE_PROMPT = """You are evaluating a customer support answer.

Question: {question}
Answer: {answer}

Score each dimension 1-5:
- correctness: does the answer address the question correctly?
- completeness: does it provide all needed information?
- tone: is it polite and professional?

Be strict. A score of 5 means excellent; 3 means acceptable; 1 means poor.
Rubric version: {rubric_version}
"""


@tool
def answer_question(question: str) -> str:
    """The actor: answer a support question (mocked; an LLM in production)."""
    return "Click 'Forgot Password' on the login page, then follow the email link."


def build_judge() -> Runnable:
    """Build the judge LLM with structured output bound."""
    judge_llm = ChatAnthropic(model=JUDGE_MODEL)
    return judge_llm.with_structured_output(AnswerScore)


def __getattr__(name: str):
    """Lazily build the module-level judge; importing needs no API key."""
    if name == "judge":
        return build_judge()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def judge_answer(question: str, answer: str) -> AnswerScore:
    """Score one answer against the rubric (requires ANTHROPIC_API_KEY)."""
    judge = build_judge()
    prompt = JUDGE_PROMPT.format(
        question=question, answer=answer, rubric_version=RUBRIC_VERSION
    )
    return judge.invoke(prompt)


def main() -> None:
    """Judge a sample answer and report the structured scores."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("[!] ANTHROPIC_API_KEY is not set; the judge is an LLM call.")
        print("    Set it in .env (see .env.example) and re-run.")
        return

    print(f"\n=== LLM-as-judge demo (rubric {RUBRIC_VERSION}) ===\n")
    question = "How do I reset my password?"
    answer = answer_question.invoke({"question": question})
    print(f"Question: {question}")
    print(f"Answer (actor): {answer}\n")

    score = judge_answer(question, answer)
    print(f"Scores (judge={JUDGE_MODEL}, actor={MODEL}):")
    print(f"  correctness: {score.correctness}/5")
    print(f"  completeness: {score.completeness}/5")
    print(f"  tone: {score.tone}/5")
    print(f"  explanation: {score.explanation}")

    assert 1 <= score.correctness <= 5
    assert 1 <= score.completeness <= 5
    assert 1 <= score.tone <= 5
    print("\nLLM-as-judge validation passed.")


if __name__ == "__main__":
    main()
