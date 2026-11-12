from pathlib import Path
import re

base=Path(__file__).resolve().parent
folder=base.parent
src=folder/'涤纶DTY毛丝论文-完整结构讨论初稿-v0.2.md'
dst=folder/'涤纶DTY毛丝论文-完整结构讨论初稿-v0.3.md'
if dst.exists(): raise SystemExit('目标已存在，停止覆盖：'+str(dst))
s=src.read_text(encoding='utf-8')
chinese='''涤纶拉伸变形丝（DTY）加弹过程中，单丝断裂形成的毛丝可能影响产品外观和后道加工。本文采用文献研究与案例比较方法，梳理原丝状态、拉伸倍数、第一热箱温度、加工速度及假捻条件与毛丝的关系。柳恩等111 dtex/144 f DTY案例中，在第一热箱189℃时，拉伸倍数1.710和1.695两组的毛丝降等率分别为4.23%和0.52%；张慧敏、周文龙在全消光高弹DTY案例中记录了不同拉伸倍数和速度下的定性毛丝表现。两例产品及指标口径不同，不能直接合并或推广参数。基于文献，本文提出结合原丝、设备和工艺记录开展排查，并分别观察毛丝、断头、僵丝及产品性能。文献部分样本及重复信息未充分报告，所提措施尚未通过本人现场验证。'''
english='''Broken filaments may occur during the draw-texturing of polyester yarn and affect yarn appearance and subsequent processing. This study reviews published literature and compares documented cases to examine feed-yarn conditions, draw ratio, first-heater temperature, processing speed and false-twist settings. Direct records of broken filaments, qualitative observations and other yarn-quality indicators are distinguished. In the 111 dtex/144 f DTY case reported by Liu and co-authors, at a first-heater setting of 189 °C, the reported broken-filament downgrade rates were 4.23% and 0.52% at draw ratios of 1.710 and 1.695, respectively. Zhang and Zhou reported qualitative observations for a fully dull high-elasticity DTY product. Differences in materials, processing conditions and outcome definitions limit direct comparison.

Materials and observations were extracted with their reported equipment, process conditions and indicator definitions. Comparisons were made first between groups within each source; results from different sources were not averaged or treated as repeated experiments. Studies of tensile, crimp and dyeing performance were used to discuss quality trade-offs rather than to infer broken-filament rates. The cases support consideration of draw ratio and heater settings within the reported conditions, while oil content, speed and disc-to-yarn ratio require interpretation for each product and machine. A conditional approach to recording feed-yarn, equipment and process information is proposed, with broken filaments, end breaks and other quality indicators considered separately. The proposed measures have not been tested in the author's own production setting. Conclusions are limited by incomplete reporting of sample sizes, repetitions and controlled conditions in the source literature.'''
new,n=re.subn(r'(## 摘要\n\n).*?(\n\n\*\*关键词)',lambda m:m.group(1)+chinese+m.group(2),s,count=1,flags=re.S)
if n!=1: raise SystemExit('未找到唯一中文摘要')
new,n=re.subn(r'(## Abstract\n\n).*?(\n\n\*\*Key words:)',lambda m:m.group(1)+english+m.group(2),new,count=1,flags=re.S)
if n!=1: raise SystemExit('未找到唯一英文摘要')
new=new.replace('完整结构讨论稿 v0.2','完整结构讨论稿 v0.3',1)
old='[1] 柳恩, 兰金良, 许福明, 陈郭兰.'
if old not in new: raise SystemExit('未找到预期参考文献[1]')
new=new.replace(old,'[1] 柳恩, 兰金良, 许福明, 等.',1)
old='[12] KURNIA D, FAKHRURROJA H, MARNO, JONIKO.'
if old not in new: raise SystemExit('未找到预期参考文献[12]')
new=new.replace(old,'[12] KURNIA D, FAKHRURROJA H, MARNO, et al.',1)
with dst.open('x',encoding='utf-8') as out: out.write(new)
print('中文摘要汉字',len(re.findall(r'[\u4e00-\u9fff]',chinese)))
print('英文摘要词数（所有词，非实词）',len(re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*",english)))
print('已生成',dst)
