"""Tests for the interview quiz demo: dataset integrity and grading."""

from __future__ import annotations

from pathlib import Path

import pytest

from examples.interview_quiz_demo import (
    DEFAULT_DATASET,
    Question,
    filter_by_module,
    grade,
    load_questions,
    self_check,
)


def _all_questions() -> list[Question]:
    return load_questions(DEFAULT_DATASET)


def test_dataset_loads_with_all_nine_modules():
    questions = _all_questions()
    modules = {q.module for q in questions}
    assert modules == {f"0{i}" for i in range(1, 10)}
    assert len(questions) >= 45


def test_every_row_is_well_formed():
    for q in _all_questions():
        assert q.answer in ("A", "B", "C", "D")
        assert len(q.options) == 4
        assert all(opt.strip() for opt in q.options)
        assert q.prompt.strip()
        assert q.explanation.strip()


def test_module_filter_selects_and_rejects():
    questions = _all_questions()
    chosen = filter_by_module(questions, "02")
    assert chosen and all(q.module == "02" for q in chosen)
    assert filter_by_module(questions, "all") == questions
    with pytest.raises(ValueError, match="unknown module"):
        filter_by_module(questions, "42")


def test_grade_counts_correct_and_skipped():
    questions = _all_questions()[:3]
    answers = {
        0: questions[0].answer,
        1: "X" if questions[1].answer != "X" else "Y",
    }
    correct, results = grade(questions, answers)
    assert correct == 1
    assert results == [True, False, False]


def test_self_check_passes_on_the_real_dataset(capsys):
    questions = _all_questions()
    assert self_check(questions) == 0
    out = capsys.readouterr().out
    assert "PASS" in out
    assert "9" in out  # module count


def test_loader_rejects_bad_answer_letter(tmp_path: Path):
    bad = tmp_path / "bad.csv"
    header = ("module,question,option_a,option_b,option_c,option_d,"
              "answer,explanation\n")
    bad.write_text(
        header + "01,q,a,b,c,d,E,why\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="bad answer"):
        load_questions(bad)


def test_loader_rejects_missing_column(tmp_path: Path):
    bad = tmp_path / "bad.csv"
    bad.write_text("module,question,answer\n01,q,A\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing columns"):
        load_questions(bad)
