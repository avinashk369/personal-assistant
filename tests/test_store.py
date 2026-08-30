from dataclasses import replace

from private_research_assistant.config import get_settings
from private_research_assistant.store import get_vector_store


def test_reset_allows_missing_collection(tmp_path):
    settings = replace(get_settings(), chroma_dir=tmp_path, collection_name="test_research")
    store = get_vector_store(settings, reset=True)
    assert store._collection.name == "test_research"
