"""
ingest.py
Load documents from data/, chunk them, embed with HuggingFace,
and persist to a local ChromaDB vector store.

Usage:
    python -m rag_pipeline.ingest        # via module
    rag-ingest                           # via installed CLI (pyproject.toml)
"""
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    DirectoryLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from rag_pipeline.config import (
    DATA_DIR,
    VECTORSTORE_DIR,
    EMBED_MODEL,
    EMBED_DEVICE,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    CHROMA_COLLECTION,
)


def load_documents() -> list:
    """Load all PDFs and TXT files from DATA_DIR."""
    DATA_DIR.mkdir(exist_ok=True)
    docs = []
    docs.extend(
        DirectoryLoader(
            str(DATA_DIR), glob="**/*.pdf",
            loader_cls=PyPDFLoader, show_progress=True
        ).load()
    )
    docs.extend(
        DirectoryLoader(
            str(DATA_DIR), glob="**/*.txt",
            loader_cls=TextLoader, show_progress=True
        ).load()
    )
    print(f"[ingest] Loaded {len(docs)} pages from {DATA_DIR}")
    return docs


def split_documents(docs: list) -> list:
    """Split documents into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"[ingest] Split into {len(chunks)} chunks "
          f"(size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    return chunks


def build_vectorstore(chunks: list) -> Chroma:
    """Embed chunks and persist to ChromaDB."""
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": EMBED_DEVICE},
        encode_kwargs={"normalize_embeddings": True},
    )
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTORSTORE_DIR),
        collection_name=CHROMA_COLLECTION,
    )
    print(f"[ingest] Vector store persisted at: {VECTORSTORE_DIR}")
    return vectorstore


def main():
    docs = load_documents()
    if not docs:
        print("[ingest] No documents found — add PDF or TXT files to data/")
        return
    chunks = split_documents(docs)
    build_vectorstore(chunks)
    print("[ingest] Ingestion complete. Run 'rag-chat' to start querying.")


if __name__ == "__main__":
    main()
