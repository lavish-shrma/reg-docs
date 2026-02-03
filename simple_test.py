import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()
print("1. Environment loaded.")

VECTOR_STORE_PATH = "data/vector_store"

def test_rag():
    print(f"2. Checking vector store at {VECTOR_STORE_PATH}...")
    if not os.path.exists(VECTOR_STORE_PATH):
        print("   [ERROR] Vector store not found!")
        return

    print("3. Loading Embeddings (models/text-embedding-004)...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    print("4. Loading Vector Store...")
    try:
        vectorstore = FAISS.load_local(
            VECTOR_STORE_PATH, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        print("   [SUCCESS] Vector store loaded.")
    except Exception as e:
        print(f"   [ERROR] Failed to load vector store: {e}")
        return

    print("5. Initializing LLM (gemini-flash-latest)...")
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0
    )

    print("6. Creating Retrieval Chain...")
    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vectorstore.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    query = "What is in the test document?"
    print(f"7. Running Query: '{query}'")
    print("   ... Waiting for response (this might take 10-20s if rate limited) ...")
    
    try:
        response = retrieval_chain.invoke({"input": query})
        print("\n" + "="*30)
        print(f"RESPONSE:\n{response['answer']}")
        print("="*30 + "\n")
    except Exception as e:
        print(f"   [ERROR] Query failed: {e}")

if __name__ == "__main__":
    try:
        test_rag()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
