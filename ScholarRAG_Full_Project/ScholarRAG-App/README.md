# 📚 ScholarRAG — AI-Powered Multi-PDF RAG Assistant

> An intelligent document question-answering application that allows users to upload multiple PDF files and ask natural-language questions based on their content using Retrieval-Augmented Generation (RAG).

---

## 🚀 Project Overview

**ScholarRAG** is an AI-powered Multi-PDF Question Answering application developed using **Python, Streamlit, LangChain, Google Gemini, Gemini Embeddings, and FAISS**.

The application implements a **Retrieval-Augmented Generation (RAG)** pipeline that enables users to interact with multiple PDF documents through natural-language questions.

Instead of sending the entire PDF content directly to the Large Language Model (LLM), the application:

1. Extracts text from uploaded PDF files.
2. Splits the extracted text into smaller, meaningful chunks.
3. Converts those chunks into numerical vector representations using Gemini Embeddings.
4. Stores the vectors in a FAISS vector index.
5. Converts the user's question into an embedding.
6. Retrieves the most relevant document chunks using similarity search.
7. Provides the retrieved context to Google Gemini.
8. Generates an answer based only on the retrieved PDF content.

This approach helps reduce irrelevant information and enables the LLM to provide context-aware responses from user-provided documents.

---

## 🎯 Objectives

The primary objectives of this project are:

- Build a practical **Retrieval-Augmented Generation (RAG)** application.
- Understand the complete RAG pipeline from document ingestion to answer generation.
- Enable users to interact with multiple PDF documents using natural language.
- Implement semantic search using vector embeddings.
- Use FAISS for efficient similarity-based document retrieval.
- Use Google Gemini as the Large Language Model.
- Develop an interactive user interface using Streamlit.
- Gain hands-on experience with modern LangChain components.

---

## ✨ Key Features

### 📄 Multiple PDF Upload

Users can upload multiple PDF files simultaneously.

### 🔍 Semantic Document Search

The application does not rely only on keyword matching. It converts documents and questions into vector embeddings and retrieves semantically relevant content.

### 🤖 Gemini-Powered Answers

Google Gemini generates responses using the relevant content retrieved from the uploaded documents.

### 🧠 Retrieval-Augmented Generation

The application follows the RAG architecture:

```text
Documents
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Embeddings
    ↓
FAISS Vector Store
    ↓
User Question
    ↓
Query Embedding
    ↓
Similarity Search
    ↓
Relevant Context
    ↓
Google Gemini
    ↓
Answer
````

### 🛡️ Context-Grounded Responses

The prompt instructs the LLM to answer using only the retrieved document context and avoid generating unsupported information.

### ⚡ Local FAISS Vector Store

FAISS is used to store and search document embeddings efficiently.

### 🎨 Streamlit Interface

A simple and interactive web interface is provided for:

* Uploading PDFs
* Processing documents
* Entering questions
* Viewing generated answers

---

#  System Architecture

```text
                       ┌─────────────────────┐
                       │    User Uploads     │
                       │    Multiple PDFs    │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │     PyPDF2          │
                       │   Text Extraction   │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ RecursiveCharacter  │
                       │ Text Splitter       │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Gemini Embeddings   │
                       │ gemini-embedding-001│
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │       FAISS         │
                       │   Vector Index      │
                       └──────────┬──────────┘
                                  │
                         User asks question
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Gemini Embedding    │
                       │ Query Vector        │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ FAISS Similarity    │
                       │ Search              │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Relevant PDF        │
                       │ Chunks / Context    │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Prompt + Context    │
                       │ + User Question     │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Google Gemini       │
                       │ gemini-3.7-flash    │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │     Final Answer    │
                       └─────────────────────┘
```

---

# 🧩 RAG Pipeline Explained

## 1. Document Ingestion

The user uploads one or more PDF files through the Streamlit interface.

```python
pdf_docs = st.file_uploader(
    "Upload your PDF files:",
    type=["pdf"],
    accept_multiple_files=True
)
```

---

## 2. Text Extraction

`PyPDF2` is used to extract text from every page of every uploaded PDF.

```python
pdf_reader = PdfReader(pdf)

for page in pdf_reader.pages:
    page_text = page.extract_text()
