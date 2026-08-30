"""LlamaIndex retrieval plus local LLM synthesis with source-numbered context."""

from __future__ import annotations

import re

from llama_index.core import VectorStoreIndex

from private_research_assistant.cleaning import strip_markdown_links
from private_research_assistant.config import Settings
from private_research_assistant.evaluation import citation_precision, is_faithful
from private_research_assistant.models import build_embedding_model, build_llm
from private_research_assistant.prompts import build_answer_prompt
from private_research_assistant.store import get_vector_store
from private_research_assistant.types import ABSTENTION_TEXT, Answer, Source

_WORD = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]+")
_QUERY_STOP_WORDS = frozenset("a an and are as at be by do for from how in is it of on or that the this to what where which who with".split())


def _format_context(sources: tuple[Source, ...]) -> str:
    return "\n\n".join(f"[{source.number}]\n{source.text}" for source in sources)


def _content_words(text: str) -> set[str]:
    return {word.lower() for word in _WORD.findall(text) if word.lower() not in _QUERY_STOP_WORDS}


_MAX_EVIDENCE_SENTENCE_CHARS = 400
# A single shared word (e.g. "python" or "package") is common by topic alone and
# does not indicate the retrieved text actually answers the question; two shared
# content words is the same bar `is_faithful` uses to avoid one-word coincidences.
_MIN_SHARED_WORDS = 2


def _best_evidence(question: str, sources: tuple[Source, ...]) -> list[tuple[float, int, str]]:
    question_words = _content_words(question)
    candidates: list[tuple[float, int, str]] = []
    for source in sources:
        # Strip markdown links first: a raw URL's periods would otherwise
        # fragment one real sentence into several meaningless pieces.
        for sentence in re.split(r"(?<=[.!?])\s+", strip_markdown_links(source.text)):
            sentence = sentence.strip()
            # A "sentence" longer than this has no terminal punctuation nearby
            # (a code block or link list, most likely) and is not real prose.
            if not sentence or len(sentence) > _MAX_EVIDENCE_SENTENCE_CHARS or "```" in sentence:
                continue
            words = _content_words(sentence)
            overlap = len(question_words & words)
            if overlap >= _MIN_SHARED_WORDS:
                candidates.append((overlap / max(len(question_words), 1), source.number, sentence))
    return sorted(candidates, reverse=True)


def _extractive_answer(question: str, sources: tuple[Source, ...]) -> Answer:
    """Return directly retrieved evidence when the LLM violates citation rules."""
    evidence = _best_evidence(question, sources)
    if not evidence:
        return Answer(ABSTENTION_TEXT, sources)
    # Do not manufacture a summary: show up to two relevant source sentences verbatim.
    selected: list[tuple[int, str]] = []
    for _, number, sentence in evidence:
        if (number, sentence) not in selected:
            selected.append((number, sentence))
        if len(selected) == 2:
            break
    text = "\n".join(f"{sentence} [{number}]" for number, sentence in selected)
    return Answer(text, sources)


class ResearchAssistant:
    """Read-only RAG facade. It exposes retrieval and generation, never tools/actions."""

    def __init__(self, settings: Settings):
        self.settings = settings
        index = VectorStoreIndex.from_vector_store(
            get_vector_store(settings), embed_model=build_embedding_model(settings)
        )
        self.retriever = index.as_retriever(similarity_top_k=settings.retrieval_top_k)
        self.llm = build_llm(settings)

    def ask(self, question: str) -> Answer:
        if not question.strip():
            raise ValueError("Question must not be blank.")
        retrieved_nodes = self.retriever.retrieve(question)
        sources = tuple(
            Source(number=index, text=item.node.get_content(), metadata=item.node.metadata)
            for index, item in enumerate(retrieved_nodes, start=1)
        )
        if not sources:
            return Answer(ABSTENTION_TEXT, sources)
        prompt = build_answer_prompt(question, _format_context(sources))
        generated = Answer(str(self.llm.complete(prompt)).strip(), sources)
        if generated.text == ABSTENTION_TEXT:
            return _extractive_answer(question, sources) if _best_evidence(question, sources) else generated
        if citation_precision(generated) and is_faithful(generated):
            return generated
        return _extractive_answer(question, sources)
