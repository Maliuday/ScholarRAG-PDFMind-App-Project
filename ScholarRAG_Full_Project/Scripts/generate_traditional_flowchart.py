import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def create_traditional_flowchart():
    # Setup figure with academic dimensions
    fig, ax = plt.subplots(figsize=(10, 14), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 140)
    ax.axis('off')

    # Color Palette matching Orange Academic Report
    ORANGE_COLOR = '#C55A11'
    NAVY_COLOR = '#C55A11'
    GREEN_COLOR = '#2E7D32'
    RED_COLOR = '#C62828'
    BG_LIGHT_ORANGE = '#FFF8F2'
    BG_LIGHT_BLUE = '#FFF8F2'
    BG_LIGHT_GREEN = '#E8F5E9'
    BORDER_DARK = '#333333'
    TEXT_COLOR = '#111111'

    # Title
    ax.text(50, 137, "TRADITIONAL SYSTEM FLOWCHART — SCHOLARRAG PIPELINE", 
            fontsize=12, fontweight='bold', ha='center', va='center', color=NAVY_COLOR,
            family='serif')
    ax.text(50, 134.5, "Standard ANSI / ISO Flowchart Representation of Ingestion, Indexing, and Retrieval", 
            fontsize=8.5, fontstyle='italic', ha='center', va='center', color='#555555',
            family='serif')

    def draw_terminal(cx, cy, w, h, text, bg_color='#E0E0E0', border_color=BORDER_DARK):
        box = patches.FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                                     boxstyle="round,pad=0.2,rounding_size=1.8",
                                     fc=bg_color, ec=border_color, lw=1.5)
        ax.add_patch(box)
        ax.text(cx, cy, text, fontsize=9, fontweight='bold', ha='center', va='center', color=TEXT_COLOR, family='serif')

    def draw_process(cx, cy, w, h, title, subtitle="", bg_color=BG_LIGHT_BLUE, border_color=NAVY_COLOR):
        box = patches.Rectangle((cx - w/2, cy - h/2), w, h, fc=bg_color, ec=border_color, lw=1.4)
        ax.add_patch(box)
        if subtitle:
            ax.text(cx, cy + 0.9, title, fontsize=8.5, fontweight='bold', ha='center', va='center', color=TEXT_COLOR, family='serif')
            ax.text(cx, cy - 1.1, subtitle, fontsize=7.2, fontstyle='italic', ha='center', va='center', color='#444444', family='serif')
        else:
            ax.text(cx, cy, title, fontsize=8.5, fontweight='bold', ha='center', va='center', color=TEXT_COLOR, family='serif')

    def draw_io(cx, cy, w, h, text, subtext="", bg_color=BG_LIGHT_ORANGE, border_color=ORANGE_COLOR):
        # Parallelogram for Input/Output
        offset = 2.2
        poly = patches.Polygon([
            [cx - w/2 + offset, cy + h/2],
            [cx + w/2, cy + h/2],
            [cx + w/2 - offset, cy - h/2],
            [cx - w/2, cy - h/2]
        ], fc=bg_color, ec=border_color, lw=1.4)
        ax.add_patch(poly)
        if subtext:
            ax.text(cx, cy + 0.8, text, fontsize=8.5, fontweight='bold', ha='center', va='center', color=TEXT_COLOR, family='serif')
            ax.text(cx, cy - 1.1, subtext, fontsize=7.2, fontstyle='italic', ha='center', va='center', color='#444444', family='serif')
        else:
            ax.text(cx, cy, text, fontsize=8.5, fontweight='bold', ha='center', va='center', color=TEXT_COLOR, family='serif')

    def draw_decision(cx, cy, w, h, line1, line2="", bg_color='#FFFDE7', border_color='#F57F17'):
        # Diamond shape
        diamond = patches.Polygon([
            [cx, cy + h/2],
            [cx + w/2, cy],
            [cx, cy - h/2],
            [cx - w/2, cy]
        ], fc=bg_color, ec=border_color, lw=1.4)
        ax.add_patch(diamond)
        if line2:
            ax.text(cx, cy + 0.7, line1, fontsize=7.8, fontweight='bold', ha='center', va='center', color=TEXT_COLOR, family='serif')
            ax.text(cx, cy - 1.0, line2, fontsize=7.2, fontstyle='italic', ha='center', va='center', color='#444444', family='serif')
        else:
            ax.text(cx, cy, line1, fontsize=8, fontweight='bold', ha='center', va='center', color=TEXT_COLOR, family='serif')

    def draw_datastore(cx, cy, w, h, title, subtitle="", bg_color='#EDE7F6', border_color='#512DA8'):
        box = patches.FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                                     boxstyle="round,pad=0.1,rounding_size=0.6",
                                     fc=bg_color, ec=border_color, lw=1.4)
        ax.add_patch(box)
        # Double side lines for datastore indicator
        ax.plot([cx - w/2 + 1.2, cx - w/2 + 1.2], [cy - h/2, cy + h/2], color=border_color, lw=1.2)
        ax.plot([cx + w/2 - 1.2, cx + w/2 - 1.2], [cy - h/2, cy + h/2], color=border_color, lw=1.2)
        if subtitle:
            ax.text(cx, cy + 0.8, title, fontsize=8.5, fontweight='bold', ha='center', va='center', color=TEXT_COLOR, family='serif')
            ax.text(cx, cy - 1.0, subtitle, fontsize=7.2, fontstyle='italic', ha='center', va='center', color='#444444', family='serif')
        else:
            ax.text(cx, cy, title, fontsize=8.5, fontweight='bold', ha='center', va='center', color=TEXT_COLOR, family='serif')

    def draw_arrow(x1, y1, x2, y2, label="", label_pos="right", color='#333333'):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.3, shrinkA=0, shrinkB=0))
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            dx = 1.6 if label_pos == "right" else -1.6
            dy = 0.8 if label_pos == "above" else 0
            ax.text(mx + dx, my + dy, label, fontsize=7.5, fontweight='bold', color=color,
                    ha='center', va='center', family='serif')

    # ─────────────────────────────────────────────────────────────
    # Flowchart Nodes Placement (Vertical Flow Layout)
    # ─────────────────────────────────────────────────────────────

    # 1. Start
    draw_terminal(50, 130, 22, 4.2, "START", bg_color='#E2E8F0', border_color=NAVY_COLOR)
    draw_arrow(50, 127.9, 50, 122.5)

    # 2. Input: Upload PDFs
    draw_io(50, 119.5, 54, 5.5, "Input: Upload Multi-PDF Documents", "User selects 1 to N academic / technical PDF files")
    draw_arrow(50, 116.7, 50, 111.5)

    # 3. Process: PyPDF2 Text Extraction
    draw_process(50, 108.5, 56, 5.5, "Process: Stream Text Extraction & Cleaning", "PyPDF2 extracts pages, strips null bytes & normalizes text")
    draw_arrow(50, 105.7, 50, 100.5)

    # 4. Decision: Any Text Found?
    draw_decision(50, 96.5, 34, 7.5, "Readable Text", "Extracted?", bg_color='#FFFDE7', border_color='#F57F17')
    # Decision branch No -> Error display on left
    draw_arrow(33, 96.5, 14, 96.5, "No", label_pos="above", color=RED_COLOR)
    draw_io(14, 89.5, 24, 6.0, "Display Error:", "No readable text", bg_color='#FFEBEE', border_color=RED_COLOR)
    draw_arrow(14, 96.5, 14, 92.5)
    # Branch Yes -> Chunking
    draw_arrow(50, 92.7, 50, 87.5, "Yes", label_pos="right", color=GREEN_COLOR)

    # 5. Process: Recursive Semantic Chunking
    draw_process(50, 84.5, 58, 5.5, "Process: Recursive Character Text Chunking", "Splits by [\\n\\n, \\n, . , ' '] with dynamic overlap (C=2000, O=300)")
    draw_arrow(50, 81.7, 50, 76.5)

    # 6. Process: Generate Vector Embeddings
    draw_process(50, 73.5, 58, 5.5, "Process: Generate Dense 3072-dim Embeddings", "Google Gemini gemini-embedding-001 with L2 normalization")
    draw_arrow(50, 70.7, 50, 65.5)

    # 7. Decision: API Rate Limit Check (429)?
    draw_decision(50, 61.5, 34, 7.5, "HTTP 429 Quota", "Exceeded?", bg_color='#FFFDE7', border_color='#F57F17')
    # If Yes -> Exponential backoff loop on right
    draw_arrow(67, 61.5, 86, 61.5, "Yes", label_pos="above", color=RED_COLOR)
    draw_process(86, 67.5, 24, 5.5, "Exponential Backoff", "t = t_base * 2^att + jitter", bg_color='#FFF3E0', border_color=ORANGE_COLOR)
    draw_arrow(86, 61.5, 86, 64.7)
    draw_arrow(86, 70.3, 86, 73.5)
    draw_arrow(86, 73.5, 79, 73.5) # loop back to embedding
    # If No -> Build FAISS Index
    draw_arrow(50, 57.7, 50, 52.5, "No", label_pos="right", color=GREEN_COLOR)

    # 8. Data Store & Indexing: FAISS IndexFlatIP
    draw_datastore(50, 49.5, 58, 5.5, "Data Store: FAISS Vector Database", "Local in-memory index.faiss + index.pkl serialization")
    draw_arrow(50, 46.7, 50, 41.5)

    # 9. Input: User Question Submission
    draw_io(50, 38.5, 54, 5.5, "Input: User Natural Language Question", "User enters query & selects target foundation model")
    draw_arrow(50, 35.7, 50, 30.5)

    # 10. Process: Vector Similarity Search
    draw_process(50, 27.5, 58, 5.5, "Process: FAISS Cosine Distance Top-K Retrieval", "Inner Product similarity search retrieves Top-K most relevant chunks")
    draw_arrow(50, 24.7, 50, 19.5)

    # 11. Process: Grounded Prompt & LLM Generation
    draw_process(50, 16.5, 60, 5.5, "Process: Grounded Synthesis via Gemini API", "Injects context into strict prompt template (rejects hallucinations)")
    draw_arrow(50, 13.7, 50, 8.5)

    # 12. Output: Rendered Answer & Citations
    draw_io(50, 5.5, 58, 5.5, "Output: Formatted Answer + Inspectable Citations", "Displays synthesized response with similarity scores & source text")
    draw_arrow(50, 2.7, 50, -0.5)

    # 13. Terminal: End
    draw_terminal(50, -2.5, 22, 4.0, "END", bg_color='#E2E8F0', border_color=NAVY_COLOR)

    # Route error block to End
    draw_arrow(14, 86.5, 14, -2.5, color='#999999')
    draw_arrow(14, -2.5, 39, -2.5, color='#999999')

    # Save Flowchart Image
    assets_dir = r"C:\Users\sdmal\OneDrive\Desktop\hunt\assets"
    os.makedirs(assets_dir, exist_ok=True)
    out_path = os.path.join(assets_dir, "traditional_system_flowchart.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Traditional flowchart successfully generated at: {out_path}")

if __name__ == "__main__":
    create_traditional_flowchart()
