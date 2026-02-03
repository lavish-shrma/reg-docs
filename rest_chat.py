import os
import requests
import json
import time
from typing import List, Optional, Any
from dotenv import load_dotenv

# Import only safe langchain components
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.embeddings import Embeddings

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
VECTOR_STORE_PATH = "data/vector_store"

class RestGeminiEmbeddings(Embeddings):
    def __init__(self, model="models/text-embedding-004"):
        self.model = model
        self.api_key = API_KEY
        self.url = f"https://generativelanguage.googleapis.com/v1beta/{model}:embedContent?key={self.api_key}"

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        print(f"Embedding {len(texts)} texts...")
        for text in texts:
            embeddings.append(self.embed_query(text))
            time.sleep(1) # Rate limit help
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        payload = {
            "model": self.model,
            "content": {"parts": [{"text": text}]}
        }
        response = requests.post(self.url, json=payload)
        if response.status_code != 200:
            raise Exception(f"Embedding failed: {response.text}")
        return response.json()['embedding']['values']

class RestGeminiChat(BaseChatModel):
    model_name: str = "gemini-flash-latest"
    api_key: str = API_KEY

    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs: Any) -> ChatResult:
        # Convert messages to Gemini format
        gemini_messages = []
        for m in messages:
            role = "user" if isinstance(m, HumanMessage) else "model"
            gemini_messages.append({
                "role": role,
                "parts": [{"text": m.content}]
            })
        
        # Add system instruction if needed or just send the last message content if simplified
        # For simple RAG, we can just take the last message which usually contains the prompt with context
        prompt_text = messages[-1].content
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt_text}]}]
        }
        
        print("Sending request to Gemini (REST)...")
        response = requests.post(url, json=payload)
        
        if response.status_code != 200:
             raise Exception(f"Chat failed: {response.text}")
        
        try:
            candidates = response.json()['candidates']
            if not candidates:
                content = "No response generated."
            else:
                content = candidates[0]['content']['parts'][0]['text']
        except Exception as e:
            content = f"Error parsing response: {response.text}"

        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])

    @property
    def _llm_type(self) -> str:
        return "gemini-rest"

def run_rest_rag():
    print("Initializing REST-based RAG...")
    
    if not os.path.exists(VECTOR_STORE_PATH):
        print("Vector store not found. Please ingest first.")
        return

    print("Loading Embeddings...")
    embeddings = RestGeminiEmbeddings()
    
    try:
        print("Loading FAISS...")
        vectorstore = FAISS.load_local(
            VECTOR_STORE_PATH, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        print("FAISS loaded.")
    except Exception as e:
        print(f"Error loading FAISS: {e}")
        return

    print("Init LLM...")
    llm = RestGeminiChat()

    print("Creating Chain...")
    prompt = ChatPromptTemplate.from_template("""Answer the question based only on:
{context}

Question: {input}""")

    chain = create_retrieval_chain(
        vectorstore.as_retriever(),
        create_stuff_documents_chain(llm, prompt)
    )
    print("Chain created.")

    print("\nChat Ready! (Type 'exit' to quit)")
    while True:
        try:
            q = input("You: ")
            if q.lower() in ['exit', 'quit']: break
            res = chain.invoke({"input": q})
            print(f"Bot: {res['answer']}\n")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_rest_rag()
