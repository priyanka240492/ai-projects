"""
rag.py
Retrieval-Augmented Generation chain.
  - Retriever : ChromaDB MMR search
  - LLM       : Claude Haiku via Anthropic API
  - Chain     : LangChain LCEL (pipe operator)
"""
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from rag_pipeline.config import (
    VECTORSTORE_DIR,
    EMBED_MODEL,
    EMBED_DEVICE,
    ANTHROPIC_API_KEY,
    ANTHROPIC_MODEL,
    LLM_TEMPERATURE,
    TOP_K,
    FETCH_K,
    CHROMA_COLLECTION,
    PROMPT_TEMPLATE,
)


def load_retriever() -> object:
    """Load persisted ChromaDB and return an MMR retriever."""
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": EMBED_DEVICE},
        encode_kwargs={"normalize_embeddings": True},
    )
    vectorstore = Chroma(
        persist_directory=str(VECTORSTORE_DIR),
        embedding_function=embeddings,
        collection_name=CHROMA_COLLECTION,
    )
    # MMR: avoids returning near-duplicate chunks
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": TOP_K, "fetch_k": FETCH_K},
    )
    return retriever


def format_docs(docs: list) -> str:
    """Concatenate retrieved chunks with source metadata labels."""
    parts = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "unknown")
        page   = doc.metadata.get("page", "")
        label  = f"[{i}] {source}" + (f" p.{page}" if page != "" else "")
        parts.append(f"{label}\n{doc.page_content}")
    return "\n\n".join(parts)


def build_rag_chain(retriever) -> object:
    """Build LCEL chain: retrieve → format → prompt → LLM → parse."""
    llm = ChatAnthropic(
        model=ANTHROPIC_MODEL,
        anthropic_api_key=ANTHROPIC_API_KEY,
        temperature=LLM_TEMPERATURE,
    )
    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = (
        {
            "context":  retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def ask(question: str, chain, retriever) -> dict:
    """Run the RAG chain and return answer + deduplicated source list."""
    source_docs = retriever.invoke(question)
    answer      = chain.invoke(question)
    sources     = list({
        doc.metadata.get("source", "unknown") for doc in source_docs
    })
    return {"answer": answer, "sources": sources}
