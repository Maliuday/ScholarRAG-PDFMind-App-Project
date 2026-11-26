import streamlit as st
import os
import time
from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI)
from langchain_community.vectorstores import FAISS
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# Page Config & Session State Initialization
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ScholarRAG — AI PDF Assistant",
    page_icon="🧠",
    layout="wide"
)

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processed" not in st.session_state:
    st.session_state.processed = False
if "processing_stats" not in st.session_state:
    st.session_state.processing_stats = {}

# ─────────────────────────────────────────────
# Dynamic Theme CSS (High-Contrast Dark / Light Mode)
# ─────────────────────────────────────────────
if st.session_state.theme == "Dark":
    theme_css = """
    <style>
        .stApp {
            background-color: #0b0f19 !important;
            color: #f1f5f9 !important;
        }
        [data-testid="stSidebar"] {
            background-color: #111827 !important;
            border-right: 1px solid #1f2937 !important;
        }
        [data-testid="stSidebar"] * {
            color: #e2e8f0 !important;
        }
        .header-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-bottom: 0.25rem;
        }
        .header-icon {
            font-size: 2.8rem;
            line-height: 1;
        }
        .main-header {
            font-size: 2.7rem;
            font-weight: 800;
            background: linear-gradient(135deg, #60a5fa, #a78bfa, #f472b6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            padding: 0;
            letter-spacing: -0.5px;
        }
        .sub-header {
            text-align: center;
            color: #94a3b8 !important;
            font-size: 1.05rem;
            font-weight: 500;
            margin-bottom: 2rem;
        }
        /* Buttons */
        .stButton>button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
            color: #ffffff !important;
            border: 1px solid #3b82f6 !important;
            transition: all 0.2s ease !important;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
            border-color: #60a5fa !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
        }
        /* Chat Messages */
        [data-testid="stChatMessage"] {
            background-color: #161e2e !important;
            border: 1px solid #283548 !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            margin-bottom: 12px !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25) !important;
        }
        [data-testid="stChatMessage"] * {
            color: #f1f5f9 !important;
        }
        /* Metrics Cards */
        [data-testid="stMetric"] {
            background-color: #161e2e !important;
            border: 1px solid #283548 !important;
            border-radius: 10px !important;
            padding: 12px !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
        }
        [data-testid="stMetricValue"] * {
            color: #60a5fa !important;
            font-weight: 700 !important;
        }
        [data-testid="stMetricLabel"] * {
            color: #94a3b8 !important;
            font-size: 0.9rem !important;
        }
        /* Expanders */
        .streamlit-expanderHeader {
            background-color: #161e2e !important;
            border: 1px solid #283548 !important;
            border-radius: 8px !important;
            color: #cbd5e1 !important;
        }
        [data-testid="stExpander"] {
            background-color: #111827 !important;
            border: 1px solid #283548 !important;
            border-radius: 8px !important;
        }
        /* Chat Input */
        [data-testid="stChatInput"] {
            border-color: #3b82f6 !important;
        }
    </style>
    """
else:
    theme_css = """
    <style>
        .stApp {
            background-color: #f8fafc !important;
            color: #0f172a !important;
        }
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #e2e8f0 !important;
        }
        [data-testid="stSidebar"] * {
            color: #0f172a !important;
        }
        .header-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-bottom: 0.25rem;
        }
        .header-icon {
            font-size: 2.8rem;
            line-height: 1;
        }
        .main-header {
            font-size: 2.7rem;
            font-weight: 800;
            background: linear-gradient(135deg, #1d4ed8, #6d28d9, #be185d);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            padding: 0;
            letter-spacing: -0.5px;
        }
        .sub-header {
            text-align: center;
            color: #334155 !important;
            font-size: 1.05rem;
            font-weight: 600;
            margin-bottom: 2rem;
        }
        /* Buttons */
        .stButton>button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
            color: #ffffff !important;
            border: none !important;
            box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2) !important;
            transition: all 0.2s ease !important;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3) !important;
            color: #ffffff !important;
        }
        /* Chat Messages - Sharp High Contrast on Light Mode */
        [data-testid="stChatMessage"] {
            background-color: #ffffff !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            margin-bottom: 12px !important;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08) !important;
        }
        [data-testid="stChatMessage"] * {
            color: #0f172a !important;
        }
        /* Metrics Cards */
        [data-testid="stMetric"] {
            background-color: #ffffff !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 10px !important;
            padding: 12px !important;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.06) !important;
        }
        [data-testid="stMetricValue"] * {
            color: #1d4ed8 !important;
            font-weight: 700 !important;
        }
        [data-testid="stMetricLabel"] * {
            color: #334155 !important;
            font-size: 0.9rem !important;
            font-weight: 700 !important;
        }
        /* Expanders */
        .streamlit-expanderHeader {
            background-color: #ffffff !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 8px !important;
            color: #0f172a !important;
            font-weight: 700 !important;
        }
        [data-testid="stExpander"] {
            background-color: #f1f5f9 !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 8px !important;
        }
        [data-testid="stExpander"] * {
            color: #0f172a !important;
        }
        /* Alert Info/Warning boxes */
        .stAlert {
            border-radius: 8px !important;
            border: 1.5px solid #cbd5e1 !important;
        }
        .stAlert * {
            color: #0f172a !important;
        }
        /* Chat Input */
        [data-testid="stChatInput"] {
            border: 1.5px solid #2563eb !important;
            background-color: #ffffff !important;
        }
        [data-testid="stChatInput"] textarea {
            color: #0f172a !important;
            font-weight: 500 !important;
        }
    </style>
    """

