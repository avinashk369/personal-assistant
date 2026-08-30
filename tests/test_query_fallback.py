from private_research_assistant.query import _best_evidence, _extractive_answer
from private_research_assistant.types import ABSTENTION_TEXT, Source


def test_fallback_returns_source_labeled_evidence():
    sources = (Source(1, "Install packages with python -m pip install Example.", {}),)
    answer = _extractive_answer("How do I install packages with pip?", sources)
    assert answer.text.endswith("[1]")
    assert "pip install" in answer.text


def test_single_shared_word_is_not_evidence():
    """A one-word topical coincidence must not look like support for an
    adversarial question, or a correct abstention gets overridden with a
    fabricated non-abstention answer (see ResearchAssistant.ask)."""
    sources = (Source(1, "Python packages are installed with pip.", {}),)
    assert _best_evidence("Who invented Python?", sources) == []
    assert _extractive_answer("Who invented Python?", sources).text == ABSTENTION_TEXT


def test_code_block_is_not_treated_as_a_sentence():
    sources = (
        Source(
            1,
            "Install packages with pip.\n\n```\npip install a very long line "
            + "of code without any terminal punctuation to speak of at all\n```",
            {},
        ),
    )
    evidence = _best_evidence("How do I install packages with pip?", sources)
    assert all("```" not in sentence for _, _, sentence in evidence)
