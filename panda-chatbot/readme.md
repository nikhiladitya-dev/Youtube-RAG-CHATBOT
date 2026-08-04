# 🐼 PANDA CHATBOT
### Chat with Any YouTube Video using Retrieval-Augmented Generation (RAG)

<p align="center">
  <strong>Skip the Watch. Ask the Video.</strong>
</p>

---

## 📖 Overview

PANDA CHATBOT is a production-oriented Retrieval-Augmented Generation (RAG) application that allows users to interact with any YouTube video conversationally.

Instead of watching an entire video, users simply provide a YouTube URL and ask questions in natural language. The application retrieves the most relevant transcript segments and generates grounded answers using a Large Language Model while providing timestamp citations from the original video.

The project is designed using a modular architecture with FastAPI, LangChain, ChromaDB, Hugging Face models, and Streamlit.

---

# ✨ Features

### 🎥 YouTube Processing

- Process any supported YouTube video
- Automatically extract transcripts
- Preserve timestamps
- Store transcript locally
- Intelligent transcript chunking

---

### 🧠 Semantic Search

- Recursive document chunking
- HuggingFace Embeddings
- ChromaDB Vector Database
- Persistent vector storage
- Fast semantic retrieval

---

### 🤖 Retrieval-Augmented Generation (RAG)

- Context-aware retrieval
- MMR (Max Marginal Relevance) Search
- Multi-turn conversation support
- History-aware question rewriting
- Grounded responses only
- Hallucination prevention

---

### 📍 Source Attribution

Every answer includes:

- Transcript citations
- Video timestamps
- Retrieved transcript chunks

This allows users to directly verify every generated response.

---

### 💻 Modern Web Interface

- Streamlit Frontend
- Responsive layout
- Interactive chat interface
- Clean sidebar
- Video processing workflow
- Professional UI inspired by modern AI assistants

---

# 🏗️ Project Architecture

```
User
   │
   ▼
Streamlit Frontend
   │
   ▼
FastAPI Backend
   │
   ▼
Chat Service
   │
   ▼
History Aware Retrieval
   │
   ▼
MMR Retriever
   │
   ▼
Chroma Vector Database
   │
   ▼
Transcript Chunks
   │
   ▼
Large Language Model
```

---

# ⚙️ Tech Stack

## Backend

- FastAPI
- LangChain
- ChromaDB
- Hugging Face Inference API

## Frontend

- Streamlit

## Embeddings

- BAAI/bge-small-en-v1.5

## Language Model

- Qwen2.5-7B-Instruct

## Transcript Extraction

- youtube-transcript-api

## Vector Database

- ChromaDB

---

# 📂 Project Structure

```
youtube-rag-chatbot/

│
├── app/
│   ├── api/
│   ├── chains/
│   ├── core/
│   ├── frontend/
│   ├── models/
│   ├── prompts/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── data/
│   ├── transcripts/
│   ├── vector_db/
│   └── cache/
│
├── tests/
│
├── requirements.txt
├── run.py
└── README.md
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/youtube-rag-chatbot.git
```

Navigate into the project

```bash
cd youtube-rag-chatbot
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file

```env
HUGGINGFACEHUB_API_TOKEN=YOUR_API_KEY
```

---

# ▶️ Running the Backend

```bash
python run.py
```

Backend will be available at

```
http://127.0.0.1:8000
```

---

# ▶️ Running the Frontend

```bash
streamlit run app/frontend/app.py
```

---

# 🧩 Implemented RAG Pipeline

✅ Transcript Extraction

↓

✅ Document Creation

↓

✅ Recursive Text Splitting

↓

✅ Embedding Generation

↓

✅ ChromaDB Indexing

↓

✅ Semantic Search

↓

✅ MMR Retrieval

↓

✅ History-aware Query Rewriting

↓

✅ Retrieval-Augmented Generation

↓

✅ Timestamp Citations

↓

✅ Interactive Chat UI

---

# 🎯 Current Capabilities

✔ Chat with any supported YouTube video

✔ Context-aware conversations

✔ History-aware retrieval

✔ Grounded AI responses

✔ Timestamp citations

✔ Semantic transcript search

✔ Modern web interface

✔ Modular architecture

✔ Production-ready backend

---

# 📈 Future Improvements

- User authentication
- Multiple video workspace
- PDF export of conversations
- Streaming responses
- Voice input
- Multi-language support
- Docker deployment
- Cloud deployment
- Conversation history persistence
- Video thumbnail previews
- Source highlighting inside transcript

---

# 📸 Screenshots

> Add screenshots of your application here.

Examples:

- Home Screen
- Processing Video
- Chat Interface
- Timestamp Citations

---

# 🎓 Learning Outcomes

This project demonstrates practical experience with:

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Databases
- LangChain
- Large Language Models
- Prompt Engineering
- FastAPI
- Streamlit
- Production Software Architecture
- REST API Design
- Frontend Integration
- Modular Python Development

---

# 👨‍💻 Author

**Nikhil Aditya**

B.Tech Computer Science Engineering

VIT-AP University

---

# ⭐ If you found this project useful

Consider giving this repository a ⭐ on GitHub.