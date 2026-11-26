import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

doc = docx.Document()

# Section 1 (Prelim)
sec1 = doc.sections[0]
sec1.different_first_page_header_footer = True

pgNumType1 = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="lowerRoman" w:start="1"/>')
sec1._sectPr.append(pgNumType1)

footer1 = sec1.footer
p_f1 = footer1.paragraphs[0]
p_f1.alignment = WD_ALIGN_PARAGRAPH.CENTER
fld1 = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
p_f1._p.append(fld1)

doc.add_paragraph('Page 1: Cover')
doc.add_page_break()
doc.add_paragraph('Page 2: Certificate')
doc.add_page_break()
doc.add_paragraph('Page 3: Declaration')

# Section 2 (Main)
sec2 = doc.add_section(WD_SECTION.NEW_PAGE)
sec2.different_first_page_header_footer = False
sec2.header.is_linked_to_previous = False
sec2.footer.is_linked_to_previous = False

pgNumType2 = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="decimal" w:start="1"/>')
sec2._sectPr.append(pgNumType2)

footer2 = sec2.footer
p_f2 = footer2.paragraphs[0]
p_f2.alignment = WD_ALIGN_PARAGRAPH.CENTER
fld2 = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
p_f2._p.append(fld2)

doc.add_paragraph('Page 4 (Sec 2 Page 1): Chapter 1')
doc.add_page_break()
doc.add_paragraph('Page 5 (Sec 2 Page 2): Chapter 1 cont')

doc.save(r'C:\Users\sdmal\OneDrive\Desktop\hunt\test_page_num.docx')
print('Saved test docx')
