import shutil
import streamlit as st
from rag_pipeline.config import DATA_DIR, VECTORSTORE_DIR, ANTHROPIC_MODEL
from rag_pipeline.ingest import load_documents, split_documents, build_vectorstore
from rag_pipeline.rag import load_retriever, build_rag_chain, ask

st.set_page_config(page_title='Local RAG', page_icon='🧠')
st.title('🧠 Local RAG')

if 'messages' not in st.session_state: st.session_state.messages = []
if 'ingested' not in st.session_state: st.session_state.ingested = False

with st.sidebar:
    st.subheader('Documents')
    files = st.file_uploader('PDF or TXT', type=['pdf', 'txt'], accept_multiple_files=True)
    if files and st.button('Ingest documents', type='primary'):
        DATA_DIR.mkdir(exist_ok=True)
        if VECTORSTORE_DIR.exists(): shutil.rmtree(VECTORSTORE_DIR)
        for f in files: (DATA_DIR / f.name).write_bytes(f.read())
        chunks = split_documents(load_documents())
        build_vectorstore(chunks)
        st.session_state.retriever = load_retriever()
        st.session_state.chain = build_rag_chain(st.session_state.retriever)
        st.session_state.ingested = True
        st.session_state.messages = []
        st.success(f'Ingested {len(chunks)} chunks')
    st.caption(f'Model: {ANTHROPIC_MODEL}')

if not st.session_state.ingested:
    st.info('Upload documents and ingest them from the sidebar.')
    st.stop()

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        if message.get('sources'): st.caption('Sources: ' + ', '.join(message['sources']))

if question := st.chat_input('Ask about your documents...'):
    st.session_state.messages.append({'role': 'user', 'content': question})
    with st.chat_message('user'): st.markdown(question)
    with st.chat_message('assistant'):
        result = ask(question, st.session_state.chain, st.session_state.retriever)
        st.markdown(result['answer'])
        st.caption('Sources: ' + ', '.join(result['sources']))
    st.session_state.messages.append({'role': 'assistant', 'content': result['answer'], 'sources': result['sources']})
