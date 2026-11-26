# 🎓 ScholarRAG: College Presentation & Viva Guide

Use this guide to confidently explain your project to your professor, internal faculty, or external viva examiners.

---

## 1. The 30-Second Elevator Pitch (Start with this!)

> *"Good morning Sir/Ma'am. My project is **ScholarRAG**, an AI-powered Multi-PDF Question-Answering system based on **Retrieval-Augmented Generation (RAG)**.*
>
> *Standard LLMs like ChatGPT often hallucinate or don't have access to private course material or enterprise documents. In this project, users can upload multiple large PDFs simultaneously, and ask natural language questions. Instead of dumping full documents into the AI, our system extracts the text, breaks it down into semantic chunks, indexes them in a local **FAISS vector database**, and retrieves only the most relevant passages to feed into **Google Gemini** for factually grounded, verifiable answers."*

---

## 2. Tech Stack Breakdown (When asked: "What did you use?")

| Layer | Technology | Why We Used It |
| :--- | :--- | :--- |
| **Frontend / UI** | **Streamlit** | Rapid development of interactive web applications, chat state, and theme switching. |
| **PDF Extraction** | **PyPDF2** | Reads raw text and page metadata from arbitrary PDF documents. |
| **Chunking Engine** | **LangChain Text Splitters** (`RecursiveCharacterTextSplitter`) | Splits long document text into manageable snippets with overlap to preserve cross-boundary context. |
| **Embeddings** | **Google Gemini Embeddings** (`gemini-embedding-001`) | Converts textual meaning into 3072-dimensional semantic vector arrays. |
| **Vector Store** | **FAISS (Facebook AI Similarity Search)** | Ultra-fast local vector similarity indexing and nearest-neighbor search without needing an external cloud DB. |
| **LLM Reasoning** | **Google Gemini** (`gemini-3.6-flash`, `gemini-3.7-flash`) | Generates concise, grounded answers based strictly on the retrieved context. |
| **Framework Glue** | **LangChain** | Chains document loaders, prompt templates, vector retrievers, and LLMs into a seamless pipeline. |

---

## 3. Step-by-Step Architecture (When asked: "How did you build it?")

Explain the architecture in **5 logical stages**:

1. **Document Ingestion & Text Parsing:**
   * PyPDF2 processes uploaded PDF files page by page, handling corrupt files gracefully.
2. **Recursive Semantic Chunking:**
   * Document text is split into chunks of ~2000 characters with 300 character overlap so key sentences spanning chunk boundaries aren't lost.
3. **Batch Vector Embedding & Rate Limiting:**
   * Text chunks are converted to mathematical vectors via `gemini-embedding-001`.
   * To prevent API quota exhaustion (429 errors), we implemented a batching mechanism with exponential backoff retries.
4. **Local Vector Storage in FAISS:**
   * Vector embeddings are indexed locally in memory and serialized to disk (`./faiss_index/`), eliminating recurring cloud database costs.
5. **Contextual Retrieval & Generation:**
   * When a question is asked, it is vectorized and compared against all indexed chunks using similarity search.
   * Top-K chunks are injected into a strict system prompt that instructs Gemini to only use provided facts and prevent hallucinations.

---

## 4. Key Questions Examiners Love to Ask (and How to Answer)

### Q1: "Why RAG? Why not just fine-tune an LLM or use ChatGPT directly?"
> **Answer:** *"Fine-tuning is expensive, requires powerful GPUs, and must be retrained every time documents change. Furthermore, standard ChatGPT doesn't have our internal documents. RAG allows real-time dynamic querying over brand-new documents with zero retraining cost, and completely prevents hallucination by grounding responses in cited source text."*

### Q2: "What is the purpose of 'Chunk Overlap'?"
> **Answer:** *"If a critical sentence or definition gets split right down the middle between Chunk A and Chunk B, a semantic search might miss it. Chunk overlap ensures continuous contextual continuity across chunk borders."*

### Q3: "Why did you choose FAISS over cloud databases like Pinecone or ChromaDB?"
> **Answer:** *"FAISS runs completely in-memory on the local host with zero recurring subscription fees, minimal latency, and full data privacy since document vectors never leave the local environment."*

### Q4: "What extra features did you add to improve on basic tutorials?"
> **Answer:**
> 1. Multi-turn conversational chat memory with exportable chat logs.
> 2. Source citation verification: users can expand and inspect the exact PDF chunks used to generate the answer.
> 3. Dynamic RAG parameters: live sliders for chunk size, overlap, top-K, and temperature.
> 4. Automated rate-limit handling with exponential backoff.
> 5. Responsive Dark & Light UI modes.
