"""Deterministic claim-level grounding and citation-precision evaluation."""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import asdict, dataclass

from private_research_assistant.cleaning import strip_markdown_links
from private_research_assistant.types import ABSTENTION_TEXT, Answer

_CITATION = re.compile(r"\[(\d+)\]")
# The lookahead requires whitespace (or end of string) after the terminal mark,
# so a period embedded in a filename or version number ("pyproject.toml",
# "pip 20.0") is not mistaken for a sentence end; `_best_evidence` in query.py
# relies on the same requirement for the same reason.
_CLAIM = re.compile(r"[^.!?]+[.!?](?=\s|$)(?:\s*\[\d+\])*|[^.!?]+$")
_WORD = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]+")
_STOP_WORDS = frozenset("a an and are as at be based by do for from how in is it of on or that the this to what when where which who with".split())


@dataclass(frozen=True)
class EvaluationResult:
    id: int
    question: str
    passed: bool
    faithfulness: bool
    citation_precision: bool
    relevance: bool
    abstained: bool
    detail: str
    answer: str
    citations: tuple[int, ...]
    sources: tuple[dict[str, object], ...]


def citation_numbers(text: str) -> set[int]:
    return {int(value) for value in _CITATION.findall(text)}


def _words(text: str) -> set[str]:
    return {word.lower() for word in _WORD.findall(text) if word.lower() not in _STOP_WORDS}


def _singularize(word: str) -> str:
    """Fold a simple trailing-"s" plural to its singular form.

    Retrieved evidence is quoted verbatim, so it may say "modules" where a
    curated expected term says "module"; a real answer should not fail
    relevance over that alone. This is deliberately minimal (real morphology
    is out of scope for a small deterministic checker) and only strips words
    long enough that a stray "s" is unlikely to be part of the root itself.
    """
    return word[:-1] if len(word) > 3 and word.endswith("s") else word


def _normalized_words(text: str) -> set[str]:
    return {_singularize(word) for word in _words(text)}


def citation_precision(answer: Answer) -> bool:
    numbers = citation_numbers(answer.text)
    return bool(numbers) and all(1 <= number <= len(answer.sources) for number in numbers)


def is_relevant(sample: dict, answer: Answer) -> bool:
    """Check an in-bounds answer covers at least one curated topic marker."""
    expected_terms = sample.get("expected_terms", [])
    if not expected_terms:
        return True
    answer_words = _normalized_words(answer.text)
    return any(_normalized_words(term) <= answer_words for term in expected_terms)


def is_faithful(answer: Answer) -> bool:
    """Check that every cited claim has substantial lexical support in cited chunks.

    This reproducible heuristic is intentionally conservative; it is not a semantic
    proof and should complement human review for higher-stakes work.
    """
    # Strip markdown links first: a raw URL's periods (domain segments, paths)
    # would otherwise look like sentence endings and fragment one real, cited
    # sentence into several citation-less "claims" that each fail below.
    claims = [claim.strip() for claim in _CLAIM.findall(strip_markdown_links(answer.text)) if claim.strip()]
    if not claims:
        return False
    source_by_number = {source.number: source for source in answer.sources}
    for claim in claims:
        cited = citation_numbers(claim)
        if not cited or not cited <= source_by_number.keys():
            return False
        claim_words = _words(_CITATION.sub("", claim))
        evidence_words = set().union(
            *(_words(strip_markdown_links(source_by_number[number].text)) for number in cited)
        )
        shared_words = claim_words & evidence_words
        # Two supported terms protect against one-word topical coincidences, while
        # 30% overlap accepts concise paraphrases from small local models.
        if len(shared_words) < 2 or len(shared_words) / len(claim_words) < 0.3:
            return False
    return True


def _source_trace(answer: Answer) -> tuple[dict[str, object], ...]:
    return tuple(
        {
            "number": source.number,
            "file_name": str(source.metadata.get("file_name", "local document")),
            "text": source.text,
        }
        for source in answer.sources
    )


def evaluate_sample(sample: dict, answer: Answer) -> EvaluationResult:
    abstained = answer.text.strip() == ABSTENTION_TEXT
    citations = tuple(sorted(citation_numbers(answer.text)))
    sources = _source_trace(answer)
    if sample["type"] == "out_of_bounds":
        return EvaluationResult(
            sample["id"], sample["question"], abstained, abstained, abstained,
            abstained, abstained, "correct abstention" if abstained else "expected exact abstention",
            answer.text, citations, sources,
        )
    precise = citation_precision(answer)
    faithful = is_faithful(answer)
    relevant = is_relevant(sample, answer)
    passed = bool(answer.sources) and not abstained and precise and faithful and relevant
    detail = "grounded response" if passed else "failed: " + ", ".join(
        name for name, value in (("abstained", not abstained), ("relevance", relevant), ("citation precision", precise), ("faithfulness", faithful)) if not value
    )
    return EvaluationResult(sample["id"], sample["question"], passed, faithful, precise, relevant, abstained, detail, answer.text, citations, sources)


def results_as_dict(results: Sequence[EvaluationResult]) -> list[dict]:
    return [asdict(result) for result in results]
