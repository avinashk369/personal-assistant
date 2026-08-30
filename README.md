# Private Local Research Assistant

A learning-focused, read-only RAG system. It collects a small public corpus with Firecrawl, indexes Markdown locally with LlamaIndex and Chroma, and generates cited answers with a local Ollama model. The assistant has no tools, browser access, file-writing ability, or code execution capability during a query.

## Project structure

```text
src/private_research_assistant/
  collection.py       # Explicit Firecrawl allowlist and manifest
  ingestion.py        # Markdown -> chunks -> Chroma
  query.py            # Read-only retrieval and cited synthesis
  evaluation.py       # Deterministic citation/grounding checks
  cli/                # Thin executable adapters
data/                 # Collected Markdown (generated)
storage/chroma/       # Persistent local vectors (generated)
evaluation/           # 10-question suite and generated report
tests/                # Fast unit tests; no model required
```

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
ollama pull llama3:8b
ollama pull nomic-embed-text
```

Add your `FIRECRAWL_API_KEY` to `.env`. The defaults use `llama3:8b` for generation and `nomic-embed-text` for embeddings; both can be changed through environment variables.

## Run the pipeline

```bash
# 1. Scrape four explicit Python-packaging pages into data/
research-collect

# 2. Chunk Markdown (512 tokens, 50-token overlap) and create a local Chroma index
research-ingest --reset

# 3. Ask a question and inspect the exact retrieved chunks
research-query "How do I install a Python package?"

# 4. Run 7 in-bounds and 3 adversarial questions
research-evaluate
```

The root scripts (`collect.py`, `ingest.py`, `query.py`, and `evaluate.py`) provide the same commands after installation.

## Why these choices

The 512-token chunk size keeps each retrieval result focused enough to cite; a 50-token overlap avoids losing meaning at a chunk boundary. Generation is deterministic (`temperature=0`) and receives only numbered retrieved excerpts. The prompt requires each factual sentence to cite `[1]`, `[2]`, and so on, and requires the exact abstention: `I do not know based on the provided documents.`

`research-evaluate` writes `evaluation/results.json`. Its deterministic checker verifies that every factual claim cites an available chunk and has substantial word overlap with that cited evidence. This is useful for repeatable learning, but not a replacement for human review in high-stakes work.
