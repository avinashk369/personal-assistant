from private_research_assistant.collection import collect_pages
from private_research_assistant.config import get_settings


def main() -> None:
    manifest = collect_pages(get_settings())
    for item in manifest:
        print(f"Saved {item['url']} -> data/{item['file']}")


if __name__ == "__main__":
    main()
