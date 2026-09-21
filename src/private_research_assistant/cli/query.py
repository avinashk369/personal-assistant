import argparse
from dataclasses import replace

from private_research_assistant.config import Settings, get_settings
from private_research_assistant.query import ResearchAssistant


def _resolve_settings(settings: Settings, limit: int | None) -> Settings:
    """Apply a per-invocation --limit override to retrieval_top_k, if given."""
    return settings if limit is None else replace(settings, retrieval_top_k=limit)


def main() -> None:
    parser = argparse.ArgumentParser(description="Query the private local research index.")
    parser.add_argument("question", nargs="*", help="question to ask; omit for interactive input")
    parser.add_argument("--limit", type=int, default=None, help="override RETRIEVAL_TOP_K for this query")
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be a positive integer")
    question = " ".join(args.question) or input("Question: ").strip()
    settings = _resolve_settings(get_settings(), args.limit)
    answer = ResearchAssistant(settings).ask(question)
    print(f"\n{answer.text}\n\nSources:")
    for source in answer.sources:
        filename = source.metadata.get("file_name", "local document")
        print(f"\n[{source.number}] {filename}\n{source.text[:500]}")


if __name__ == "__main__":
    main()
