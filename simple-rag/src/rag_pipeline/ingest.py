from langchain_community.document_loaders import PyMuPDFLoader, TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from rag_pipeline.config import DATA_DIR, VECTORSTORE_DIR, EMBED_MODEL, EMBED_DEVICE, CHUNK_SIZE, CHUNK_OVERLAP, CHROMA_COLLECTION


def load_documents() -> list:
    DATA_DIR.mkdir(exist_ok=True)
    docs = DirectoryLoader(str(DATA_DIR), glob='**/*.pdf', loader_cls=PyMuPDFLoader, show_progress=True).load()
    docs += DirectoryLoader(str(DATA_DIR), glob='**/*.txt', loader_cls=TextLoader, show_progress=True).load()
    return docs


def split_documents(docs: list) -> list:
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, separators=['\n\n', '\n', '.', ' ', ''])
    return splitter.split_documents(docs)


def build_vectorstore(chunks: list) -> Chroma:
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL, model_kwargs={'device': EMBED_DEVICE}, encode_kwargs={'normalize_embeddings': True})
    return Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=str(VECTORSTORE_DIR), collection_name=CHROMA_COLLECTION)


def main():
    docs = load_documents()
    if not docs:
        print('No PDF or TXT documents found in data/.')
        return
    chunks = split_documents(docs)
    build_vectorstore(chunks)
    print(f'Ingested {len(chunks)} chunks.')


if __name__ == '__main__':
    main()
