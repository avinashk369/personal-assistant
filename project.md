# Blueprint: Local Private Research Assistant with LlamaIndex, Ollama, Firecrawl, and Rigorous Evaluation

You are an expert AI systems architect and local machine-learning engineer. Help me build a **Private, Local Research Assistant** from scratch on my local machine. 

The primary goal of this project is hands-on learning across ingestion, vector search, local model generation, citation formatting, and custom evaluation—**without** introducing complex, risky agentic actions (no external write tools, no code execution sandbox, strictly read-only retrieval and generation).

---

## Technical Stack Constraints
* **Orchestration & Parsing:** LlamaIndex (Python)
* **Local LLM & Embeddings:** Ollama running a small Hugging Face model (e.g., `llama3:8b`, `mistral:7b`, or `phi3`) locally.
* **Vector Database:** ChromaDB or Qdrant (local persistent storage mode).
* **Data Collection:** Firecrawl (to scrape a small, targeted set of 3–5 public target web pages/docs into clean markdown).
* **Evaluation Framework:** Custom Python-based script checking claim-level grounding/faithfulness.

---

## Phase-by-Phase Implementation Plan

Please provide the complete, modular Python code and structural guidelines for the following 4 phases:

### Phase 1: Environment Setup & Firecrawl Data Collection
1. Provide a minimal script using the `firecrawl` SDK to scrape 3–5 specific URLs of a public topic of choice, saving them locally as clean markdown files into a `./data` directory.
2. Detail how to configure Ollama with LlamaIndex using `Ollama` and `OllamaEmbedding` local integration modules.

### Phase 2: LlamaIndex Ingestion & Local Vector Store
1. Write code to load the markdown files using LlamaIndex's `SimpleDirectoryReader`.
2. Parse the documents into optimal nodes (e.g., chunk size 512, overlap 50).
3. Embed and store these nodes persistently into either **ChromaDB** or **Qdrant** running locally.

### Phase 3: RAG Query Engine with Inline Citations
1. Configure a LlamaIndex query engine using your local Ollama model.
2. Implement a **Citation Query Engine** or custom prompt template that forces the local model to inject precise source citations (e.g., `[1], [2]`) mapping directly back to the retrieved text chunks.
3. Ensure the prompt explicitly instructs the model: *"If the context does not contain the answer, state that you do not know. Do not hallucinate external facts."*

### Phase 4: Custom 10-Question Groundedness Evaluation Suite
1. Design a programmatic **10-question evaluation dataset** JSON structure tailored to the scraped text. Include:
   * 7 "In-Bounds" questions (directly answerable by the text).
   * 3 "Out-of-Bounds" / Adversarial questions (facts *not* present in the text to test hallucination resistance).
2. Write a lightweight evaluation script that iterates through the 10 questions, queries your RAG pipeline, and uses a deterministic or LLM-as-a-judge approach to check:
   * **Faithfulness / Groundedness:** Are all claims in the response strictly backed by the cited text chunks?
   * **Citation Precision:** Do the citation numbers match the actual source node provided?

---

## Expected Output Format
* Provide clear, well-commented Python code blocks for each file (`ingest.py`, `query.py`, `evaluate.py`).
* Keep explanations educational, highlighting *why* specific parameters (like chunk size or prompt constraints) matter for learning.