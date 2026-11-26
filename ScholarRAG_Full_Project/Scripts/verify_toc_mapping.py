import PyPDF2
import re

reader = PyPDF2.PdfReader(r'C:\Users\sdmal\OneDrive\Desktop\hunt\ScholarRAG_Project_Report.pdf')
print(f'Total pages in PDF: {len(reader.pages)}')

with open(r'C:\Users\sdmal\OneDrive\Desktop\hunt\build_full_report.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Parse toc_hierarchy
toc_matches = re.findall(r'\(\s*(\d+)\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\)', text)
print(f'Total TOC entries found: {len(toc_matches)}')

all_matched = True
for level, title, page_str in toc_matches:
    if page_str in ['ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']:
        pdf_page = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x'].index(page_str) + 1
    else:
        pdf_page = int(page_str) + 9 # Page 1 of body is PDF page 10
    
    page_txt = reader.pages[pdf_page - 1].extract_text()
    
    # Extract clean keywords
    clean_title = re.sub(r'^(CHAPTER\s+\d+:?|\d+\.\d+(\.\d+)?)\s*', '', title)
    words = [w for w in clean_title.split() if len(w) > 3 and w.lower() not in ['with', 'from', 'into', 'across', 'under', 'over']]
    
    found = any(w.lower() in page_txt.lower() for w in words[:3]) if words else True
    if not found:
        # Check adjacent pages
        prev_txt = reader.pages[pdf_page - 2].extract_text() if pdf_page > 1 else ''
        next_txt = reader.pages[pdf_page].extract_text() if pdf_page < len(reader.pages) else ''
        if any(w.lower() in prev_txt.lower() for w in words[:3]):
            print(f'[ADJACENT -1] {title:<55} claimed {page_str} (PDF {pdf_page}), actually on PDF {pdf_page-1} (Page {int(page_str)-1})')
            all_matched = False
        elif any(w.lower() in next_txt.lower() for w in words[:3]):
            print(f'[ADJACENT +1] {title:<55} claimed {page_str} (PDF {pdf_page}), actually on PDF {pdf_page+1} (Page {int(page_str)+1})')
            all_matched = False
        else:
            print(f'[CHECK]       {title:<55} claimed {page_str} (PDF {pdf_page})')
            all_matched = False

if all_matched:
    print('SUCCESS: ALL TOC ENTRIES PERFECTLY MATCH THEIR RESPECTIVE PAGES!')

# Now check figures
fig_matches = re.findall(r'\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\)', text[text.find('figures_list = ['):text.find('tables_list = [')])
print(f'\nTotal Figures checked: {len(fig_matches)}')
for f_num, f_desc, f_pg in fig_matches:
    pdf_page = int(f_pg) + 9
    p_txt = reader.pages[pdf_page - 1].extract_text()
    if f_num in p_txt:
        print(f'{f_num} correctly located on Page {f_pg} (PDF {pdf_page})')
    else:
        print(f'{f_num} NOT directly seen on Page {f_pg} (PDF {pdf_page})')

# Now check tables
tbl_matches = re.findall(r'\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\)', text[text.find('tables_list = ['):text.find('add_h1("LIST OF ABBREVIATIONS")')])
print(f'\nTotal Tables checked: {len(tbl_matches)}')
for t_num, t_desc, t_pg in tbl_matches:
    pdf_page = int(t_pg) + 9
    p_txt = reader.pages[pdf_page - 1].extract_text()
    if t_num in p_txt:
        print(f'{t_num} correctly located on Page {t_pg} (PDF {pdf_page})')
    else:
        print(f'{t_num} NOT directly seen on Page {t_pg} (PDF {pdf_page})')