st.markdown(theme_css, unsafe_allow_html=True)



# ─────────────────────────────────────────────
# Core RAG Functions
# ─────────────────────────────────────────────
def get_pdf_text(pdf_docs):
    """Extract text from all uploaded PDFs and return text + page count."""
    text = ""
    total_pages = 0
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            total_pages += len(pdf_reader.pages)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            st.warning(f"⚠️ Could not read {pdf.name}: {str(e)}")
    return text, total_pages


def get_text_chunks(text, chunk_size, chunk_overlap):
    """Split text into chunks with configurable size and overlap."""
    # Ensure overlap is always less than chunk_size
    if chunk_overlap >= chunk_size:
        chunk_overlap = chunk_size // 4

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    """Generate embeddings in batches with retry logic to avoid rate limits."""
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

    batch_size = 5
    vector_store = None
    progress_bar = st.progress(0, text="Generating embeddings...")
    total_batches = (len(text_chunks) + batch_size - 1) // batch_size

    for i in range(0, len(text_chunks), batch_size):
        batch = text_chunks[i:i + batch_size]
        batch_num = i // batch_size + 1
        progress = min((i + batch_size) / len(text_chunks), 1.0)
        progress_bar.progress(progress, text=f"Embedding batch {batch_num}/{total_batches}...")

        # Retry with exponential backoff
        max_retries = 5
        for attempt in range(max_retries):
            try:
                if vector_store is None:
                    vector_store = FAISS.from_texts(batch, embedding=embeddings)
                else:
                    batch_store = FAISS.from_texts(batch, embedding=embeddings)
                    vector_store.merge_from(batch_store)
                break  # Success
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    wait_time = (2 ** attempt) * 5  # 5s, 10s, 20s, 40s, 80s
                    progress_bar.progress(
                        progress,
                        text=f"⏳ Rate limited — waiting {wait_time}s (retry {attempt+1}/{max_retries})..."
                    )
                    time.sleep(wait_time)
                else:
                    progress_bar.empty()
                    raise e
        else:
            progress_bar.empty()
            st.error("❌ Failed after multiple retries. Please wait a few minutes and try again.")
            return False

        # Delay between batches
        if i + batch_size < len(text_chunks):
            time.sleep(4)

    progress_bar.empty()
    vector_store.save_local("faiss_index")
    return True


def get_conversational_chain(temperature, model_name):
    """Create the LLM chain with configurable temperature, model, and strict timeout."""
    prompt_template = """You are a helpful assistant answering questions based on
    the uploaded PDF documents.

    Follow these rules:

    1. Answer the question using ONLY the provided context.
    2. Do not use outside knowledge.
    3. Answer briefly and clearly.
    4. Use bullet points when multiple details are required.
    5. Do not make up or hallucinate information.
    6. If the answer is not available in the provided context,
    say exactly: "Answer is not available in the provided PDF."

    Context:
    {context}
    Question:
    {input}
    Answer: """

    model = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        timeout=12,
        max_retries=1
    )
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "input"])
    chain = create_stuff_documents_chain(llm=model, prompt=prompt)
    return chain


