import argparse

from private_research_assistant.config import get_settings
from private_research_assistant.ingestion import ingest


def main() -> None:
    parser = argparse.ArgumentParser(description="Index local Markdown into Chroma.")
    parser.add_argument("--reset", action="store_true", help="replace this project's Chroma collection")
    args = parser.parse_args()
    count = ingest(get_settings(), reset=args.reset)
    print(f"Indexed {count} chunks.")


if __name__ == "__main__":
    main()
