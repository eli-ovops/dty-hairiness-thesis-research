from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
source = root / '涤纶DTY毛丝论文-柳恩刘海军备用引用修订讨论稿-v0.2-2026-11-05.md'
target = root / '涤纶DTY毛丝论文-柳恩刘海军对抗审查优化讨论稿-v0.3-2026-11-05.md'
builder_source = root / '初稿核查-2026-11-05/生成备用稿引用修订阅读版v0.2.py'
builder_target = root / '初稿核查-2026-11-05/生成对抗审查优化阅读版v0.3.py'
assert not target.exists() and not builder_target.exists(), '目标文件已存在，停止覆盖'
text = source.read_text(encoding='utf-8')

def replace_once(old, new):
    global text
    assert text.count(old) == 1, f'替换目标数量不是1：{old[:60]}'
    text = text.replace(old, new, 1)

replace_once('柳恩与刘海军案例备用引用修订讨论稿 v0.2，2026-11-05', '柳恩与刘海军案例对抗审查优化讨论稿 v0.3，2026-11-05')
replace_once('研究采用文献与公开案例比较，没有本人企业现场试验或生产原始数据。作者、导师、学号、学校格式及AI使用披露按真实情况和学校要求另行核对，不在本稿虚构。', '研究采用文献与公开案例比较，没有本人企业现场试验或生产原始数据。此前内容由AI协助组织，本稿供本人核读资料、形成自己的分析和与导师讨论；不得直接冒充本人独立完成的研究成果。作者、导师、学号、学校格式及AI使用处理按真实情况和学校要求另行核对，不在本稿虚构。')
replace_once('本文采用文献研究和案例比较，讨论原丝状态、拉伸倍数、热箱温度、加工速度和假捻条件与毛丝的关系。', '本文采用文献研究和案例比较，按原料、设备、工艺、指标及未报告信息提取资料，讨论原丝状态、拉伸倍数、热箱温度、加工速度和假捻条件与毛丝的关系。')
replace_once('两项研究的材料、变量和毛丝记录方式不同，不能合并数据或推定通用工艺值。', '两项研究的材料、变量和毛丝记录方式不同；组间差值仅在同一原表内计算，不能合并数据或推定通用工艺值。')
replace_once('The comparison retains the reported equipment and conditions, separates defect records from other properties, and identifies missing sample and control information.', 'For each case, reported feed yarn, equipment, processing conditions and defect measures are recorded alongside missing sample and control information. Differences in percentage points are calculated only for groups within the same source table. The comparison separates direct defect observations from indirect measurements of other yarn properties.')
replace_once('The available studies do not fully report inspection quantities and independent repetitions, and the proposed measures have not been validated through the author\'s own production trials.', 'The available studies do not fully report inspection quantities, independent repetitions and common processing conditions. The photographs in the second case do not independently establish a seven-day threshold. The proposed measures have not been validated through the author\'s own production trials.')
replace_once('每日13:00在92号机193—198锭位取样，观察DTY的张力、强伸及毛丝情况。', '每日13:00在92号机193—198锭位取样，记录加工区T1加捻张力和T2解捻张力，并观察所得DTY的强伸性能及毛丝情况。')
replace_once('照片并未列出毛丝数量，不能由图估算改善百分比，也不能把6 d照片当作7 d组或认定后期毛丝率为零。', '照片并未列出毛丝数量，且背景和视角有所差异；原文未交代等长取样、图像标尺、照明和重复。图示不足以排除取样或成像差异，不能单凭四张照片独立验证7 d界限、估算改善百分比，也不能把6 d照片当作7 d组或认定后期毛丝率为零。')
replace_once('对照组中同时变化的条件未完整交代时，也不宜断定由单一参数导致全部差异。', '原文称其他条件一定，但其余共同条件的具体数值及是否发生变化未完整交代，不宜断定全部差异均由单一参数导致。')
replace_once('刘海军文的29 ℃是原丝平衡环境的平均温度，不能与第一热箱设定相比较。[1，第87、89页；2，第10页]', '刘海军文的29 ℃是原丝平衡环境的平均温度，不能与第一热箱设定相比较。[1，第87、89页；2，第10页] 柳文表4的189 ℃组为2.58%，表5中189 ℃且拉伸倍数1.695组为0.52%；两表其余共同条件未完整列出，不能将两值当作同一基线直接相减，也不能推断差异由某一个条件引起。[1，第89页表4—5]')
replace_once('作者认为在其研究范围内调整D/Y对改善毛丝的效果不明显，但未报告误差和独立重复。[1，第88页2.3节及表3]', '作者认为在其研究范围内调整D/Y对改善毛丝的效果不明显，但未报告误差和独立重复。[1，第88页2.3节及表3] 原文工况概述的D/Y范围为1.50—1.65，而表3另列1.70组，原因未说明；此处按原表记录并保留该差异。[1，第87—88页]')
old = '## 4.7 本章小结与局限\n\n柳文提供加工因素与毛丝降等率的组内记录；刘海军文提供另一种材料条件下原丝平衡时间与毛丝外观的定性观察。两项研究变量和评价口径不同，均不足以直接确定普遍适用的参数或验证拟议措施。'
new = '''## 4.7 本章小结与局限

为避免把不同指标合并，表4-3将本章观察、可用解释及证据缺口并列。该表是根据原文条件所做的资料整理，并非新增现场实验或效果验证。

表4-3 案例观察与解释边界

| 观察项目与来源 | 原文记录 | 可解释范围及缺口 |
| --- | --- | --- |
| 柳恩：拉伸倍数[1，第89页表5] | 第一热箱189 ℃，1.710与1.695组降等率为4.23%与0.52%。 | 同表组值相差3.71个百分点；检查量、重复和其他共同条件不完整，不推定通用临界值。 |
| 柳恩：第一热箱[1，第89页表4] | 192 ℃和189 ℃组降等率为6.47%和2.58%。 | 同表组值相差3.89个百分点；另需考虑僵丝，不与表5的189 ℃组视作同一基线。 |
| 柳恩：D/Y[1，第87—88页表3] | 各组记录未逐档单调；表中包含1.70。 | 可报告所列范围内组值；概述上限为1.65，差异原因与误差、独立重复未知。 |
| 刘海军：POY平衡时间[2，第10—11页图3] | 指定材料和环境下，作者结合照片描述毛丝外观变化。 | 只有定性观察，图中未列毛丝数或分母；取样及成像细节不足，不能独立验证7 d阈值。 |
| Pal：D/Y[11，第147、152页图6] | 特定工况下作者记录断单丝减少与紧点增加。 | 以所检丝长计数、材料与温度不同，不能和柳文按日降等率换算或相减。 |

柳文提供加工因素与毛丝降等率的组内记录；刘海军文提供另一种材料条件下原丝平衡时间与毛丝外观的定性观察。两项研究变量和评价口径不同，均不足以直接确定普遍适用的参数或验证拟议措施。'''
replace_once(old, new)
old = '5. **综合评估**：分别查看毛丝、断头、僵丝和物理性能等指标，连同样本和观察时长解释结果。只有取得可靠原始记录、定义清楚的分母及可比条件后，才讨论实际变化；不能直接沿用文献中的改善幅度。'
new = old + '''

表5-1示意如何把异常分布转化为待核问题。其情境为说明方法而设，不代表发生过的生产记录；每条检查方向都需要结合设备与现场条件验证。

表5-1 毛丝异常的条件化排查示例

| 假设的观察情境 | 可以先核对的资料 | 解释边界 |
| --- | --- | --- |
| 同批原丝对应多个锭位出现异常 | 原丝规格、批次、存放条件，以及同时采用的机台和工艺记录。 | 异常可能涉及共同条件，不能仅凭分布认定原丝为原因。[1，第88页；2，第10—11页] |
| 异常集中在个别锭位 | 异常锭位与相近锭位的丝路、接触部件、维护及工艺记录。 | 这是检查部件的线索，不能直接认定某个部件有故障。[4，第33—34页] |
| 一次调整前后质量指标变化 | 核对产品、批次、工况、检查数量和毛丝判定口径，并同时观察其他质量指标。 | 多个条件或检测范围同时变化时，不能将结果归于一个参数；缺少记录时只保留现象。 |

上述分支是根据已列文献及信息记录原则提出的待验证排查思路，不能等同于真实生产诊断结果。'''
replace_once(old, new)
replace_once('作者描述前3 d对应DTY毛丝外观逐渐改善，7 d后变化趋缓；图示照片为1、3、6和15 d，未列毛丝率。', '作者描述前3 d对应DTY毛丝外观逐渐改善，7 d后变化趋缓；图示照片为1、3、6和15 d，未列毛丝率，也不足以独立验证7 d界限。')
replace_once('有限文献不能证明统计显著性或通用工艺条件。', '刘文照片的背景和视角存在差异，取样及成像细节未充分交代，不能排除其对比较的影响。有限文献不能证明统计显著性或通用工艺条件。')
assert '张慧敏' not in text and '周文龙' not in text
refs = lambda s: re.findall(r'^\[\d+\].*$', s, re.M)
assert refs(text) == refs(source.read_text(encoding='utf-8')) and len(refs(text)) == 15
builder = builder_source.read_text(encoding='utf-8').replace(source.name, target.name)
builder = builder.replace('涤纶DTY毛丝论文-柳恩刘海军备用引用修订阅读版-v0.2-2026-11-05.docx', '涤纶DTY毛丝论文-柳恩刘海军对抗审查优化阅读版-v0.3-2026-11-05.docx')
assert target.name in builder and '优化阅读版-v0.3' in builder
assert text.count('with the first heater set at 189 °C.') == 1
text = text.replace('with the first heater set at 189 °C.', 'with the first heater set at 189 degrees Celsius.')
target.write_text(text, encoding='utf-8')
builder_target.write_text(builder, encoding='utf-8')
print(target)
print(builder_target)
