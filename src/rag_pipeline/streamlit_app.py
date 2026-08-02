"""
streamlit_app.py
Web UI for the local RAG pipeline.

Run with:
    streamlit run src/rag_pipeline/streamlit_app.py
"""
import os
import shutil
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from rag_pipeline.config import DATA_DIR, VECTORSTORE_DIR, ANTHROPIC_MODEL
from rag_pipeline.ingest import load_documents, split_documents, build_vectorstore
from rag_pipeline.rag import load_retriever, build_rag_chain, ask

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Local RAG — Ask your documents",
    page_icon="🧠",
    layout="centered",
)

# ── Session state init ────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chain" not in st.session_state:
    st.session_state.chain = None

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "ingested" not in st.session_state:
    st.session_state.ingested = False

if "doc_count" not in st.session_state:
    st.session_state.doc_count = 0

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🧠 Local RAG")
    st.caption("LangChain · ChromaDB · Claude Haiku")
    st.divider()

    st.subheader("Upload documents")
    uploaded_files = st.file_uploader(
        "PDF or TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded_files:
        if st.button("Ingest documents", use_container_width=True, type="primary"):
            # Save uploaded files to data/
            DATA_DIR.mkdir(exist_ok=True)

            # Clear old vectorstore for fresh ingestion
            if VECTORSTORE_DIR.exists():
                shutil.rmtree(VECTORSTORE_DIR)

            with st.spinner("Saving files..."):
                for f in uploaded_files:
                    dest = DATA_DIR / f.name
                    dest.write_bytes(f.read())

            with st.spinner("Loading and chunking documents..."):
                docs = load_documents()
                chunks = split_documents(docs)

            with st.spinner("Embedding and storing in ChromaDB..."):
                build_vectorstore(chunks)

            with st.spinner("Loading retriever and RAG chain..."):
                retriever = load_retriever()
                chain = build_rag_chain(retriever)
                st.session_state.retriever = retriever
                st.session_state.chain = chain
                st.session_state.ingested = True
                st.session_state.doc_count = len(uploaded_files)
                st.session_state.chunk_count = len(chunks)
                st.session_state.messages = []   # clear chat on new ingest

            st.success(f"Ingested {len(chunks)} chunks from {len(uploaded_files)} file(s)")

    st.divider()

    # Stats
    col1, col2 = st.columns(2)
    col1.metric("Documents", st.session_state.doc_count)
    col2.metric("Chunks", st.session_state.chunk_count)

    st.caption(f"Model: `{ANTHROPIC_MODEL}`")

    if st.session_state.ingested:
        st.success("● Ready to query")
    else:
        st.warning("● Upload and ingest documents first")

    st.divider()
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ── Main chat area ────────────────────────────────────────────────────────────
st.title("Ask your documents")

if not st.session_state.ingested:
    st.info("Upload your PDF or TXT files in the sidebar and click **Ingest documents** to get started.")
    st.stop()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            st.caption(f"📄 Sources: {', '.join(msg['sources'])}")

# Chat input
if question := st.chat_input("Ask a question about your documents..."):
    # Show user message
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = ask(question, st.session_state.chain, st.session_state.retriever)
        st.markdown(result["answer"])
        st.caption(f"📄 Sources: {', '.join(result['sources'])}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result["sources"],
    })
