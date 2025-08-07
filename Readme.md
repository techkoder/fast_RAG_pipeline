
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

This Hugging Face Space deploys a Retrieval-Augmented Generation (RAG) app built using LangChain, FastAPI, ChromaDB, and Google Gemini API, packaged within a Docker container.

## About


- The FastAPI app serves as the backend for your RAG system.
- ChromaDB is used as the vector store.
- LangChain manages the language model interaction.
- Google Gemini is used as the LLM backend.
- Docker is used for consistent environment deployment.
- Python 3.11 is the runtime environment.

## How to Run

Once deployed, the app listens on port **7860** as required by Hugging Face Spaces when using Docker.

Visit your Space URL to interact with the API. The FastAPI Swagger docs are accessible at:

