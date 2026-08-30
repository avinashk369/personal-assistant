from private_research_assistant.cleaning import clean_markdown


def test_cleaning_removes_navigation_and_clipboard_noise():
    markdown = """### Navigation
- [index](https://example.com)
# Installing Packages [¶](https://example.com/#packages)

Use `python -m pip install Example`.

Copy to clipboard

### [Table of Contents](https://example.com/toc)
footer
"""
    assert clean_markdown(markdown) == "# Installing Packages\n\nUse `python -m pip install Example`.\n"


def test_cleaning_drops_read_the_docs_flyout_menu():
    """Read the Docs sites append a language/version flyout after the final
    "* * *" separator; it is not a heading, so `_FOOTER_HEADING` cannot catch it."""
    markdown = """# Installing Packages

Use `python -m pip install Example`.

* * *

Languages**[en](https://example.com)**Versions**[latest](https://example.com)**On Read the Docs[Project Home](https://example.com)Search

* * *

[Addons documentation](https://example.com) - Hosted by
[Read the Docs](https://example.com)
"""
    assert clean_markdown(markdown) == "# Installing Packages\n\nUse `python -m pip install Example`.\n\n* * *\n"
