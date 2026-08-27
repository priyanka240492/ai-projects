from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from rag_pipeline.config import VECTORSTORE_DIR, EMBED_MODEL, EMBED_DEVICE, ANTHROPIC_API_KEY, ANTHROPIC_MODEL, LLM_TEMPERATURE, TOP_K, FETCH_K, CHROMA_COLLECTION, PROMPT_TEMPLATE


def load_retriever():
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL, model_kwargs={'device': EMBED_DEVICE}, encode_kwargs={'normalize_embeddings': True})
    vectorstore = Chroma(persist_directory=str(VECTORSTORE_DIR), embedding_function=embeddings, collection_name=CHROMA_COLLECTION)
    return vectorstore.as_retriever(search_type='mmr', search_kwargs={'k': TOP_K, 'fetch_k': FETCH_K})


def format_docs(docs: list) -> str:
    parts = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get('source', 'unknown')
        page = doc.metadata.get('page', '')
        label = f'[{i}] {source}' + (f' p.{page}' if page != '' else '')
        parts.append(f'{label}\n{doc.page_content}')
    return '\n\n'.join(parts)


def build_rag_chain(retriever):
    llm = ChatAnthropic(model=ANTHROPIC_MODEL, anthropic_api_key=ANTHROPIC_API_KEY, temperature=LLM_TEMPERATURE)
    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    return ({'context': retriever | format_docs, 'question': RunnablePassthrough()} | prompt | llm | StrOutputParser())


def ask(question: str, chain, retriever) -> dict:
    source_docs = retriever.invoke(question)
    answer = chain.invoke(question)
    sources = list({doc.metadata.get('source', 'unknown') for doc in source_docs})
    return {'answer': answer, 'sources': sources}
