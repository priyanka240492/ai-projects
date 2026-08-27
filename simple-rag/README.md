# Simple RAG — LangChain + ChromaDB + Claude

A local Retrieval-Augmented Generation pipeline for asking questions over your own PDF and TXT documents.

## Architecture

```text
Documents -> PyMuPDF -> Chunking -> HuggingFace Embeddings -> ChromaDB
                                                               |
Question -> MMR Retrieval -> Context -> Claude -> Answer + Sources
```

## Stack

- Python 3.11+
- LangChain LCEL
- HuggingFace `all-MiniLM-L6-v2` embeddings
- ChromaDB local vector store
- Claude Haiku via Anthropic API
- PyMuPDF document extraction
- Streamlit UI

## Run

```bash
cd simple-rag
python -m venv .venv
# activate the environment
pip install -e '.[dev]'
# set ANTHROPIC_API_KEY in your environment
python -m rag_pipeline.ingest
streamlit run src/rag_pipeline/streamlit_app.py
```

Put PDF/TXT files in `data/` before ingestion. `data/` and `vectorstore/` are intentionally local and should not be committed.

## Design decisions

- **MMR retrieval** reduces duplicate chunks and increases context diversity.
- **PyMuPDFLoader** is used for more complete page extraction, including headers and footers.
- **Centralised configuration** keeps model, chunking and retrieval settings easy to change.
- **Local ChromaDB** keeps the first version reproducible without a hosted vector database.

## Roadmap

- [x] Local document ingestion
- [x] MMR retrieval
- [x] Claude grounded generation
- [x] Streamlit UI
- [ ] RAGAS evaluation
- [ ] Reranking and hybrid retrieval
- [ ] Agentic RAG with LangGraph
