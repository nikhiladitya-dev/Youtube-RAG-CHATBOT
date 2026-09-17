# 🐼 PANDA CHATBOT
### Chat with Any YouTube Video using Retrieval-Augmented Generation (RAG) Implementation

<p align="left">
  Skip the Watch. Ask the Video.
</p>

---

## 📖 Overview

PANDA CHATBOT is a production-oriented Retrieval-Augmented Generation (RAG) application that allows users to interact with any YouTube video conversationally.

Instead of watching an entire video, users simply provide a YouTube URL and ask questions in natural language. The application retrieves the most relevant transcript segments and generates grounded answers using a Large Language Model while providing timestamp citations from the original video.

The project is designed using a modular architecture with FastAPI, LangChain, ChromaDB, Hugging Face models, and Streamlit.

**Retriever Evaluation:**
- Contextual Precision : 1.00
- Contextual Recall : 0.84
  
**Generator Evaluation:**
- Faithfulness : 0.86
- Answer Relevancy : 0.95

---

# ✨ Features

### YouTube Processing

- Process any supported YouTube video
- Automatically extract transcripts
- Preserve timestamps
- Store transcript locally
- Intelligent transcript chunking

---

### Semantic Search

- Recursive document chunking
- HuggingFace Embeddings
- ChromaDB Vector Database
- Persistent vector storage
- Fast semantic retrieval

---

###  Source Attribution

Every answer includes:

- Transcript citations
- Video timestamps
- Retrieved transcript chunks

This allows users to directly verify every generated response.

---

###  Modern Web Interface

- Streamlit Frontend
- Responsive layout
- Interactive chat interface
- Clean sidebar
- Video processing workflow
- Professional UI inspired by modern AI assistants

---

#  Project Architecture

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

#  Project Structure

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
git clone https://github.com/nikhiladitya-dev/Youtube-RAG-CHATBOT.git
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

# Running the Backend

```bash
python run.py
```

Backend will be available at

```
http://127.0.0.1:8000
```

---

#  Running the Frontend

```bash
streamlit run app/frontend/app.py
```

---

#  Implemented RAG Pipeline

<img width="754" height="470" alt="image" src="https://github.com/user-attachments/assets/3b8dae64-4b0d-43b3-b2db-aaeb30bea3d6" />


---

#  Current Capabilities

- Chat with any supported YouTube video

- Context-aware conversations

- History-aware retrieval

- Grounded AI responses

- Timestamp citations

- Semantic transcript search

- Modern web interface

- Modular architecture

- Production-ready backend

---

# 📈 Future Improvements

- User authentication
- Multiple video workspace
- PDF export of conversations
- Voice input
- Video's Thumbnail Preview
---

# 📸 Screenshots

- Home Screen
  
  <img width="1919" height="1032" alt="image" src="https://github.com/user-attachments/assets/d69177e4-a1b5-48f2-850e-491689669663" />

- Processing Video
  
  <img width="1919" height="918" alt="image" src="https://github.com/user-attachments/assets/1c27c739-dfd8-4c9d-9f73-c808c2d95c73" />

- Chat Interface
  
 <img width="1481" height="894" alt="image" src="https://github.com/user-attachments/assets/10a736e1-e078-4077-84c6-7b690de0d103" />
  

- Timestamp Citations
  
 <img width="1914" height="913" alt="image" src="https://github.com/user-attachments/assets/5be483f4-089a-4a40-bbc4-cbc3e2a44025" />

 - RAG Evaluation

   <img width="896" height="378" alt="Screenshot 2026-09-09 110536" src="https://github.com/user-attachments/assets/1b4bb10e-d104-42d3-98e0-afa437e27a95" />

    <img width="1295" height="377" alt="Screenshot 2026-09-10 103405" src="https://github.com/user-attachments/assets/f2c6cd66-9d34-4e9c-9faf-632261df3a09" />


---

# Outcomes

This project demonstrates practical experience with:

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Databases
- LangChain
- Large Language Models
- Prompt Engineering
- FastAPI , Streamlit
- Production Software Architecture
- REST API Design
- Frontend Integration
- Modular Python Development

---

# 🧠 Author

**Nikhil Aditya**

MTech - Software Engineering 

VIT-AP University

---

# ⭐ If you found this project useful

Consider giving this repository a ⭐ on GitHub.
