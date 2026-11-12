from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
src = root / "涤纶DTY毛丝论文-引用修订讨论稿-v0.4-2026-11-05.md"
dst = root / "涤纶DTY毛丝论文-对抗审查修订讨论稿-v0.5-2026-11-05.md"
if dst.exists():
    raise SystemExit(f"目标已存在：{dst}")
s = src.read_text(encoding="utf-8")

zh = ("涤纶拉伸变形丝（DTY）加工中，单丝断裂形成的毛丝可能影响产品外观和后道加工。"
      "本文采用文献研究和案例比较，分析原丝、拉伸倍数、热箱温度、速度及假捻条件与毛丝的关系。"
      "柳恩等案例中，第一热箱为189℃时，拉伸倍数1.710和1.695对应的毛丝降等率分别为4.23%和0.52%；"
      "张慧敏、周文龙案例提供了定性毛丝记录。Pal等研究中D/Y增大时断单丝减少、紧点增加。"
      "先在文献内比较组别并记录指标口径及缺失。各研究材料、工况和指标不同，不能合并数据或推广参数。本文提出结合原丝、设备和工艺记录排查，"
      "并兼顾毛丝、断头及其他性能。原文样本和重复信息不充分，拟议措施未经本人现场验证。")
en = ("Broken filaments formed during the draw-texturing of polyester yarn may affect yarn appearance and subsequent processing. "
      "This study reviews published literature and compares documented cases to examine how feed yarn, draw ratio, heater temperature, "
      "processing speed and false-twist conditions relate to broken filaments. In the case reported by Liu and co-authors, at a first-heater "
      "setting of 189 °C, broken-filament downgrade rates were 4.23% and 0.52% at draw ratios of 1.710 and 1.695, respectively. "
      "Zhang and Zhou provided qualitative observations for a fully dull high-elasticity product. In the study by Pal and co-authors, "
      "broken filaments decreased while tight spots increased as the disc-to-yarn speed ratio rose. "
      "For each case, the reported material, equipment, processing conditions and indicator definitions are recorded. "
      "Observations are compared first within the same source, and missing sample or control information is left unfilled. "
      "Direct defect records are distinguished from tensile, crimp and dyeing properties when considering overall quality. "
      "These observations were made under different materials, equipment and indicator definitions; they cannot be combined as one dataset "
      "or used to prescribe universal settings. A conditional inspection approach is proposed using records of feed yarn, equipment and process "
      "conditions, while broken filaments, end breaks and other quality properties are considered separately. Sample sizes and independent "
      "repetitions were not fully reported in the case literature, and the proposed measures have not been tested in the author's own production setting.")
s, n = re.subn(r"(?<=## 摘要\n\n).*?(?=\n\n\*\*关键词)", lambda m: zh, s, count=1, flags=re.S)
assert n == 1
s, n = re.subn(r"(?<=## Abstract\n\n).*?(?=\n\n\*\*Key words:)", lambda m: en, s, count=1, flags=re.S)
assert n == 1
s=s.replace("引用修订讨论稿 v0.4，2026-11-05","对抗审查修订讨论稿 v0.5，2026-11-05",1)

anchor="对每项拟使用资料，首先确认题名、作者、出版信息和可读范围"
assert s.count(anchor)==1
paragraph=("资料检索采用定向检索与后续补充相结合。2026年10月29日，围绕“涤纶 DTY 毛丝 加弹 工艺”、"
           "“涤纶 拉伸变形丝 毛丝 断单丝 质量”及“polyester drawn textured yarn broken filaments texturing”等"
           "五条查询，在Crossref进行一次2021—2026年范围的检索，原始返回25条，年份筛选和去重后保留6条候选；"
           "其中包含不相关结果，不能视为6篇均合格或全部参考文献均出自该次检索。"
           "之后结合期刊页面、原刊及合法取得的全文补充资料。该检索不是对所有数据库的穷尽，也不是系统综述。\n\n")
s=s.replace(anchor,paragraph+anchor,1)

anchor="张文表8列出了D/Y、K值、T2张力和卷曲收缩率"
assert s.count(anchor)==1
pal=("Pal等对普通及不同DMS盐含量的阳离子可染聚酯进行研究，在图6所列条件下，"
     "拉伸倍数为1.649、热箱接触时间为0.282 s，三种原丝对应的第一热箱温度分别为195、175和155℃。"
     "作者报告随D/Y增大，断单丝数减少而紧点增加，体现两项质量指标可能存在权衡。[11，第147页表1、第152页图6]"
     "柳文的D/Y分组记录则未呈现逐档单调变化。两项研究的材料、设备、工况及指标定义不同；"
     "Pal文的断单丝计数不能直接换算为柳文按日统计的毛丝降等率，也不能据此确立统一的D/Y变化方向。\n\n")
s=s.replace(anchor,pal+anchor,1)

s=s.rstrip()+"\n\n# 致谢\n\n【待本人根据实际经历撰写。】\n"

toc_start=s.index("## 目录（暂列，页码待最终排版生成）")
toc_end=s.index("# 第一章 绪论",toc_start)
headings=[]
for line in s[toc_end:].splitlines():
    if line.startswith("# "): headings.append(line[2:])
    elif line.startswith("## "): headings.append("　　"+line[3:])
toc="## 目录（阅读版，页码以Word最终排版为准）\n\n"+"\n\n".join(headings)+"\n\n"
s=s[:toc_start]+toc+s[toc_end:]

with dst.open("x",encoding="utf-8") as f:f.write(s)
print("已创建",dst)
print("中文摘要非空格字符",len(re.sub(r"\s","",zh)),"汉字",len(re.findall(r"[\u4e00-\u9fff]",zh)))
print("英文摘要空格分词数",len(en.split()),"英文实词数未计算")
