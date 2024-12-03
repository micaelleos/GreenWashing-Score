# This peace of code load the files in directory to the database
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import chromadb
from langchain_core.tools import tool
import shutil
import chromadb 


UPLOAD_DIR = "data/stage/"
PROCESSED_DOC = "data/processed/"
PERSIST_DIR="./../../../data/"

OPENAI_API_KEY=os.getenv('OPEN_API_KEY')

def save_uploadedfile(uploadedfile):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    with open(os.path.join(UPLOAD_DIR, uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())

def doc_spliters(diretorio):
    # Load PDF
    loaders = [PyPDFLoader(UPLOAD_DIR+arquivo) for arquivo in os.listdir(diretorio) if arquivo.endswith('.pdf')]
    docs = []

    for loader in loaders:
        docs.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=2000, chunk_overlap=300
    )

    doc_splits = text_splitter.split_documents(docs)
    
    arquivos = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith('.pdf')]
    for arquivo in arquivos:
        shutil.move(UPLOAD_DIR+arquivo, PROCESSED_DOC+arquivo)

    return doc_splits


def load_doc_to_db(doc_splits):
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large",api_key=OPENAI_API_KEY)
    db = vector_store()
    
    # Add to vectorDB
    db.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )

def load_doc_pipeline():
    doc_splits = doc_spliters(UPLOAD_DIR)
    load_doc_to_db(doc_splits)

def vector_store():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)
    persistent_client = chromadb.PersistentClient(path=PERSIST_DIR)
    vectorstore = Chroma(client=persistent_client,
                                    collection_name="rag-chroma",
                                    embedding_function=embeddings,
                                    )
    return vectorstore


@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    vectorstore = vector_store()
    retrieved_docs = vectorstore.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

def retriever(query: str):
    """Retrieve information related to a query."""
    vectorstore = vector_store()
    retrieved_docs = vectorstore.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs



tools = [retrieve]

if __name__ == "__main__":
    print(retriever("IN441"))

    