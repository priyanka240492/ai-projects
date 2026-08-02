# Local RAG Pipeline — LangChain + ChromaDB + Claude

A fully local Retrieval-Augmented Generation (RAG) system built from scratch.
Ask questions over your own documents — answers are grounded in your data, with source citations.

No hallucinations. No cloud vector store. No OpenAI dependency.

---

## Stack

| Layer | Tool | Why |
|---|---|---|
| Orchestration | LangChain 0.2 (LCEL) | Industry standard, composable chains |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` | Free, fast, ~90MB, no API key needed |
| Vector Store | ChromaDB (local, persistent) | Zero infra, runs on your machine |
| Retrieval | MMR (Maximal Marginal Relevance) | Avoids returning duplicate chunks |
| LLM | Claude Haiku via Anthropic API | Fast, accurate, grounded responses |
| Document Loading | LangChain PyPDFLoader | Handles multi-page PDFs |
| Web UI | Streamlit | File upload, chat history, source citations |

---

## Project Structure

```
local-rag-langchain/
├── src/
│   └── rag_pipeline/
│       ├── __init__.py
│       ├── config.py          # all settings in one place
│       ├── ingest.py          # load → chunk → embed → store
│       ├── rag.py             # retriever + LLM chain (LCEL)
│       ├── app.py             # interactive CLI entrypoint
│       └── streamlit_app.py  # web UI entrypoint
├── tests/
│   └── __init__.py            # placeholder for Phase 2 RAGAS evals
├── data/                      # drop your PDFs here (gitignored)
├── vectorstore/               # ChromaDB persists here (gitignored)
├── .env.example               # API key template (committed)
├── .gitignore
├── Makefile                   # shortcuts: make ingest, make chat, make ui
├── pyproject.toml             # modern Python packaging
└── README.md
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/priyanka240492/ai-projects.git
cd ai-projects
```

### 2. Create virtual environment (Python 3.11 required)
```bash
# Windows
py -3.11 -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Install as a package
```bash
pip install --upgrade pip
pip install -e ".[dev]"
```

### 4. Set up your API key
```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```
Get your key at: https://console.anthropic.com

---

## Usage — two ways to run

### Option A — Streamlit web UI (recommended)

```bash
make ui
# or: streamlit run src/rag_pipeline/streamlit_app.py
```

Opens at **http://localhost:8501** in your browser automatically.

**In the UI:**
1. Click **Browse files** in the sidebar → select your PDF or TXT file
2. Click **Ingest documents** → wait for the green **● Ready to query** status
3. Type your question in the chat box at the bottom
4. Answer appears with source citation underneath

To stop the server: press **Ctrl + C** in the terminal.

> **First run tip:** Streamlit will ask for your email on first launch — just press Enter to skip.

---

### Option B — CLI (terminal)

```bash
# Step 1: add documents to data/ folder
cp your_document.pdf data/

# Step 2: ingest (one-time per document set)
make ingest
# or: python -m rag_pipeline.ingest

# Step 3: start querying
make chat
# or: python -m rag_pipeline.app
```

**Single question mode:**
```bash
python -m rag_pipeline.app -q "What is the employee ID in the document?"
```

---

## Example (Streamlit UI)

```
Upload: relieving_letter.pdf  →  Ingested 4 chunks ✓

You:       What is the employee ID mentioned in the document?
Assistant: The employee ID mentioned in the document is xx12345.
           📄 Source: data/relieving_letter.pdf

You:       When was the letter issued?
Assistant: The letter was issued on 04 August 2022.
           📄 Source: data/relieving_letter.pdf
```

---

## Makefile shortcuts

| Command | What it does |
|---|---|
| `make install` | Install all dependencies |
| `make ingest` | Load and embed documents from `data/` |
| `make chat` | Start interactive CLI |
| `make ui` | Launch Streamlit web UI at localhost:8501 |
| `make clean` | Remove vectorstore and pycache |

---

## Key Design Decisions

### Why MMR over simple similarity search?
MMR (Maximal Marginal Relevance) balances relevance with diversity. Plain similarity
search can return 4 near-identical chunks from the same paragraph. MMR ensures the
retrieved context covers different parts of the document, giving the LLM more signal.

### Why chunk overlap?
`RecursiveCharacterTextSplitter` uses a 100-token overlap between chunks. This preserves
context across chunk boundaries — a sentence split across two chunks won't lose meaning.

### Why centralise config?
All settings (chunk size, model names, paths, temperature) live in `config.py`. Changing
the embedding model or LLM requires editing one file, not hunting across the codebase.

### Why LCEL (LangChain Expression Language)?
The chain is built with the `|` pipe operator. Swapping any component — e.g. replacing
Claude with Ollama, or ChromaDB with pgvector — is a one-line change, not a rewrite.

### Why Streamlit over Gradio?
Streamlit gives finer control over layout, session state, and sidebar — making it easier
to build a proper multi-step UI (upload → ingest → chat) compared to Gradio's
single-function model.

---

## Swapping the LLM to fully local (no API key)

Install Ollama: https://ollama.com
```bash
ollama pull llama3.2
```

In `src/rag_pipeline/rag.py`, replace:
```python
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model=ANTHROPIC_MODEL, ...)
```
With:
```python
from langchain_community.llms import Ollama
llm = Ollama(model="llama3.2", temperature=0)
```

---

## Debugging lessons learned

| Problem | Root cause | Fix |
|---|---|---|
| `numpy` build error | Python 3.13 has no ML wheels yet | Use Python 3.11 |
| `Split into 0 chunks` | PDF was image-based (scanned) | Use digitally created PDFs |
| ChromaDB version conflict | `langchain-chroma 0.1.4` excludes `chromadb==0.5.5` | Unpin chromadb version |
| `insufficient_quota` | OpenAI free tier exhausted | Use HuggingFace embeddings (free) |
| `404 model not found` | Wrong Claude model string | Use `claude-haiku-4-5-20251001` |
| `ModuleNotFoundError: setuptools.backends` | Old setuptools version in venv | Change build-backend to `setuptools.build_meta` and run `pip install --upgrade setuptools` |
| `ModuleNotFoundError: rag_pipeline` | Package not installed in editable mode | Run `pip install -e ".[dev]"` before `streamlit run` |

---

## `pyproject.toml` note — build backend

If you see `ModuleNotFoundError: No module named 'setuptools.backends'`:

```bash
pip install --upgrade setuptools
pip install -e ".[dev]"
```

Or update `pyproject.toml`:
```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"   # ← stable, universally supported
```

---

## Roadmap

- [x] Phase 1 — Basic RAG pipeline with Streamlit UI
- [ ] Phase 2 — Advanced retrieval: reranking, hybrid search, HyDE
- [ ] Phase 3 — RAGAS eval in GitHub Actions CI/CD quality gate
- [ ] Phase 4 — Fine-tuned domain embeddings
- [ ] Phase 5 — Agentic RAG with LangGraph

---

## Author

**Lakshmi Priyanka Kaduluri**
Data Engineer | AWS | GenAI
[GitHub](https://github.com/priyanka240492) · [LinkedIn](https://www.linkedin.com/in/lakshmipriyanka-k/)