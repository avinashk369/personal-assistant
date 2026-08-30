"""Small framework-independent data structures shared across layers."""

from collections.abc import Mapping
from dataclasses import dataclass

ABSTENTION_TEXT = "I do not know based on the provided documents."


@dataclass(frozen=True)
class Source:
    number: int
    text: str
    metadata: Mapping[str, object]


@dataclass(frozen=True)
class Answer:
    text: str
    sources: tuple[Source, ...]
