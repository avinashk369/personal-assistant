"""Constrained prompt used for all generation."""

from private_research_assistant.types import ABSTENTION_TEXT


def build_answer_prompt(question: str, context: str) -> str:
    return f"""You are a private research assistant. Answer only using the numbered source excerpts below.
Do not use external knowledge. Do not speculate. Keep the answer concise and prefer wording that appears in the excerpts.
Every factual sentence must end with the relevant source label, such as [1] or [1][2]. Do not place a citation on its own line or cite a sentence that it does not support.
If the excerpts do not contain the answer, reply with exactly: {ABSTENTION_TEXT}

Source excerpts:
{context}

Question: {question}
Answer:"""
