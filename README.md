# RAG Application with Google Gemini

A Retrieval-Augmented Generation (RAG) system using Google Gemini API (Free Tier) and FAISS.

## Setup

1.  **Clone the repository** (if you haven't already).
2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate  # Windows
    # source .venv/bin/activate  # Mac/Linux
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your `.env` file**:
    -   Get a free API key from [Google AI Studio](https://aistudio.google.com/).
    -   Create a `.env` file in the root directory:
        ```
        GOOGLE_API_KEY=your_api_key_here
        ```

## Usage

### 1. Ingestion
Put your PDF files in the `data/raw` folder. Then run:
```bash
python main.py --mode ingest
```
This will process the documents and create a vector store in `data/vector_store`.

### 2. Chat
Start the retrieval chat:
```bash
python main.py --mode chat
```
Ask questions about your documents!
