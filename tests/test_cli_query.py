import pytest

from private_research_assistant.cli.query import _resolve_settings, main
from private_research_assistant.config import get_settings


def test_resolve_settings_without_limit_is_unchanged():
    settings = get_settings()
    resolved = _resolve_settings(settings, None)
    assert resolved == settings


def test_resolve_settings_with_limit_overrides_only_retrieval_top_k():
    settings = get_settings()
    resolved = _resolve_settings(settings, 2)
    assert resolved.retrieval_top_k == 2
    assert resolved.chunk_size == settings.chunk_size
    assert resolved.chunk_overlap == settings.chunk_overlap
    assert resolved.llm_model == settings.llm_model
    assert resolved.embedding_model == settings.embedding_model


@pytest.mark.parametrize("limit", ["0", "-1"])
def test_cli_rejects_non_positive_limit(limit, monkeypatch, capsys):
    # parser.error() exits before ResearchAssistant is ever constructed, so this
    # never touches Ollama/Chroma.
    monkeypatch.setattr("sys.argv", ["research-query", "--limit", limit, "irrelevant question"])
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 2
    assert "--limit must be a positive integer" in capsys.readouterr().err
