import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

RAW_DOCS_PATH = "data/raw"
VECTOR_STORE_PATH = "data/vector_store"


def load_documents():
    documents = []

    for file in os.listdir(RAW_DOCS_PATH):
        path = os.path.join(RAW_DOCS_PATH, file)

        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
            documents.extend(loader.load())

        elif file.endswith(".txt"):
            loader = TextLoader(path)
            documents.extend(loader.load())

    return documents


def ingest():
    print("Starting ingestion...")

    docs = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(docs)
    print(f"Loaded {len(chunks)} chunks")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004"
    )

    import time
    
    # Process in batches to avoid rate limits
    batch_size = 10
    vectorstore = None
    
    print(f"Processing {len(chunks)} chunks in batches of {batch_size}...")
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"Embedding batch {i//batch_size + 1}/{(len(chunks) + batch_size - 1)//batch_size}...")
        
        if vectorstore is None:
            vectorstore = FAISS.from_documents(batch, embeddings)
        else:
            vectorstore.add_documents(batch)
            
        time.sleep(2)  # Wait 2 seconds between batches to respect rate limits

    if vectorstore:
        vectorstore.save_local(VECTOR_STORE_PATH)
        print("Ingestion complete. Vector store created.")
    else:
        print("No documents found to ingest.")


if __name__ == "__main__":
    ingest()
