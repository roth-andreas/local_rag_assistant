import os
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import chromadb

DB_PATH = "db"

def get_vectorstore(model_name="BAAI/bge-small-en-v1.5"):
    embeddings = FastEmbedEmbeddings(model_name=model_name)
    
    chroma_host = os.getenv("CHROMA_HOST")
    chroma_port = os.getenv("CHROMA_PORT")

    if chroma_host and chroma_port:
        client = chromadb.HttpClient(host=chroma_host, port=int(chroma_port))
        vectorstore = Chroma(
            client=client,
            collection_name="rag_collection",
            embedding_function=embeddings,
        )
    else:
        vectorstore = Chroma(
            persist_directory=DB_PATH, 
            embedding_function=embeddings,
            collection_name="rag_collection"
        )
    return vectorstore

def ingest_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024, chunk_overlap=100, length_function=len, is_separator_regex=False
    )
    chunks = text_splitter.split_documents(pages)

    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)
    return len(chunks)

def query_rag(question):
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    llm = ChatOllama(model="llama3", temperature=0, base_url=base_url)

    docs = retriever.invoke(question)
    context_text = "\n\n".join([doc.page_content for doc in docs])

    prompt_template = ChatPromptTemplate.from_template("""
    Answer the question based ONLY on the following context:
    {context}

    Question: {question}
    """)

    prompt = prompt_template.format(context=context_text, question=question)

    response = llm.invoke(prompt)
    return response.content, docs

