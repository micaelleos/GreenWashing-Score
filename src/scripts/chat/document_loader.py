# This peace of code load the files in directory to the database
import os
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import chromadb
from langchain_core.tools import tool
import shutil
import chromadb 
import uuid
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryByteStore
from langchain_core.documents import Document

UPLOAD_DIR = "data/stage/"
PROCESSED_DOC = "data/processed/"
PERSIST_DIR="data/"

OPENAI_API_KEY=os.getenv('OPEN_API_KEY')

def retrieve_sections():
    db = vector_store()
    retriever = db.as_retriever()
    result = retriever.vectorstore.get(where={"type": {"$eq": 'parent'}})
    docs=[]
    for i,id in enumerate(result['ids']):
        if len(result['documents'][i]) > 500:
            docs.append({'ids':id,'documents':result['documents'][i],"metadatas":result['metadatas'][i]})
    return docs

def retrieve_sections_page(initial_page:int,final_page:int):
    db = vector_store()
    retriever = db.as_retriever()
    result = retriever.vectorstore.get(where={"type": {"$eq": 'parent'}})
    docs=[]
    for i,id in enumerate(result['ids']):
        if int(result['metadatas'][i]['page']) <= final_page and int(result['metadatas'][i]['page']) >= initial_page:
            if len(result['documents'][i]) > 500:
                docs.append({'ids':id,'documents':result['documents'][i],"metadatas":result['metadatas'][i]})
    return docs

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
    print("Quantidade de chunks:",len(doc_splits))
    arquivos = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith('.pdf')]
    for arquivo in arquivos:
        shutil.move(UPLOAD_DIR+arquivo, PROCESSED_DOC+arquivo)

    return doc_splits

def doc_spliters_family(diretorio):
        # Load PDF
    loaders = loaders = [PyPDFLoader(UPLOAD_DIR+arquivo) for arquivo in os.listdir(diretorio) if arquivo.endswith('.pdf')]
    docs = []

    for loader in loaders:
        docs.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=2000, chunk_overlap=300
    )

    doc_splits = text_splitter.split_documents(docs)
    id_key = "doc_id"
   
    child_text_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

    sub_docs = []
    for doc in doc_splits:
        id = str(uuid.uuid4())
        doc.metadata[id_key] = id
        doc.metadata["type"] = "parent"
        _sub_docs = child_text_splitter.split_documents([doc])
        for _doc in _sub_docs:
            _doc.metadata[id_key] = id
            _doc.metadata["type"] = "child"
        sub_docs.extend(_sub_docs)

    return doc_splits, sub_docs


def family_db_retriever():
        # The storage layer for the parent documents
    store = InMemoryByteStore()
    id_key = "doc_id"
    vectorstore = vector_store()
    # The retriever (empty to start)
    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        byte_store=store,
        id_key=id_key,
    )  
    return retriever

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

def load_doc_family_to_db(doc_splits, sub_docs):
    db = vector_store()
    db.add_documents(doc_splits)
    db.add_documents(sub_docs)

def load_doc_family_pipeline():
    doc_splits, sub_docs = doc_spliters_family(UPLOAD_DIR)
    load_doc_family_to_db(doc_splits, sub_docs)


def vector_store():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)
    persistent_client = chromadb.PersistentClient(path=PERSIST_DIR)
    vectorstore = Chroma(client=persistent_client,
                                    collection_name="rag-chroma",
                                    embedding_function=embeddings,
                                    )
    return vectorstore


def format_doc(doc_list):
    docs=[]
    for doc in doc_list:
        document = Document(
            page_content=doc['documents'][0],
            metadata=doc['metadatas'][0]
        )
        docs.append(document)
    return docs

@tool(response_format="content_and_artifact")
def custom_retriver(query: str):
    """Retrieve information related to a query."""
    db = vector_store()
    retriever = db.as_retriever()
    child_docs = retriever.vectorstore.max_marginal_relevance_search(query, k=14,fetch_k=5,filter={'type':'child'})

    doc_id = []
    for doc in child_docs:
        if doc.metadata['doc_id'] not in doc_id:
            doc_id.append(doc.metadata['doc_id'])

    docs = []
    for id in doc_id:
        docs.append(retriever.vectorstore.get(where={"$and": [{"doc_id": {"$eq":f"{id}" }},{"type": {"$eq": 'parent'}}]}))
    
    formated_docs = format_doc(docs)

    serialized = "\n\n".join(
        (f"Termo de pesquisa: {query} Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in formated_docs
    )
    return serialized, formated_docs

@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    vectorstore = vector_store()
    retrieved_docs = vectorstore.similarity_search(query, k=24)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    print(len(serialized), len(retrieved_docs))
    print(serialized, retrieved_docs)
    return serialized, retrieved_docs

@tool(response_format="content_and_artifact")
def retrieve_family(query: str):
    """Retrieve information related to a query."""
    retriever = family_db_retriever()
    retrieved_docs = retriever.vectorstore.similarity_search(query, k=8)
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


tools = [custom_retriver]#[retrieve]

if __name__ == "__main__":
    print(retriever("IN441"))

    