def get_answer(user_question, top_k, temperature, model_name):
    """Process user question: retrieve relevant chunks and generate answer."""
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question, k=top_k)
    
    # Fast reliable models ordered by latency and stability
    fallback_models = [
        model_name,
        "gemini-flash-lite-latest",
        "gemini-3.1-flash-lite",
        "gemini-3-flash-preview",
        "gemini-3.5-flash-lite",
        "gemini-3.8-flash"
    ]
    # Deduplicate while preserving order
    models_to_try = list(dict.fromkeys(fallback_models))
    
    last_err = None
    for m in models_to_try:
        try:
            chain = get_conversational_chain(temperature, m)
            raw_response = chain.invoke({
                "input": user_question,
                "context": docs,
            })
            # Convert response to string if it is an object
            return str(raw_response), docs, m
        except Exception as e:
            last_err = e
            continue
            
    raise last_err


# ─────────────────────────────────────────────
# Main Application
# ─────────────────────────────────────────────
def main():
    # ── Header ──
    st.markdown('''
    <div class="header-container">
        <span class="header-icon">🧠</span>
        <span class="main-header">ScholarRAG</span>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">AI-Powered Multi-PDF RAG Assistant — Upload PDFs, Ask Questions, Get Answers</div>',
        unsafe_allow_html=True
    )

    # ── Sidebar ──
    with st.sidebar:
        # Theme Toggle
        selected_theme = st.radio(
            "🎨 Theme Mode",
            ["🌙 Dark", "☀️ Light"],
            index=0 if st.session_state.theme == "Dark" else 1,
            horizontal=True
        )
        theme_val = "Dark" if "Dark" in selected_theme else "Light"
        if theme_val != st.session_state.theme:
            st.session_state.theme = theme_val
            st.rerun()

        st.markdown("---")
        st.title("📂 Upload Section")
        pdf_docs = st.file_uploader(
            "Upload your PDF files:",
            type=["pdf"],
            accept_multiple_files=True
        )

        # Show uploaded file names
        if pdf_docs:
            st.markdown("### 📋 Uploaded Files:")
            for pdf in pdf_docs:
                file_size = len(pdf.getvalue()) / 1024  # KB
                st.markdown(f"- ✅ **{pdf.name}** ({file_size:.1f} KB)")

        st.markdown("---")

        # ── RAG Settings ──
        st.subheader("⚙️ RAG Parameters")
        chunk_size = st.slider("Chunk Size", 500, 5000, 2000, step=100,
                               help="Size of each text chunk in characters. Larger = more context per chunk.")
        chunk_overlap = st.slider("Chunk Overlap", 50, 1000, 300, step=50,
                                  help="Overlap between chunks to preserve context across boundaries.")
        top_k = st.slider("Top K Results", 1, 15, 5,
                          help="Number of most relevant chunks to retrieve for answering.")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.2, step=0.1,
                                help="Lower = more focused answers. Higher = more creative.")

        # ── Model Selection ──
        st.markdown("---")
        st.subheader("🤖 Model Selection")
        model_name = st.selectbox(
            "Choose Gemini Model:",
            [
                "gemini-flash-lite-latest",
                "gemini-3.1-flash-lite",
                "gemini-3.5-flash-lite",
                "gemini-3-flash-preview",
                "gemini-3.8-flash"
            ],
            index=0,
            help="gemini-flash-lite-latest provides sub-second, ultra-fast responses."
        )

        st.markdown("---")

        # ── Process Button ──
        if st.button("🚀 Submit & Process", use_container_width=True):
            if pdf_docs:
                with st.spinner("Processing PDFs..."):
                    start_time = time.time()

                    # Step 1: Extract text
                    raw_text, total_pages = get_pdf_text(pdf_docs)

                    if not raw_text.strip():
                        st.error("❌ No readable text found in the uploaded PDF files.")
                    else:
                        # Step 2: Create chunks
                        text_chunks = get_text_chunks(raw_text, chunk_size, chunk_overlap)

                        # Step 3: Create vector store
                        success = get_vector_store(text_chunks)

                        if success:
                            elapsed = time.time() - start_time

                            # Save stats
                            st.session_state.processing_stats = {
                                "files": len(pdf_docs),
                                "pages": total_pages,
                                "chunks": len(text_chunks),
                                "chars": len(raw_text),
                                "time": elapsed,
                                "chunk_size": chunk_size,
                                "chunk_overlap": chunk_overlap,
                            }
                            st.session_state.processed = True
                            st.success("✅ Processing Complete!")
            else:
                st.warning("⚠️ Please upload at least one PDF file.")

    # ── Processing Stats Display ──
    if st.session_state.processed and st.session_state.processing_stats:
        stats = st.session_state.processing_stats
        st.markdown("### 📊 Processing Statistics")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("📄 PDFs", stats["files"])
        with col2:
            st.metric("📃 Pages", stats["pages"])
        with col3:
            st.metric("🧩 Chunks", stats["chunks"])
        with col4:
            st.metric("📝 Characters", f"{stats['chars']:,}")
        with col5:
            st.metric("⏱️ Time", f"{stats['time']:.1f}s")

        st.caption(
            f"Settings used → Chunk Size: {stats['chunk_size']} | "
            f"Overlap: {stats['chunk_overlap']}"
        )
        st.markdown("---")

    # ── Chat History Display ──
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "🧠"):
            st.write(msg["content"])
            if msg["role"] == "assistant" and "elapsed" in msg:
                st.caption(f"⚡ *Response generated in {msg['elapsed']:.2f}s via `{msg.get('model', 'gemini')}`*")

            # Show source chunks for assistant messages
            if msg["role"] == "assistant" and "sources" in msg:
                with st.expander(f"📄 View Source Chunks ({len(msg['sources'])} chunks used)"):
                    for i, chunk in enumerate(msg["sources"]):
                        st.markdown(f"**Chunk {i+1}:**")
                        st.info(chunk[:600] + ("..." if len(chunk) > 600 else ""))

    # ── Question Input ──
    user_question = st.chat_input("💬 Ask a question from your PDF files...")

    if user_question:
        if not os.path.exists("faiss_index"):
            st.warning("⚠️ Please upload and process PDF files first using the sidebar.")
        else:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_question})
            with st.chat_message("user", avatar="🧑‍💻"):
                st.write(user_question)

            # Generate answer
            with st.chat_message("assistant", avatar="🧠"):
                with st.spinner("🔍 Searching and generating answer..."):
                    t_start = time.time()
                    try:
                        response, docs, used_model = get_answer(
                            user_question, top_k, temperature, model_name
                        )
                        elapsed = time.time() - t_start

                        st.write(response)
                        st.caption(f"⚡ *Response generated in {elapsed:.2f}s via `{used_model}`*")

                        # Show source chunks
                        source_texts = [doc.page_content for doc in docs]
                        with st.expander(f"📄 View Source Chunks ({len(docs)} chunks used)"):
                            for i, doc in enumerate(docs):
                                st.markdown(f"**Chunk {i+1}:**")
                                st.info(
                                    doc.page_content[:600]
                                    + ("..." if len(doc.page_content) > 600 else "")
                                )

                        # Save to chat history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response,
                            "sources": source_texts,
                            "model": used_model,
                            "elapsed": elapsed
                        })

                    except Exception as e:
                        error_str = str(e)
                        # Provide helpful error messages
                        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                            st.error("⏳ Rate limit reached. Please wait 1-2 minutes and try again.")
                        elif "404" in error_str or "NOT_FOUND" in error_str:
                            st.error(f"❌ Model not available. Try selecting a different model from the sidebar.")
                        elif "API_KEY" in error_str or "api_key" in error_str:
                            st.error("🔑 Invalid API key. Please check your .env file.")
                        else:
                            st.error(f"❌ Error: {error_str}")

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"❌ Error: {error_str}"
                        })

    # ── Export & Clear Chat ──
    if st.session_state.messages:
        st.markdown("---")
        col1, col2 = st.columns([1, 1])

        with col1:
            chat_text = "\n\n".join(
                [f"{'YOU' if m['role']=='user' else 'ScholarRAG'}: {m['content']}"
                 for m in st.session_state.messages]
            )
            st.download_button(
                "📥 Download Chat History",
                chat_text,
                "scholarrag_chat_history.txt",
                use_container_width=True
            )

        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

    # ── Footer ──
    st.markdown("---")
    st.caption("Developed By : MCA II | Powered by Google Gemini & LangChain")


if __name__ == "__main__":
    main()