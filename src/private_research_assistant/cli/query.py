import argparse

from private_research_assistant.config import get_settings
from private_research_assistant.query import ResearchAssistant


def main() -> None:
    parser = argparse.ArgumentParser(description="Query the private local research index.")
    parser.add_argument("question", nargs="*", help="question to ask; omit for interactive input")
    args = parser.parse_args()
    question = " ".join(args.question) or input("Question: ").strip()
    answer = ResearchAssistant(get_settings()).ask(question)
    print(f"\n{answer.text}\n\nSources:")
    for source in answer.sources:
        filename = source.metadata.get("file_name", "local document")
        print(f"\n[{source.number}] {filename}\n{source.text[:500]}")


if __name__ == "__main__":
    main()
