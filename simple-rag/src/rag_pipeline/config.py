"""Single source of truth for RAG settings."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / 'data'
VECTORSTORE_DIR = ROOT_DIR / 'vectorstore'
EMBED_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
EMBED_DEVICE = 'cpu'
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 4
FETCH_K = 20
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
ANTHROPIC_MODEL = 'claude-haiku-4-5-20251001'
LLM_TEMPERATURE = 0
CHROMA_COLLECTION = 'local_rag'
PROMPT_TEMPLATE = '''You are a helpful assistant. Use ONLY the context below to answer the question.\nIf the answer is not in the context, say "I don't have enough information to answer that."\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:'''
