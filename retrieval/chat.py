import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

VECTOR_STORE_PATH = "data/vector_store"

def start_chat():
    print("Initializing chat system...")
    
    if not os.path.exists(VECTOR_STORE_PATH):
        print("Vector store not found. Please run ingestion first.")
        return

    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    try:
        vectorstore = FAISS.load_local(
            VECTOR_STORE_PATH, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        print(f"Error loading vector store: {e}")
        return

    full_retriever = vectorstore.as_retriever()

    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(full_retriever, document_chain)

    print("\nChat system ready! Type 'exit' to quit.\n")

    while True:
        try:
            query = input("You: ")
            if query.lower() in ["exit", "quit", "q"]:
                break
            
            if not query.strip():
                continue

            response = retrieval_chain.invoke({"input": query})
            print(f"Bot: {response['answer']}\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    start_chat()
