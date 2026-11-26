"""Interview quiz CLI: drill the curriculum question banks without a key.

Loads datasets/interview_quiz.csv (one row per question) and runs an
interactive quiz, or a non-interactive self-check when stdin is not a TTY
(so CI can verify dataset integrity keylessly and cheaply).

Run:
    python examples/interview_quiz_demo.py                 # interactive
    python examples/interview_quiz_demo.py --module 02     # one module
    python examples/interview_quiz_demo.py --random 10     # sampled drill
    python examples/interview_quiz_demo.py --self-check    # validation only

Environment:
    none. This demo is fully keyless by design - it quizzes you, not a
    model; the questions come from the repo's own quiz banks.
"""

from __future__ import annotations

import argparse
import csv
import random
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATASET = REPO_ROOT / "datasets" / "interview_quiz.csv"
OPTIONS = ("A", "B", "C", "D")
MODULE_NAMES = {
    "01": "Foundations",
    "02": "LangGraph core",
    "03": "Agents in practice",
    "04": "Tools and MCP",
    "05": "Agentic patterns",
    "06": "Evals and observability",
    "07": "Multi-agent and A2A",
    "08": "Production",
    "09": "Emerging topics",
}


@dataclass(frozen=True)
class Question:
    module: str
    prompt: str
    options: tuple[str, str, str, str]
    answer: str
    explanation: str


def load_questions(path: Path = DEFAULT_DATASET) -> list[Question]:
    """Load the quiz dataset, validating shape as we read."""
    questions: list[Question] = []
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        required = {"module", "question", "option_a", "option_b",
                    "option_c", "option_d", "answer", "explanation"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing columns: {sorted(missing)}")
        for row in reader:
            answer = row["answer"].strip().upper()
            if answer not in OPTIONS:
                raise ValueError(f"bad answer {row['answer']!r}")
            if not all(row[k].strip() for k in required):
                raise ValueError("empty field in row")
            questions.append(Question(
                module=row["module"].strip(),
                prompt=row["question"].strip(),
                options=(row["option_a"], row["option_b"],
                         row["option_c"], row["option_d"]),
                answer=answer,
                explanation=row["explanation"].strip(),
            ))
    if not questions:
        raise ValueError("empty quiz dataset")
    return questions


def filter_by_module(questions: list[Question], module: str) -> list[Question]:
    """Select one module ('02'); 'all' returns everything."""
    if module == "all":
        return questions
    chosen = [q for q in questions if q.module == module]
    if not chosen:
        known = ", ".join(sorted({q.module for q in questions}))
        raise ValueError(f"unknown module {module!r}; known: {known}")
    return chosen


def grade(questions: list[Question], answers: dict[int, str]) -> tuple[int, list[bool]]:
    """Grade answers keyed by question index; returns (correct, per-question)."""
    results = []
    for i, q in enumerate(questions):
        given = answers.get(i, "").strip().upper()
        results.append(given == q.answer)
    return sum(results), results


def self_check(questions: list[Question]) -> int:
    """Validate the dataset and print a summary; 0 exit on success."""
    modules = sorted({q.module for q in questions})
    answers = {q.answer for q in questions}
    print("[+] interview quiz self-check")
    print(f"    rows: {len(questions)}")
    print(f"    modules: {', '.join(modules)}")
    print(f"    answer letters used: {', '.join(sorted(answers))}")
    ok = (
        len(modules) == 9
        and answers.issubset(set(OPTIONS))
        and all(len(q.options) == 4 for q in questions)
    )
    print(f"[+] {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def run_interactive(questions: list[Question]) -> int:
    """Ask, grade, explain. Returns the number correct."""
    print(f"[+] {len(questions)} questions. Answer A/B/C/D; anything else skips.\n")
    answers: dict[int, str] = {}
    for i, q in enumerate(questions):
        label = MODULE_NAMES.get(q.module, q.module)
        print(f"{i + 1}. [{label}] {q.prompt}")
        for letter, text in zip(OPTIONS, q.options, strict=True):
            print(f"   {letter}) {text}")
        given = input("> ").strip().upper()
        if given in OPTIONS:
            answers[i] = given
        print()
    correct, results = grade(questions, answers)
    print(f"[+] Score: {correct}/{len(questions)}")
    for i, (q, right) in enumerate(zip(questions, results, strict=True)):
        if not right:
            print(f"    miss {i + 1}: {q.answer}) {q.explanation}")
    return correct


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Interview quiz drill")
    parser.add_argument("--module", default="all",
                        help="module number, e.g. 02 (default: all)")
    parser.add_argument("--random", type=int, default=0,
                        help="ask a random sample of N questions")
    parser.add_argument("--self-check", action="store_true",
                        help="validate the dataset and exit")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET,
                        help="path to the quiz CSV")
    args = parser.parse_args(argv)

    questions = load_questions(args.dataset)
    if args.self_check:
        return self_check(questions)

    module = args.module.zfill(2) if args.module != "all" else "all"
    questions = filter_by_module(questions, module)
    if args.random and args.random < len(questions):
        rng = random.Random(19)
        questions = rng.sample(questions, args.random)

    if sys.stdin.isatty():
        run_interactive(questions)
        return 0
    # Non-interactive (CI): run the self-check instead of hanging on input.
    return self_check(questions)


if __name__ == "__main__":
    raise SystemExit(main())
