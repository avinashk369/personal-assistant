from private_research_assistant.config import get_settings


def test_chunk_settings_are_valid():
    settings = get_settings()
    assert settings.chunk_size == 512
    assert 0 <= settings.chunk_overlap < settings.chunk_size
