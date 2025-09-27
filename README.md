
---
title: LangChain FastAPI RAG App
emoji: 🦜
colorFrom: indigo
colorTo: blue
sdk: docker
sdk_version: "latest"
app_file: main.py
pinned: false
---

# LangChain FastAPI RAG App

This is a Backend For a simple Retrieval-Augmented Generation (RAG) app built using LangChain, FastAPI, ChromaDB, and Google Gemini API.

---
## ⭐️ Features

- **FastAPI backend** for high-performance APIs  
- **LangChain** for LLM workflow and chaining  
- **ChromaDB** for vector storage and retrieval  
- **Google Gemini API** as the Large Language Model backend  
- **Dockerized** for consistent deployment anywhere  
- **Auth-protected** endpoints using Bearer Tokens  
- **Async PDF/text/document support** for ingestion and question answering  
- **Automatic LLM parameter selection** based on document metadata  
- **Integrated PDF, DOCX, and email document support**

---
## ⚙️ Environment Variables

Create a `.env` file at the project root with:

- **API_AUTH_TOKEN**: Used for securing the FastAPI endpoints.
- **GOOGLE_API_KEY**: Required for Google Gemini LLM backend.
---

## How to Run
Run the following commands after cloning this repo:
- pip install -r requirements.txt
- uvicorn api.main:app --host 0.0.0.0 --port 7860

**Access the app** at `http://localhost:7860`  
FastAPI interactive docs available at `/docs` (e.g., `http://localhost:7860/docs`).

---

## 🔐 Authentication

All endpoints are secured with Bearer Token authentication:

- The API expects an `Authorization: Bearer <token>` header.
- The valid token is set via the `.env` environment variable (`API_AUTH_TOKEN`).

---

---

## 🛠️ Core Modules

- `api/main.py` — FastAPI app, batching logic, endpoint for `/hackrx/run`
- `app/models/schema.py` — Input/Output schemas using Pydantic
- `app/services/pdf_utils.py` — Async and sync PDF/DOCX/MSG text extraction, PDF metadata writing
- `app/services/rag_engine.py` — Build and configure LangChain+Chroma+Gemini RAG pipeline dynamically
- `app/services/auth.py` — Token verification for API access
- `app/services/parameter_selection.py` — Selects optimal LLM parameters based on document metadata

---

---

## 📊 Request & Response Example

### POST `/hackrx/run`
Request Header{
"Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer <Your Authorization: Bearer <token>`set in .env file>"
}

Request Body:
{
"documents": "<public PDF/DOCX/MSG/EML URL>",

"questions": [
"Summarize the document.",
"What are key findings?"
]
}

**Response:**
"answers": [
"Answer to Question 1",
"Answer to Question 2"
]
}

---
## 🧰 Utilities

- **PDF/Docx/Email extraction**: Handles various input types async and in parallel for speed.
- **Parameter Auto-tuning**: The RAG engine reads `/tmp/meta_data.txt` to adjust chunking/search dynamically for best LLM recall.
- **ChromaDB Vector Store**: Used for efficient document retrieval and similarity search embedded in the pipeline.
---

---

## 👨‍💻 Contributors

- [techkoder](https://github.com/techkoder)
- [nagarjun1302](https://github.com/nagarjun1302)

---

