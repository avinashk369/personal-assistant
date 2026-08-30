"""Application settings loaded once from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    project_root: Path
    data_dir: Path
    chroma_dir: Path
    evaluation_dir: Path
    collection_name: str
    chunk_size: int
    chunk_overlap: int
    retrieval_top_k: int
    ollama_base_url: str
    llm_model: str
    embedding_model: str
    firecrawl_api_key: str | None


def get_settings() -> Settings:
    root = Path(__file__).resolve().parents[2]
    load_dotenv(root / ".env")
    chunk_size = int(os.getenv("CHUNK_SIZE", "512"))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "50"))
    if not 0 <= chunk_overlap < chunk_size:
        raise ValueError("CHUNK_OVERLAP must be non-negative and less than CHUNK_SIZE.")
    return Settings(
        project_root=root,
        data_dir=root / "data",
        chroma_dir=root / "storage" / "chroma",
        evaluation_dir=root / "evaluation",
        collection_name=os.getenv("CHROMA_COLLECTION", "research_documents"),
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        retrieval_top_k=int(os.getenv("RETRIEVAL_TOP_K", "4")),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        llm_model=os.getenv("OLLAMA_LLM_MODEL", "llama3:8b"),
        embedding_model=os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text"),
        firecrawl_api_key=os.getenv("FIRECRAWL_API_KEY") or None,
    )
