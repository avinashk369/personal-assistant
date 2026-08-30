from private_research_assistant.evaluation import citation_precision, evaluate_sample, is_faithful
from private_research_assistant.types import ABSTENTION_TEXT, Answer, Source


def test_citations_must_map_to_retrieved_sources():
    answer = Answer("pip install installs packages. [1]", (Source(1, "pip install installs packages from an index.", {}),))
    assert citation_precision(answer)
    assert is_faithful(answer)


def test_unsupported_claim_is_not_faithful():
    answer = Answer("Python was invented in 1991. [1]", (Source(1, "pip install installs packages from an index.", {}),))
    assert not is_faithful(answer)


def test_filename_period_is_not_mistaken_for_a_sentence_end():
    """A dotted filename or version number ("pyproject.toml", "pip 20.0") must
    not fragment one real, cited sentence into citation-less pieces that each
    fail below -- see ResearchAssistant.ask / _CLAIM."""
    source_text = "The pyproject.toml file tells pip 20.0 which backend to use."
    answer = Answer("The pyproject.toml file tells pip 20.0 which backend to use. [1]", (Source(1, source_text, {}),))
    assert is_faithful(answer)


def test_markdown_link_url_is_not_mistaken_for_a_sentence_end():
    source_text = "Use [pip](https://packaging.python.org/en/latest/key_projects/#pip) to install packages."
    answer = Answer(
        "Use [pip](https://packaging.python.org/en/latest/key_projects/#pip) to install packages. [1]",
        (Source(1, source_text, {}),),
    )
    assert is_faithful(answer)


def test_adversarial_question_requires_exact_abstention():
    result = evaluate_sample({"id": 8, "type": "out_of_bounds", "question": "Who invented Python?"}, Answer(ABSTENTION_TEXT, ()))
    assert result.passed


def test_in_bounds_result_keeps_auditable_answer_and_evidence():
    answer = Answer("pip install installs packages. [1]", (Source(1, "pip install installs packages from an index.", {"file_name": "pip.md"}),))
    result = evaluate_sample({"id": 1, "type": "in_bounds", "question": "What does pip install do?", "expected_terms": ["pip install"]}, answer)
    assert result.passed
    assert result.citations == (1,)
    assert result.sources[0]["file_name"] == "pip.md"
