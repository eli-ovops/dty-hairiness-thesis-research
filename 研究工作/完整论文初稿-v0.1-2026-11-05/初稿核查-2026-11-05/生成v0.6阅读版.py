from pathlib import Path
import re
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

root = Path(__file__).resolve().parent.parent
src = root / '涤纶DTY毛丝论文-引用修订讨论稿-v0.4-2026-11-05.md'
dst = root / '涤纶DTY毛丝论文-引用修订讨论稿-v0.6-2026-11-05.docx'
if dst.exists():
    raise SystemExit(f'目标已存在，停止覆盖：{dst}')
doc = Document()
section = doc.sections[0]
section.top_margin = Cm(2.5)
section.bottom_margin = Cm(2.5)
section.left_margin = Cm(2.7)
section.right_margin = Cm(2.7)
normal = doc.styles['Normal']
normal.font.name = 'Songti SC'
normal.font.size = Pt(11)
normal._element.rPr.rFonts.set(qn('w:eastAsia'), 'Songti SC')
normal.paragraph_format.line_spacing = 1.25
normal.paragraph_format.space_after = Pt(3)
for style_name, size in [('Title', 18), ('Heading 1', 16), ('Heading 2', 13)]:
    style = doc.styles[style_name]
    style.font.name = 'Songti SC'
    style.font.size = Pt(size)
    style.font.color.rgb = RGBColor.from_string('000000')
    style._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), 'Songti SC')
    style.paragraph_format.keep_with_next = True
    style.paragraph_format.space_before = Pt(10)
    style.paragraph_format.space_after = Pt(6)
footer = section.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
field = OxmlElement('w:fldSimple')
field.set(qn('w:instr'), 'PAGE')
footer._p.append(field)

def add_formatted(p, text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    fragments = re.split(r'(\*\*.*?\*\*)', text)
    for fragment in fragments:
        if not fragment:
            continue
        if fragment.startswith('**') and fragment.endswith('**'):
            p.add_run(fragment[2:-2]).bold = True
        else:
            p.add_run(fragment)

def cells(line):
    return [part.strip() for part in line.strip().strip('|').split('|')]

lines = src.read_text(encoding='utf-8').splitlines()
i = 0
first = True
while i < len(lines):
    line = lines[i].strip()
    if not line:
        i += 1
        continue
    if line.startswith('|'):
        group = []
        while i < len(lines) and lines[i].strip().startswith('|'):
            group.append(lines[i])
            i += 1
        rows = [cells(x) for x in group]
        rows = [r for r in rows if not all(re.fullmatch(r'[:\- ]+', x or '-') for x in r)]
        width = max(map(len, rows))
        table = doc.add_table(rows=0, cols=width)
        table.style = 'Table Grid'
        for row_i, row in enumerate(rows):
            out = table.add_row()
            if row_i == 0:
                trpr = out._tr.get_or_add_trPr()
                repeat = OxmlElement('w:tblHeader')
                repeat.set(qn('w:val'), 'true')
                trpr.append(repeat)
            for col_i, value in enumerate(row):
                p = out.cells[col_i].paragraphs[0]
                p.paragraph_format.line_spacing = 1.15
                add_formatted(p, value)
                for run in p.runs:
                    run.font.size = Pt(9.5)
                    if row_i == 0:
                        run.bold = True
        continue
    if line.startswith('# '):
        value = line[2:]
        if first:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_formatted(p, value)
            for run in p.runs:
                run.bold = True
                run.font.size = Pt(18)
            first = False
        else:
            p = doc.add_paragraph(style='Heading 1')
            if value.startswith('第') or value.startswith('参考文献'):
                p.paragraph_format.page_break_before = True
            add_formatted(p, value)
    elif line.startswith('## '):
        p = doc.add_paragraph(style='Heading 2')
        add_formatted(p, line[3:])
    elif line.startswith('### '):
        p = doc.add_paragraph(style='Heading 3')
        add_formatted(p, line[4:])
    else:
        p = doc.add_paragraph()
        add_formatted(p, line)
        if not (line.startswith('[') or line.startswith('表') or line.startswith('资料来源') or line.startswith('**')):
            p.paragraph_format.first_line_indent = Pt(22)
    i += 1

doc.core_properties.author = ''
doc.core_properties.title = '涤纶DTY加弹加工中毛丝的影响因素及控制措施研究（讨论初稿）'
doc.save(dst)
print(dst)
