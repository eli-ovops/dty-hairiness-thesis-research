from pathlib import Path
from copy import deepcopy
import json
from docx import Document

root=Path('/Volumes/EXTERNAL/论文/研究工作')
folder=root/'毛丝案例核验-2026-10-29'
old=root/'03-开题报告-提交准备稿-v0.2-2026-10-21.docx'
out=root/'03-开题报告-审阅稿-v0.3-2026-10-29.docx'
addition='Pal等对普通及改性聚酯加弹的研究同时考察断单丝和紧点；在该研究的特定条件下，D/Y比变化对两项指标呈现不同趋势，可用于分析质量指标之间的权衡[17]。'
ref='[17] PAL S K, GANDHI R S, KOTHARI V K. Influence of texturing variables on the properties of cationic dyeable polyester yarns with different DMS salt content[J]. Indian Journal of Fibre & Textile Research, 1997, 22(3): 146–153.'
d=Document(old)
targets=[p for row in d.tables[0].rows for cell in row.cells for p in cell.paragraphs if p.text.startswith('本人已有DTY工艺巡检')]
assert len(targets)==1
targets[0].runs[-1].text += addition
refs=[r for r in d.tables[0].rows if any(p.text.startswith('[16] 中华人民共和国') for c in r.cells for p in c.paragraphs)]
assert len(refs)==1
newrow=deepcopy(refs[0]._tr)
texts=newrow.xpath('.//w:t')
assert len(texts)==1
texts[0].text=ref
refs[0]._tr.addnext(newrow)
for p in d.paragraphs:
 if '提交准备稿 v0.2' in p.text:
  for run in p.runs:
   if '提交准备稿 v0.2' in run.text: run.text=run.text.replace('提交准备稿 v0.2    2026年10月21日','审阅稿 v0.3    2026年10月29日')
d.save(out)
data=json.loads((root/'开题完善-2026-10-21/开题报告实际填入内容.json').read_text())
for row in data['rows']:
 for e in row:
  if e['text'].startswith('本人已有DTY工艺巡检'): e['text']+=addition
refs=json.loads((root/'开题完善-2026-10-21/参考文献-正文排序.json').read_text())
fields=['\n'.join(e['text'] for e in row if e['kind'] not in ('heading',)) for row in data['rows'][:4]]
fields.append('\n'.join([r['formatted'] for r in refs]+[ref]))
(folder/'平台五栏内容-v0.3.json').write_text(json.dumps(fields,ensure_ascii=False,indent=2))
check=Document(out)
full='\n'.join(p.text for t in check.tables for row in t.rows for c in row.cells for p in c.paragraphs)
assert addition in full and ref in full
assert full.count('[17]')==2
print(out)
print('新增引用和书目各1处；五栏字数',*[len(x) for x in fields])
