from pathlib import Path
import json, re

base = Path(__file__).resolve().parent
work = base.parent.parent
existing = json.loads((work/'开题完善-2026-10-21/参考文献-正文排序.json').read_text(encoding='utf-8'))
by_number = {int(r['number_in_report']): r for r in existing}
mapping = {3: 7, 4: 1, 5: 2, 6: 5, 7: 6, 8: 9, 9: 11, 10: 15, 13: 8, 14: 10, 15: 14}
data = {target: dict(by_number[old]) for target,old in mapping.items()}
data.update({
    1: dict(author='柳恩 and 兰金良 and 许福明 and 陈郭兰',title='111 dtex/144 f涤纶DTY毛丝产生的原因分析及工艺优化',journal='合成纤维工业',year='2024',volume='47',number='3',pages='87--90'),
    2: dict(author='张慧敏 and 周文龙',title='44dtex/48f全消光细旦涤纶高弹DTY的开发',journal='现代工业与技术',year='2025',volume='2',number='4',pages='37--39',doi='10.12349/mit.v2i4.7169'),
    11: dict(author='Pal, S K and Gandhi, R S and Kothari, V K',title='Influence of texturing variables on the properties of cationic dyeable polyester yarns with different DMS salt content',journal='Indian Journal of Fibre & Textile Research',year='1997',volume='22',number='3',pages='146--153'),
    12: dict(author='Kurnia, Deni and Fakhrurroja, Hanif and Marno and Joniko',title='A hybrid pareto–fishbone and IoT-based monitoring framework for reducing DTY yarn defects',journal='Jurnal Polimesin',year='2025',volume='23',number='6',pages='881--888',doi='10.30811/jpl.v23i6.7678'),
})
output=[]
for i in range(1,16):
    record=data[i]; output.append(f'@article{{ref{i:02d},')
    for field in ('author','title','journal','year','volume','number','pages','doi'):
        value=record.get(field)
        if value: output.append(f'  {field} = {{{value}}},')
    output.append('}\n')
target=base/'初稿15篇-核查输入.bib'
if target.exists(): raise SystemExit('目标已存在：'+str(target))
target.write_text('\n'.join(output),encoding='utf-8')

draft=(base.parent/'涤纶DTY毛丝论文-完整结构讨论初稿-v0.2.md').read_text(encoding='utf-8')
body=draft.split('# 参考文献',1)[0]
refs=draft.split('# 参考文献',1)[1]
refnums=[int(x) for x in re.findall(r'^\[(\d+)\] ',refs,re.M)]
seen=set()
for match in re.finditer(r'\[([^\]]+)\]',body):
    group=match.group(1)
    if not re.match(r'^\d',group): continue
    for chunk in re.split(r'[;；]',group):
        segment=chunk.split('第',1)[0]
        for token in re.findall(r'\d+\s*[–—-]\s*\d+|\d+',segment):
            nums=[int(x) for x in re.findall(r'\d+',token)]
            if len(nums)==2 and nums[0]<=nums[1]<=15: seen.update(range(nums[0],nums[1]+1))
            elif len(nums)==1 and 1<=nums[0]<=15: seen.add(nums[0])
result={'references':refnums,'cited':sorted(seen),'missing':sorted(set(refnums)-seen),'extra':sorted(seen-set(refnums))}
(base/'编号对应检查.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
