"""Persistent local Chroma collection management."""

import chromadb
from chromadb.errors import NotFoundError
from llama_index.vector_stores.chroma import ChromaVectorStore

from private_research_assistant.config import Settings


def get_vector_store(settings: Settings, *, reset: bool = False) -> ChromaVectorStore:
    settings.chroma_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(settings.chroma_dir))
    if reset:
        try:
            client.delete_collection(settings.collection_name)
        except NotFoundError:
            # A first ingestion has nothing to reset. Chroma treats this as an error,
            # but it is the expected empty-state behavior for this command.
            pass
    collection = client.get_or_create_collection(settings.collection_name)
    return ChromaVectorStore(chroma_collection=collection)
