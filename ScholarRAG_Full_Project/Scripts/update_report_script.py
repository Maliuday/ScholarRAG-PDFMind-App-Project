import re

with open(r'C:\Users\sdmal\OneDrive\Desktop\hunt\build_full_report.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update imports
if 'from docx.enum.section import WD_SECTION' not in code:
    code = code.replace(
        'from docx.enum.table import WD_TABLE_ALIGNMENT',
        'from docx.enum.table import WD_TABLE_ALIGNMENT\nfrom docx.enum.section import WD_SECTION'
    )

# 2. Add apply_section_formatting and update initial section setup
old_sec_setup = '''    # ─────────────────────────────────────────────────────────────
    # Page Setup & Margins (Optimized to utilize all printable space)
    # ─────────────────────────────────────────────────────────────
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.75)
        section.header_distance = Inches(0.4)
        section.footer_distance = Inches(0.4)

        # Single Black Page Border (All 4 Sides, Default Single Line Only)
        sectPr = section._sectPr
        border_xml = parse_xml(
            f'<w:pgBorders {nsdecls("w")} w:offsetFrom="page">'
            f'<w:top w:val="single" w:sz="12" w:space="18" w:color="{BORDER_COLOR_HEX}"/>'
            f'<w:left w:val="single" w:sz="12" w:space="18" w:color="{BORDER_COLOR_HEX}"/>'
            f'<w:bottom w:val="single" w:sz="12" w:space="18" w:color="{BORDER_COLOR_HEX}"/>'
            f'<w:right w:val="single" w:sz="12" w:space="18" w:color="{BORDER_COLOR_HEX}"/>'
            f'</w:pgBorders>'
        )
        sectPr.append(border_xml)'''

new_sec_setup = '''    # ─────────────────────────────────────────────────────────────
    # Page Setup, Dual-Section Formatting & Page Numbering Engine
    # ─────────────────────────────────────────────────────────────
    def apply_section_formatting(section, is_prelim=False):
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.75)
        section.header_distance = Inches(0.4)
        section.footer_distance = Inches(0.4)

        # Single Black Page Border (All 4 Sides, Default Single Line Only)
        sectPr = section._sectPr
        border_xml = parse_xml(
            f'<w:pgBorders {nsdecls("w")} w:offsetFrom="page">'
            f'<w:top w:val="single" w:sz="12" w:space="18" w:color="{BORDER_COLOR_HEX}"/>'
            f'<w:left w:val="single" w:sz="12" w:space="18" w:color="{BORDER_COLOR_HEX}"/>'
            f'<w:bottom w:val="single" w:sz="12" w:space="18" w:color="{BORDER_COLOR_HEX}"/>'
            f'<w:right w:val="single" w:sz="12" w:space="18" w:color="{BORDER_COLOR_HEX}"/>'
            f'</w:pgBorders>'
        )
        sectPr.append(border_xml)

        if is_prelim:
            # Preliminary Pages: Roman Numerals (ii, iii, iv...), first page (Cover) hidden
            section.different_first_page_header_footer = True
            pgNumType = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="lowerRoman" w:start="1"/>')
            sectPr.append(pgNumType)

            footer = section.footer
            p_f = footer.paragraphs[0]
            p_f.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_f.paragraph_format.space_before = Pt(4)
            p_f.paragraph_format.space_after = Pt(0)
            fld = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
            p_f._p.append(fld)
        else:
            # Main Body: Arabic Numerals (1, 2, 3...) starting at 1 on Chapter 1
            section.different_first_page_header_footer = False
            section.header.is_linked_to_previous = False
            section.footer.is_linked_to_previous = False
            pgNumType = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="decimal" w:start="1"/>')
            sectPr.append(pgNumType)

            footer = section.footer
            p_f = footer.paragraphs[0]
            p_f.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_f.paragraph_format.space_before = Pt(4)
            p_f.paragraph_format.space_after = Pt(0)
            fld = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
            p_f._p.append(fld)

    # Apply Preliminary Section Formatting to Section 1
    apply_section_formatting(doc.sections[0], is_prelim=True)'''

code = code.replace(old_sec_setup, new_sec_setup)

# 3. Add footer style to styles
old_style_setup = '''    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = TEXT_DARK_RGB
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_before = Pt(2)
    normal_style.paragraph_format.space_after = Pt(4)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY'''

new_style_setup = '''    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = TEXT_DARK_RGB
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_before = Pt(2)
    normal_style.paragraph_format.space_after = Pt(4)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    footer_style = doc.styles['Footer']
    footer_style.font.name = 'Times New Roman'
    footer_style.font.size = Pt(10)
    footer_style.font.color.rgb = TEXT_DARK_RGB'''

code = code.replace(old_style_setup, new_style_setup)

# 4. Add add_table_caption helper
old_add_fig = '''    def add_fig(img_path, caption, width=5.6):'''
new_add_fig = '''    def add_table_caption(title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10.5)
        run.font.color.rgb = ORANGE_RGB
        return p

    def add_fig(img_path, caption, width=5.6):'''

code = code.replace(old_add_fig, new_add_fig)

# 5. Replace page break before Chapter 1 with add_section
old_ch1_break = '''    add_table_data(["Abbreviation", "Expanded Definition"], abbr_data, [1.8, 4.8])

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION'''

new_ch1_break = '''    add_table_data(["Abbreviation", "Expanded Definition"], abbr_data, [1.8, 4.8])

    # =========================================================================
    # SECTION 2: MAIN BODY (Arabic Page Numbering Starts at Page 1)
    # =========================================================================
    sec_body = doc.add_section(WD_SECTION.NEW_PAGE)
    apply_section_formatting(sec_body, is_prelim=False)

    # =========================================================================
    # CHAPTER 1: INTRODUCTION'''

code = code.replace(old_ch1_break, new_ch1_break)

# 6. Add table captions above tables
table_captions = [
    ('tech_matrix_data = [', 'add_table_caption("Table 2.1: Comparative Technology Matrix Across Web LLM, Fine-Tuned, Cloud RAG, and ScholarRAG")\n    tech_matrix_data = ['),
    ('srs_table_data = [', 'add_table_caption("Table 3.1: Software Requirements Specification (Functional & Non-Functional Requirements)")\n    srs_table_data = ['),
    ('tech_stack_data = [', 'add_table_caption("Table 4.1: ScholarRAG Layered Implementation Technology Stack & Package Specifications")\n    tech_stack_data = ['),
    ('functional_tests_data = [', 'add_table_caption("Table 5.1: Comprehensive Functional Test Catalogue (20 Test Cases TC-01 to TC-20)")\n    functional_tests_data = ['),
    ('dense_retrieval_data = [', 'add_table_caption("Table 5.2: Dense Retrieval Performance Evaluation across 12 Statistical Metrics")\n    dense_retrieval_data = ['),
    ('cross_model_data = [', 'add_table_caption("Table 5.3: Cross-Model Generative Reasoning Benchmarks (Gemini 3.8, Claude 3.5, Grok-2, GPT-4o)")\n    cross_model_data = ['),
    ('latency_profile_data = [', 'add_table_caption("Table 5.4: Subsystem Latency Profile Breakdown across Isolated Pipeline Components")\n    latency_profile_data = ['),
    ('neg_grounding_data = [', 'add_table_caption("Table 5.5: Negative Grounding & Adversarial Hallucination Resistance Matrix")\n    neg_grounding_data = ['),
    ('risk_register_data = [', 'add_table_caption("Table 6.1: Comprehensive Operational Risk Register and Implemented Mitigations")\n    risk_register_data = [')
]

for old_s, new_s in table_captions:
    if old_s in code and new_s not in code:
        code = code.replace(old_s, new_s, 1)

with open(r'C:\Users\sdmal\OneDrive\Desktop\hunt\build_full_report.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Updated build_full_report.py successfully!')
