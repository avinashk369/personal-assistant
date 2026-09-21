# CLAUDE.md

## Project purpose

A learning-focused, local RAG (retrieval-augmented generation) system: collect a small
public corpus with Firecrawl, index it locally with LlamaIndex + Chroma, and generate
cited answers with a local Ollama model. The point of the project is rigorous,
auditable grounding — not feature breadth.

## Architectural invariants (do not violate)

- **Read-only, no agentic actions.** The application's RAG assistant has no
  tools, browser access, file-writing ability, or code execution capability during
  a user query. These constraints apply to the application being developed, not
  to Claude Code or the development environment.
- **No cloud LLM calls.** Generation and embeddings run through Ollama against
  `OLLAMA_BASE_URL` (default `http://localhost:11434`). Never add a cloud model
  provider or route a query through a hosted API.
- **No external write operations at query time.** Collection (Firecrawl) is the only
  stage that talks to the outside world, and only to an explicit URL allowlist.
- **Ollama stays local.** Model factories live in `models.py` only — don't scatter
  LLM/embedding construction elsewhere.
- **`evaluation.py` is dual-purpose and must stay that way.** Its checkers
  (`citation_precision`, `is_faithful`, `is_relevant`) are used both as a **runtime
  guardrail** inside `ResearchAssistant.ask` (query.py) — to decide whether to trust
  a generated answer or fall back to extractive quoting — and as the **offline
  scorer** for `research-evaluate`. Do not fork this logic into two copies; if you
  change a threshold or rule, it affects both call sites intentionally.

## Pipeline architecture

```
collect (Firecrawl -> data/*.md)
  -> ingest (clean -> chunk -> embed -> Chroma, storage/chroma/)
    -> query (retrieve -> prompt Ollama -> self-verify -> cite or abstain)
      -> evaluate (run query over a fixed question set, score groundedness)
```

Each stage is a plain function, wired to a CLI by a thin adapter in `cli/`. Root
scripts (`collect.py`, `ingest.py`, `query.py`, `evaluate.py`) just call the same
`cli.*:main` functions — they're convenience wrappers, not a second implementation.

## Module boundaries

- **Framework-independent** (no LlamaIndex/Chroma/Ollama imports): `types.py`,
  `cleaning.py`, `evaluation.py`. Keep it this way — it's what makes the safety
  logic unit-testable without a model or vector store.
- **Framework-bound**: `store.py` (Chroma), `models.py` (Ollama), `ingestion.py`
  (LlamaIndex loading/chunking/indexing). Framework specifics belong here, not in
  `query.py` or `evaluation.py`.
- **`query.py`** is the orchestration layer: retrieval, prompting, self-verification
  against `evaluation.py`, and the extractive fallback. It should stay the only
  place that assembles these pieces into an answer.
- **`config.py`** is the single source of settings, loaded once into a frozen
  `Settings` dataclass. Don't add ad hoc `os.getenv` calls in other modules.

## Development / setup commands

```bash
python -m venv venv && source venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env        # fill in FIRECRAWL_API_KEY
ollama pull llama3:8b
ollama pull nomic-embed-text
```

Pipeline:

```bash
research-collect              # scrape the URL allowlist into data/
research-ingest --reset       # chunk + (re)index into Chroma
research-query "question"     # ask, prints answer + retrieved chunks
research-evaluate             # run the fixed question suite, writes evaluation/results.json
```

## Testing strategy — two tiers, don't conflate them

1. **`pytest`** — fast, deterministic, no Ollama/Chroma model calls required (one
   test in `test_store.py` touches a real Chroma `PersistentClient` against
   `tmp_path`, but no embeddings). This is the tier that must pass for any code
   change to logic in `cleaning.py`, `evaluation.py`, `query.py`'s fallback path,
   etc.
2. **`research-evaluate`** — slower, model-dependent integration check. It requires
   Ollama running and an ingested index, and measures actual answer quality against
   `evaluation/questions.json`, not code correctness.

Run `pytest` after any change to source under `src/`. Only run `research-evaluate`
when the change could plausibly affect retrieval or generation quality (prompt
wording, chunking, retrieval top-k, evaluation thresholds) — it's not a substitute
for `pytest` and shouldn't be run reflexively for unrelated changes.

