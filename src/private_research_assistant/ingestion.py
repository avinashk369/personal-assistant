"""Markdown loading, sentence-aware chunking, and persistent indexing."""

from __future__ import annotations

from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

from private_research_assistant.cleaning import clean_markdown
from private_research_assistant.config import Settings
from private_research_assistant.models import build_embedding_model
from private_research_assistant.store import get_vector_store


def load_documents(settings: Settings):
    documents = SimpleDirectoryReader(input_dir=str(settings.data_dir), required_exts=[".md"]).load_data()
    for document in documents:
        document.set_content(clean_markdown(document.text))
        document.metadata["content_cleaned"] = True
    return documents


def ingest(settings: Settings, *, reset: bool = False) -> int:
    documents = load_documents(settings)
    if not documents:
        raise FileNotFoundError(f"No Markdown files found in {settings.data_dir}. Run collection first.")
    splitter = SentenceSplitter(chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)
    nodes = splitter.get_nodes_from_documents(documents)
    storage_context = StorageContext.from_defaults(vector_store=get_vector_store(settings, reset=reset))
    VectorStoreIndex(nodes, storage_context=storage_context, embed_model=build_embedding_model(settings))
    return len(nodes)
