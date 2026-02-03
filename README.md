## **📌 Project Overview: RAG-Based Chatbot with MongoDB Vector Search**

This project implements a Retrieval-Augmented Generation (RAG) chatbot that enables users to interact with PDF documents using natural language. The system is designed to ingest documents, convert them into searchable vector representations, retrieve the most relevant content, and generate accurate responses using an open-source language model.

The architecture follows a modular and production-oriented RAG pipeline, combining open-source tools and scalable cloud infrastructure.

**🧩 Document Ingestion & Processing**

PDF documents are ingested and processed using Generative AI-based document loaders.

The extracted text is cleaned and split into smaller, meaningful chunks to improve retrieval accuracy and reduce context overload.

Chunking ensures that each text segment retains semantic meaning while remaining suitable for embedding.

**🔢 Embedding Generation**

Each text chunk is converted into vector embeddings using a Sentence Transformers model from Hugging Face.

These embeddings capture the semantic meaning of the text, enabling similarity-based search rather than keyword matching.

The embedding process is optimized to ensure efficient storage and fast retrieval.

**🧠 Vector Storage with MongoDB Atlas**

MongoDB Atlas Vector Search is used as the vector database.

All generated embeddings are stored in MongoDB as vectors alongside their corresponding metadata.

MongoDB Atlas provides scalability, reliability, and fast similarity search using vector indexes.

**🔍 Retrieval Mechanism**

A text-based retriever is implemented to query the vector store.

When a user submits a question, the query is embedded and compared against stored vectors.

The retriever fetches the most relevant document chunks based on semantic similarity.

**🤖 Language Model (LLM)**

The system uses Ollama, an open-source local LLM, to generate responses.

Retrieved document chunks are passed as context to the LLM.

The model generates accurate, context-aware answers grounded strictly in the retrieved data, reducing hallucinations.

**🔗 RAG Orchestration with LangChain**

LangChain is used to orchestrate the complete RAG workflow:

Document loading

Text chunking

Embedding generation

Vector storage and retrieval

Prompt construction and response generation

LangChain enables a clean, modular, and extensible architecture suitable for future scaling and production use.

**🖥️ Frontend Interface**

A Streamlit-based frontend is used to provide a simple and interactive chat interface.

Users can upload PDFs and ask questions in real time.

Responses from the RAG pipeline are displayed in a conversational chatbot format.

**🚀 Key Features**

PDF-based conversational AI

Semantic search using vector embeddings

MongoDB Atlas Vector Search integration

Open-source LLM (Ollama)

Modular RAG pipeline using LangChain

Interactive Streamlit UI

**🏗️ Use Cases**

Document-based Q&A systems

Knowledge assistants for internal documents

Research paper analysis

Enterprise chatbot solutions
