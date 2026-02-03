🧠 RAG Application with Google Gemini





A Retrieval-Augmented Generation (RAG) application built for learning and experimentation using the Google Gemini API (Free Tier) and FAISS.

The project lets you ingest PDF documents, store their embeddings locally, and chat with them using semantic search and an LLM. It’s designed to be simple, readable, and easy to extend while exploring modern RAG workflows.

✨ Key Features

📄 PDF document ingestion

🔍 Semantic search using FAISS

🤖 Context-aware responses powered by Google Gemini

⚡ Fast local vector retrieval

🧪 Built for experimentation and learning

🧩 Clean, modular project structure

🛠️ Technology Stack
Tool	Purpose

🐍 Python	Core application logic

🤖 Google Gemini API	Language model (Free Tier)

🔎 FAISS	Vector similarity search

📄 PDF Processing	Document ingestion

🔐 python-dotenv	Environment variable management

📦 Installation

1️⃣ Clone the Repository

git clone https://github.com/lavish-shrma/reg-docs.git
cd your-repo-name

2️⃣ Create a Virtual Environment
python -m venv .venv


Activate it:

Windows

.venv\Scripts\activate


Mac / Linux

source .venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

⚙️ Configuration

Get a free API key from Google AI Studio

Create a .env file in the project root:

GOOGLE_API_KEY=your_api_key_here


No billing setup is required for the Gemini free tier.

▶️ Usage
📥 Document Ingestion

Place your PDF files in:

data/raw/


Run the ingestion pipeline:

python main.py --mode ingest


This will:

Load and process all PDFs

Generate embeddings

Store vectors locally in data/vector_store/

💬 Chat with Your Documents

Start the interactive chat mode:

python main.py --mode chat


You can now ask questions about your documents and receive responses grounded in the retrieved content.

🤝 Contributing

This project is built for learning, and contributions are welcome.

If you’d like to help improve it:

Fork the repository

Create a feature branch

git checkout -b feature/your-feature


Make your changes

Commit and push

Open a Pull Request

Ideas for contributions:

Better chunking strategies

Improved prompt engineering

UI or CLI enhancements

Performance optimizations

📄 License

This project is provided for learning and educational purposes only.

No license is currently applied.
You may view and study the code, but reuse, modification, or redistribution is not permitted without explicit permission from the author.

📬 Contact

Author:

If this project helped you understand RAG systems better, consider giving it a ⭐.
