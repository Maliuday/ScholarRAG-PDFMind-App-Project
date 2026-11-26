with open(r'C:\Users\sdmal\OneDrive\Desktop\hunt\build_full_report.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace toc_hierarchy block
old_toc = '''    # (level: 0=Chapter/Prelim, 1=Section, 2=Subsection, Title, Page)
    toc_hierarchy = ['''

new_toc_block = '''    # (level: 0=Chapter/Prelim, 1=Section, 2=Subsection, Title, Page)
    toc_hierarchy = [
        (0, "Certificate", "ii"),
        (0, "Declaration", "iii"),
        (0, "Acknowledgement", "iv"),
        (0, "Abstract", "v"),
        (0, "List of Figures", "viii"),
        (0, "List of Tables", "viii"),
        (0, "List of Abbreviations", "ix"),
        (0, "CHAPTER 1: INTRODUCTION", "1"),
        (1, "1.1 Background & Context of RAG & LLMs", "1"),
        (1, "1.2 Problem Statement & Industry Bottlenecks", "1"),
        (1, "1.3 Project Aim & Core Objectives", "1"),
        (1, "1.4 Research Questions (RQ1–RQ5)", "2"),
        (1, "1.5 Scope and Delimitations of the Study", "2"),
        (1, "1.6 Academic & Practical Motivation", "2"),
        (1, "1.7 Key Technical Contributions", "3"),
        (1, "1.8 High-Level Methodology Overview", "3"),
        (1, "1.9 Outline of the Dissertation", "3"),
        (0, "CHAPTER 2: LITERATURE REVIEW & THEORETICAL FOUNDATIONS", "4"),
        (1, "2.1 Evolution of Document Information Retrieval", "4"),
        (1, "2.2 Transformer Architecture & Foundation Models", "4"),
        (1, "2.3 The Anatomy of Hallucinations in LLMs", "4"),
        (1, "2.4 Retrieval-Augmented Generation (RAG) Taxonomy", "4"),
        (1, "2.5 Comparative Technology Matrix & Research Gap", "5"),
        (1, "2.6 Chunking Theory & Semantic Boundary Dynamics", "5"),
        (1, "2.7 Vector Embeddings & High-Dimensional Semantic Topology", "5"),
        (1, "2.8 Vector Indexing Algorithms (Flat, IVFFlat, HNSW in FAISS)", "6"),
        (1, "2.9 Comparative Review of Existing Document Assistants", "6"),
        (0, "CHAPTER 3: SYSTEM REQUIREMENTS & ARCHITECTURAL DESIGN", "7"),
        (1, "3.1 Software Requirements Specification (SRS)", "7"),
        (2, "3.1.1 Functional Requirements (FR-01 to FR-10)", "7"),
        (2, "3.1.2 Non-Functional Requirements (NFR-01 to NFR-05)", "8"),
        (1, "3.2 High-Level End-to-End Architectural Pipeline", "9"),
        (1, "3.3 Traditional System Flowchart & Procedural Logic", "10"),
        (1, "3.4 Multi-PDF Ingestion & Text Parsing Subsystem", "11"),
        (1, "3.5 Mathematical Formulation of Recursive Chunking", "11"),
        (1, "3.6 Dense Vector Embedding Generation & Caching", "11"),
        (1, "3.7 FAISS Vector Indexing & Cosine Distance Search Math", "11"),
        (1, "3.8 Resiliency & API Quota Throttling Engine", "11"),
        (1, "3.9 Generation Prompt Engineering & Strict Grounding", "11"),
        (0, "CHAPTER 4: IMPLEMENTATION DETAILS & CODE ARCHITECTURE", "12"),
        (1, "4.1 Project Directory Structure & Modular Hierarchy", "12"),
        (1, "4.2 Detailed Implementation Technology Stack Table", "12"),
        (1, "4.3 Multi-PDF Extraction & Preprocessing Module", "13"),
        (1, "4.4 Vector Indexing & Serialization Workflow", "13"),
        (1, "4.5 Retrieval Engine & Dynamic Top-K Scoring", "13"),
        (1, "4.6 Generation Chain & Prompt Template Design", "13"),
        (1, "4.7 Dynamic Dual-Theme UI/UX Engine", "14"),
        (1, "4.8 Interactive Parameter Control & Model Selection Panel", "15"),
        (1, "4.9 Document Staging, Uploading & Real-Time Telemetry", "16"),
        (1, "4.10 Grounded Response Synthesizer & Citation Inspector", "17"),
        (0, "CHAPTER 5: TESTING, BENCHMARKING & EMPIRICAL EVALUATION", "18"),
        (1, "5.1 Answer Correctness as a Case Study & Theoretical Framework", "18"),
        (1, "5.2 Verification & Validation Testing Methodology", "19"),
        (1, "5.3 Evaluation Approach & Experimental Setup", "19"),
        (1, "5.4 Comprehensive Functional Test Catalogue (TC-01 to TC-20)", "19"),
        (1, "5.5 Dense Retrieval Performance Evaluation (12 Metrics)", "21"),
        (1, "5.6 Cross-Model Generative Benchmarks (Gemini, Claude, Grok, GPT)", "22"),
        (1, "5.7 Latency vs. Groundedness Frontier Analysis", "23"),
        (1, "5.8 End-to-End Latency Profile Subsystem Breakdown", "24"),
        (1, "5.9 Adversarial & Negative Grounding Experiments", "24"),
        (1, "5.10 Usability Study & User Feedback Analysis (SUS)", "24"),
        (0, "CHAPTER 6: CONCLUSION, RISK REGISTER & FUTURE SCOPE", "25"),
        (1, "6.1 Summary of Research Findings & Achievements", "25"),
        (1, "6.2 Comprehensive Risk Register & Implemented Mitigations", "25"),
        (1, "6.3 Critical Limitations of Current Prototype", "25"),
        (1, "6.4 Future Engineering Roadmap (Vision-RAG, Hybrid Fusion, GraphRAG)", "25"),
        (1, "6.5 Ethical AI Deployment & Privacy Compliance", "26"),
        (1, "6.6 Reproducibility Protocol & Environment Setup", "26"),
        (0, "REFERENCES & BIBLIOGRAPHY", "27"),
        (0, "APPENDIX A: RESEARCH PROPOSAL & PHASE-WISE WORK PLAN", "29"),
        (0, "APPENDIX B: PROJECT PROGRESS DIARY & GUIDE MEETING LOGBOOK", "30"),
        (0, "APPENDIX C: ACADEMIC INTEGRITY & CODE REPOSITORY DECLARATION", "31")
    ]'''

# Extract current toc_hierarchy until ']'
import re
code = re.sub(r'# \(level: 0=Chapter/Prelim, 1=Section, 2=Subsection, Title, Page\)\s+toc_hierarchy = \[.*?\]', new_toc_block, code, flags=re.DOTALL)

# Replace figures_list block
new_figures_block = '''    figures_list = [
        ("Figure 3.1", "ScholarRAG End-to-End Architectural Pipeline & Ingestion Dataflow", "9"),
        ("Figure 3.2", "Traditional System Flowchart of ScholarRAG Ingestion and Query Execution Pipeline", "10"),
        ("Figure 4.1", "ScholarRAG Interactive Web Interface in Dark Theme", "14"),
        ("Figure 4.2", "ScholarRAG High-Contrast Light Theme User Interface", "14"),
        ("Figure 4.3", "Dynamic RAG Parameter Tuning & Model Selector Sidebar Panel", "15"),
        ("Figure 4.4", "Multi-Document Staging & File Upload Status Dashboard", "16"),
        ("Figure 4.5", "FAISS In-Memory Vector Store Creation & Ingestion Telemetry", "16"),
        ("Figure 4.6", "Grounded RAG Response Synthesis with Expanded Citation Sources", "17"),
        ("Figure 5.1", "Quantitative Information-Centred View of Answer Correctness & Hallucination Taxonomy in RAG", "18"),
        ("Figure 5.2", "Empirical Retrieval Dynamics Curve — Recall, Precision, Hit Rate, and NDCG vs. Top-K", "22"),
        ("Figure 5.3", "Multi-Model Generation Comparison — Faithfulness, ROUGE-L, and Relevance across frontier LLMs", "23"),
        ("Figure 5.4", "Inference Latency vs Groundedness (Faithfulness) Pareto Frontier", "23")
    ]'''

code = re.sub(r'figures_list = \[.*?\]', new_figures_block, code, flags=re.DOTALL)

# Replace tables_list block
new_tables_block = '''    tables_list = [
        ("Table 2.1", "Comparative Technology Matrix Across Web LLM, Fine-Tuned, Cloud RAG, and ScholarRAG", "5"),
        ("Table 3.1", "Software Requirements Specification (Functional & Non-Functional Requirements)", "8"),
        ("Table 4.1", "ScholarRAG Layered Implementation Technology Stack & Package Specifications", "12"),
        ("Table 5.1", "Comprehensive Functional Test Catalogue (20 Test Cases TC-01 to TC-20)", "20"),
        ("Table 5.2", "Empirical Dense Retrieval Performance Evaluation across 12 Statistical Metrics", "22"),
        ("Table 5.3", "Cross-Model Generative Reasoning Benchmarks (Gemini 3.8, Claude 3.5, Grok-2, GPT-4o)", "23"),
        ("Table 5.4", "End-to-End Query Latency Profile and Subsystem Duration Breakdown", "24"),
        ("Table 5.5", "Negative Grounding & Adversarial Hallucination Resistance Matrix", "24"),
        ("Table 6.1", "Comprehensive Operational Risk Register and Implemented Mitigations", "25")
    ]'''

code = re.sub(r'tables_list = \[.*?\]', new_tables_block, code, flags=re.DOTALL)

with open(r'C:\Users\sdmal\OneDrive\Desktop\hunt\build_full_report.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Updated mappings in build_full_report.py successfully!')