## Evaluation baseline

The last recorded run scored **6/10** (`evaluation/results.json`, gitignored). Treat
this as the current baseline to compare against, not a target to preserve or a bar
that's already "good enough." If a change regresses the score, say so; if you improve
it, note the before/after — but don't tune the evaluator itself just to raise the
number.

**Evaluation integrity.** Treat `evaluation.py` as production-like
safety/measurement logic. When changing its rules or thresholds, explain the
reason and run the evaluation suite before and after the change. Do not change
evaluation criteria solely to improve the reported score.

## Security / secrets

- `FIRECRAWL_API_KEY` lives in `.env` (gitignored) and is loaded via `config.py`.
  Never hardcode it, log it, or write it into `data/`, `evaluation/`, or committed
  files.
- `collection.py` intentionally fails loudly (`RuntimeError`) if the key is missing
  rather than silently skipping collection — preserve that behavior.
- The Firecrawl URL list in `collection.py` (`DEFAULT_URLS`) is an explicit
  allowlist. Don't make it accept arbitrary/user-supplied URLs without deliberate
  discussion — unbounded scraping is out of scope for this project.

## Current constraints worth knowing

- The corpus is 4 hardcoded Python-packaging pages; there's no CLI flag or env var
  to add more without editing `collection.py`.
- No CI, no lockfile, no `[tool.ruff]` config yet — don't assume lint rules or
  reproducible installs are enforced automatically.
- `storage/` and `data/*.md` are gitignored, generated artifacts. A fresh clone has
  nothing until `research-collect` + `research-ingest` are run.

## Engineering workflow

For non-trivial changes:

1. Inspect the relevant code, tests, and configuration first.
2. Explain the proposed approach before making architectural changes.
3. Prefer the smallest change that satisfies the requirement.
4. Implement the change.
5. Run the relevant tests.
6. Inspect the final git diff for unintended changes.
7. Report:
   - what changed
   - tests/checks run
   - evaluation impact, when applicable
   - remaining risks

For non-trivial changes, use the appropriate engineering Skill:

- **Architecture changes:** use the `architecture` Skill first. It must stop
  at the decision gate and wait for approval before implementation.
- **Implementation:** use the `implement` Skill for approved changes or
  straightforward implementation requests.
- **Debugging:** use the `debug` Skill when investigating an unexpected
  failure, regression, or bug.
- **Review:** use the `review` Skill after implementation when an independent
  verification of correctness, architecture, tests, and regression risk is
  appropriate.

Preferred workflows:

- Significant architectural change:
  `architecture → approval → implement → review`
- Normal feature/change:
  `implement → review`
- Bug or unexpected failure:
  `debug → implement → review`
- Simple isolated change:
  `implement`

Do not invoke Skills unnecessarily. Choose the smallest workflow that matches
the complexity and risk of the task.

When `architecture` recommends an implementation approach and the user
approves it, hand the approved plan to `implement` rather than redesigning it
during implementation.

When `review` identifies material issues, use `implement` or `debug` as
appropriate to address them, then run `review` again.

Do not commit or push changes unless explicitly requested.
Do not modify unrelated files.

## Rules for making changes

- **Inspect before you change.** Read the relevant module(s) and the module-boundary
  section above before editing — this codebase deliberately separates
  framework-independent logic from framework-bound code, and deliberately shares
  `evaluation.py` between runtime and offline use. Don't "fix" that structure without
  understanding why it's there.
- **Don't modify tests to make them pass.** If a test fails after a change, fix the
  code (or, if the test's premise is genuinely wrong, explain why and ask before
  changing the test) — never loosen an assertion or delete a test case just to get
  green output.
- **Run `pytest` after every source change.** Run `research-evaluate` too when the
  change could affect retrieval/generation quality (see Testing strategy above).
- **No unnecessary dependencies or abstractions.** This is a small, deliberately
  minimal pipeline. Don't add a new library, framework, or layer of indirection
  (factories, plugin systems, config layers) unless the task genuinely requires it —
  prefer extending an existing module over introducing a new one.