```

The extracted content is combined into a single text representation.

---

## 3. Text Chunking

Large documents are divided into smaller chunks using:

```text
RecursiveCharacterTextSplitter
```

Current configuration:

```text
Chunk Size   : 1500 characters
Chunk Overlap: 200 characters
```

### Why chunk documents?

LLMs and embedding models work more effectively when relevant information is provided in manageable sections.

Chunk overlap also helps preserve contextual information between neighboring chunks.

---

## 4. Embedding Generation

Each text chunk is converted into a numerical vector using:

```text
gemini-embedding-001
```

Conceptually:

```text
Text
 ↓
Embedding Model
 ↓
Numerical Vector
```

For example:

```text
"Machine learning is a subset of AI..."
                    ↓
        [0.021, -0.452, 0.782, ...]
```

The vector represents the semantic meaning of the text.

---

## 5. FAISS Vector Store

The generated embeddings are stored in a FAISS index.

```python
vector_store = FAISS.from_texts(
    text_chunks,
    embedding=embeddings
)
```

The index is persisted locally:

```python
vector_store.save_local("faiss_index")
```

FAISS allows the application to efficiently search for vectors that are most similar to a user's question.

---

## 6. Query Embedding

When the user asks a question, the question is converted into an embedding using the same embedding model:

```text
User Question
      ↓
Gemini Embedding Model
      ↓
Query Vector
```

Using the same embedding model for documents and queries ensures that they are represented in the same vector space.

---

## 7. Similarity Search

The query vector is compared with vectors stored in FAISS.

```python
docs = new_db.similarity_search(
    user_question,
    k=4
)
```

The application retrieves the four most relevant document chunks.

```text
1000+ document chunks
        ↓
   FAISS Search
        ↓
Top 4 relevant chunks
```

---

## 8. Context Injection

The retrieved documents are passed to the document chain along with the user's question.

```python
response = chain.invoke({
    "input": user_question,
    "context": docs
})
```

The prompt instructs Gemini to use the retrieved context to answer the question.

---

## 9. Answer Generation

Google Gemini generates the final answer using the retrieved document context.

The system prompt instructs the model to:

* Use only the provided context.
* Avoid outside knowledge.
* Avoid hallucination.
* Answer clearly and briefly.
* State when the information is not available.

---

# 🛠️ Technology Stack

| Technology                   | Purpose                              |
| ---------------------------- | ------------------------------------ |
| **Python**                   | Core programming language            |
| **Streamlit**                | Web application and UI               |
| **PyPDF2**                   | PDF text extraction                  |
| **LangChain**                | RAG application framework            |
| **LangChain Text Splitters** | Document chunking                    |
| **Google Gemini**            | Large Language Model                 |
| **Gemini Embeddings**        | Text and query vectorization         |
| **FAISS**                    | Vector storage and similarity search |
| **python-dotenv**            | Environment variable management      |

---

# 📁 Project Structure

```text
Multi-PDF RAG App/
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
├── .gitignore
│
├── .env
│
└── faiss_index/
    ├── index.faiss
    └── index.pkl
```

> **Note:** `venv/`, `.env`, and `faiss_index/` should be excluded from Git using `.gitignore`.

Recommended `.gitignore`:

```gitignore
venv/
.env
faiss_index/
__pycache__/
*.pyc
.streamlit/secrets.toml
```

---

# ⚙️ Installation and Setup

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate into the project:

```bash
cd "Multi-PDF RAG App"
```

---

## 2. Create a Virtual Environment

Using Conda:

```bash
conda create -p venv python=3.12
```

Activate it:

```bash
conda activate venv
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Google API Key

Create a `.env` file in the project root:

```text
GOOGLE_API_KEY=your_google_api_key
```

The `.env` file is intentionally excluded from Git to protect the API key.

---

## 5. Run the Application

```bash
streamlit run app.py
```

Streamlit will provide a local URL where the application can be accessed.

---

# 🖥️ How to Use

### Step 1 — Upload PDFs

Open the application and upload one or more PDF documents using the sidebar.

### Step 2 — Process Documents

Click:

```text
Submit & Process
```

The application will:

```text
PDF
 ↓
Extract text
 ↓
Create chunks
 ↓
Generate embeddings
 ↓
Create FAISS index
```

### Step 3 — Ask a Question

Enter your question in the main input field.

Example:

```text
What are the main objectives discussed in the document?
```

### Step 4 — Generate Answer

Click:

