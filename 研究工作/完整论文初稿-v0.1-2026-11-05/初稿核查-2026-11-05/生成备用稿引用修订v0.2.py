from pathlib import Path

root = Path(__file__).resolve().parent.parent
source = root / '涤纶DTY毛丝论文-柳恩刘海军备用讨论稿-v0.1-2026-11-05.md'
target = root / '涤纶DTY毛丝论文-柳恩刘海军备用引用修订讨论稿-v0.2-2026-11-05.md'
builder_source = root / '初稿核查-2026-11-05/生成柳恩刘海军备用阅读版.py'
builder_target = root / '初稿核查-2026-11-05/生成备用稿引用修订阅读版v0.2.py'
assert not target.exists() and not builder_target.exists(), '目标文件已经存在，停止覆盖'
text = source.read_text(encoding='utf-8')
replacements = [
    ('柳恩与刘海军案例备用讨论稿 v0.1，2026-11-05', '柳恩与刘海军案例备用引用修订讨论稿 v0.2，2026-11-05'),
    ('不同产品的热传递、丝束受力和质量要求可能不同。[3]', '不同产品的热传递、丝束受力和质量要求可能不同。[3，第3—5页]'),
    ('可为讨论上油、平滑性及集束等问题提供背景。[5，第105页]', '可为讨论上油、平滑性及集束等问题提供背景。[5，第105—106页]'),
    ('Pal等按所检丝长目视统计断单丝，单位为根/km。[11，第147页]', 'Pal等按所检丝长目视统计断单丝，图6以根/km表示。[11，第147页、第152页图6]'),
    ('其他资料用于解释工艺、质量指标及统计口径。[3–12]', '其他文献用于解释加弹工艺、油剂及纱线和织物性能等背景；[3–10,13–15] Pal等与Kurnia等的研究还提供不同的断单丝或缺陷统计口径。[11–12]'),
    ('本章依据两篇文献提出原丝、拉伸倍数、第一热箱温度、速度和假捻等方面的控制与排查思路。', '本章主要依据柳恩、刘海军两篇核心文献，并结合Pal等辅助研究，提出原丝、拉伸倍数、第一热箱温度、速度和假捻等方面的控制与排查思路。'),
    ('刘海军文原刊未见DOI，不以文章编号代替；最终请检查文献类型、正文对应、DOI及撤稿状态。', '刘海军文原刊未见DOI，不以文章编号代替。毛宁文的目录页码为61—67，平台详情另出现“61—67,7”，尾部含义仍待对照原刊；Basu和Maity文目前仅核摘要。最终请检查文献类型、正文对应、DOI及撤稿状态。'),
]
for old, new in replacements:
    assert text.count(old) == 1, f'替换目标数量不是1：{old}'
    text = text.replace(old, new, 1)
assert '张慧敏' not in text and '周文龙' not in text
builder = builder_source.read_text(encoding='utf-8')
builder = builder.replace(source.name, target.name)
builder = builder.replace('涤纶DTY毛丝论文-柳恩刘海军备用阅读版-v0.1-2026-11-05.docx', '涤纶DTY毛丝论文-柳恩刘海军备用引用修订阅读版-v0.2-2026-11-05.docx')
assert target.name in builder and '备用引用修订阅读版-v0.2' in builder
target.write_text(text, encoding='utf-8')
builder_target.write_text(builder, encoding='utf-8')
print(target)
print(builder_target)
