"""Local Ollama model factories. No cloud model is configured here."""

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

from private_research_assistant.config import Settings


def build_llm(settings: Settings) -> Ollama:
    return Ollama(
        model=settings.llm_model,
        base_url=settings.ollama_base_url,
        temperature=0.0,
        context_window=8192,
        request_timeout=120.0,
    )


def build_embedding_model(settings: Settings) -> OllamaEmbedding:
    return OllamaEmbedding(model_name=settings.embedding_model, base_url=settings.ollama_base_url)