```text
Ask
```

The system retrieves relevant document chunks and generates an answer using Gemini.

---

# 🔐 Environment Variables

The project requires:

```text
GOOGLE_API_KEY
```

Example:

```text
GOOGLE_API_KEY=YOUR_API_KEY_HERE
```

Never commit your actual API key to GitHub.

---

# 📌 Important Design Decisions

## Why RAG instead of directly asking an LLM?

A general-purpose LLM may not have access to the user's private documents.

RAG provides the relevant document information to the LLM at query time.

```text
Private Documents
       ↓
Retrieval
       ↓
Relevant Context
       ↓
LLM
       ↓
Grounded Answer
```

---

## Why use embeddings?

Traditional keyword search may fail when the question and document use different words but have similar meanings.

Embeddings represent semantic meaning numerically, allowing semantic similarity search.

---

## Why FAISS?

FAISS provides efficient similarity search over high-dimensional vectors and is easy to use for a local RAG learning project.

It is particularly suitable for this project because:

* Easy to integrate with LangChain
* Fast similarity search
* Runs locally
* No external vector database is required
* Good for learning RAG fundamentals

---

## Why Gemini?

Google Gemini provides both:

* Generative language models
* Embedding models

This makes it convenient to build an end-to-end RAG application using the Google ecosystem.

---

## Why LangChain?

LangChain provides components for:

* Document processing
* Text splitting
* Embeddings
* Vector stores
* Prompt templates
* Document chains
* LLM integration

It allows the individual RAG components to be connected into a complete pipeline.

---

# ⚙️ Current Configuration

The current application uses:

```text
Chunk Size       : 1500
Chunk Overlap    : 200
Retrieved Chunks : 4
Temperature      : 0.2
Vector Store     : FAISS
Embedding Model  : gemini-embedding-001
LLM              : Gemini 3.7 Flash
```

These values are initial configurations for this learning project and can be experimented with to evaluate retrieval quality and answer quality.

---

# 🧪 Example Questions

After uploading relevant documents, users can ask questions such as:

```text
What is the main objective of the document?

Summarize the key points.

What methodology was used?

What are the major findings?

Explain the concept discussed in Chapter 2.

What are the advantages mentioned in the document?

Compare the two approaches discussed in the PDF.

Who are the key people mentioned in the document?
```

The actual answers depend entirely on the content of the uploaded PDFs.

---

### 🔹 Vector Databases

The local FAISS implementation can later be replaced or compared with:

* ChromaDB
* Pinecone
* Weaviate
* Qdrant

### 🔹 Conversation Memory

Add chat history so users can ask follow-up questions.

Example:

```text
User:
What is supervised learning?

Assistant:
...

User:
What are its advantages?

Assistant:
...
```

### 🔹 RAG Evaluation

Evaluate:

* Retrieval precision
* Retrieval recall
* Context relevance
* Faithfulness
* Answer relevance

### 🔹 Production Deployment

Potential future stack:

```text
Streamlit / React
        ↓
FastAPI
        ↓
RAG Pipeline
        ↓
Vector Database
        ↓
Gemini
```

---

# 📊 Learning Outcomes

Through this project, I gained practical understanding of:

* Large Language Models
* Retrieval-Augmented Generation
* Document ingestion
* PDF processing
* Text chunking
* Chunk overlap
* Vector embeddings
* Semantic similarity search
* FAISS vector stores
* Prompt engineering
* LangChain
* Google Gemini APIs
* Streamlit application development
* Environment variable management
* Virtual environments
* Git and GitHub

Most importantly, this project helped me understand how individual components such as **embeddings, vector stores, retrievers, prompts, and LLMs work together to form a complete RAG pipeline**.

---

# 🧠 RAG Concepts Demonstrated

```text
Document
    ↓
Chunk
    ↓
Embedding
    ↓
Vector Store
    ↓
Retriever
    ↓
Context
    ↓
Prompt
    ↓
LLM
    ↓
Response
```

This project demonstrates the fundamental architecture behind many modern document-based AI applications.

---

# 👨‍💻 Developer

**Patil Devendra Shivkumar**

Developed as a hands-on project to understand and implement a complete **Retrieval-Augmented Generation (RAG)** pipeline using modern Generative AI technologies.

---

## ⭐ If you find this project useful

Consider giving the repository a ⭐ on GitHub.