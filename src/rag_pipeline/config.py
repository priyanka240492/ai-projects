"""
config.py
Single source of truth for all pipeline settings.
All values can be overridden via environment variables or .env file.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT_DIR        = Path(__file__).resolve().parents[2]   # repo root
DATA_DIR        = ROOT_DIR / "data"
VECTORSTORE_DIR = ROOT_DIR / "vectorstore"

# ── Embeddings ───────────────────────────────────────────────────────────────
EMBED_MODEL     = "sentence-transformers/all-MiniLM-L6-v2"
EMBED_DEVICE    = "cpu"   # swap to "cuda" if GPU available

# ── Chunking ─────────────────────────────────────────────────────────────────
CHUNK_SIZE      = 500
CHUNK_OVERLAP   = 100

# ── Retrieval ────────────────────────────────────────────────────────────────
TOP_K           = 4       # chunks returned to LLM
FETCH_K         = 20      # MMR candidate pool size

# ── LLM ──────────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL   = "claude-haiku-4-5-20251001"
LLM_TEMPERATURE   = 0

# ── ChromaDB ─────────────────────────────────────────────────────────────────
CHROMA_COLLECTION = "local_rag"

# ── Prompt ───────────────────────────────────────────────────────────────────
PROMPT_TEMPLATE = """You are a helpful assistant. Use ONLY the context below to answer the question.
If the answer is not in the context, say "I don't have enough information to answer that."

Context:
{context}

Question: {question}

Answer:"""
