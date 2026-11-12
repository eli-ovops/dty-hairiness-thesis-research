from pathlib import Path
import re

root = Path(__file__).resolve().parent
work = root.parent
target = root / '涤纶DTY毛丝论文-完整结构讨论初稿-v0.2.md'
if target.exists():
    raise SystemExit(f'目标已存在，停止以保护原稿：{target}')

parts = [(root / '01-前置内容与第一至三章.md').read_text(encoding='utf-8').rstrip()]
for fname, cut_at in [
    ('第四章-案例分析讨论稿-v0.1-2026-11-05.md', '## 本稿来源与后续核对'),
    ('第五章-毛丝控制措施讨论稿-v0.1-2026-11-05.md', '## 来源与本人理解检查'),
    ('第六章-结论与展望讨论稿-v0.1-2026-11-05.md', '## 来源与本人理解检查'),
]:
    source = (work / fname).read_text(encoding='utf-8')
    if cut_at not in source:
        raise SystemExit(f'未找到预期的来源标记：{fname}')
    source = source.split(cut_at, 1)[0].rstrip()
    source = re.sub(r'^\*\*状态：.*?\*\*[^\n]*\n+', '', source, flags=re.M)
    source = re.sub(r'\[([^\]]*(?:柳|张)[^\]]*)\]',
                    lambda m: '[' + m.group(1).replace('柳', '1').replace('张', '2') + ']', source)
    parts.append(source)

refs = '''# 参考文献（讨论稿，最终格式和使用状态待核）

[1] 柳恩, 兰金良, 许福明, 陈郭兰. 111 dtex/144 f涤纶DTY毛丝产生的原因分析及工艺优化[J]. 合成纤维工业, 2024, 47(3): 87–90.

[2] 张慧敏, 周文龙. 44dtex/48f全消光细旦涤纶高弹DTY的开发[J]. 现代工业与技术, 2025, 2(4): 37–39. DOI: 10.12349/mit.v2i4.7169. （版本时间及学校对来源的要求待进一步核对）

[3] ORTEGA M, SAYNISCH A, YURTSEVEN B M, et al. A Review on False-Twist Texturing[J]. Fibers, 2024, 12(4): 36. DOI: 10.3390/fib12040036.

[4] 李谷成, 周召勇. 涤纶DTY质量对织造的影响及改进[J]. 合成纤维, 2011, (3): 32–35, 40.

[5] 禄倩倩, 张凤鸣, 马剑斌, 等. 涤纶长丝油剂的国产化研究及应用进展[J]. 现代纺织技术, 2024, 32(5): 105–115. DOI: 10.19398/j.att.202310007.

[6] YILDIRIM K, ALTUN S, ULCAY Y. The Effect of First Heater Temperature on the Properties of False-Twist Textured Poly (Ethylene Terapthalate) Yarn[J]. Tekstil ve Konfeksiyon, 2009, 19(4): 286–290.

[7] CANBAZ KARAKAŞ H, DAYIOĞLU H. Influence of false-twist texturing parameters on the structural properties of polyester yarn[J]. Indian Journal of Fibre & Textile Research, 2005, 30(1): 37–41.

[8] STEPANOVIĆ J, ŠARAC T, TRAJKOVIĆ D, et al. Investigation of deformation properties of textured multifilament PES yarns[J]. Industria Textila, 2022, 73(4): 397–404. DOI: 10.35530/IT.073.04.202167.

[9] MAITY S, BASU B, MISHRA A. Comparative Performance of Textured Yarn Drawn through Apron and Godet in Draw Texturing Machine[J]. Tekstilec, 2024, 67(1): 56–67. DOI: 10.14502/tekstilec.67.2024005.

[10] FIDAN G, KORKMAZ Y, ÇELIK H İ. Investigation of the effects of filament fineness and disc type on yarn physical and mechanical properties of DTY polyester yarns[J]. Pamukkale University Journal of Engineering Sciences, 2023, 29(7): 783–789. DOI: 10.5505/pajes.2023.03271.

[11] PAL S K, GANDHI R S, KOTHARI V K. Influence of texturing variables on the properties of cationic dyeable polyester yarns with different DMS salt content[J]. Indian Journal of Fibre & Textile Research, 1997, 22(3): 146–153.

[12] KURNIA D, FAKHRURROJA H, MARNO, JONIKO. A hybrid pareto–fishbone and IoT-based monitoring framework for reducing DTY yarn defects[J]. Jurnal Polimesin, 2025, 23(6): 881–888. DOI: 10.30811/jpl.v23i6.7678.

[13] 毛宁, 卢宏庆, 蒋力明, 等. 假捻变形工艺对涤纶DTY物理及染色性能的影响研究[J]. 丝绸, 2024, 61(1): 61–67. DOI: 10.3969/j.issn.1001-7003.2024.01.008.

[14] BASU B, MAITY S. Effects of stabilising overfeed on the properties of draw textured polyester yarns[J]. The Journal of The Textile Institute, 2024, 115(2): 278–283. DOI: 10.1080/00405000.2023.2200301.

[15] FIDAN G, KORKMAZ Y, ÇELİK H İ. Effects of filament fineness and disc type of drawn textured polyester yarns on carpet resilience and appearance retention performance[J]. Journal of Industrial Textiles, 2022, 52: 15280837221130516. DOI: 10.1177/15280837221130516.

本表按首次出现排序，包含15篇期刊论文，其中部分仅核读所引用章节、摘要或片段；较早文献用于方法与证据背景。这不是15篇全文精读或最终引文核验通过。学校既有材料一般要求不少于15篇且外文不少于2篇，具体文献统计、近五年比例及是否接纳某一来源应由导师和最新要求确定。张文版本日期与学校接受情况待核；最终请检查参考文献类型、正文一一对应、DOI与撤稿状态。
'''
parts.append(refs.strip())
body = '\n\n'.join(parts) + '\n'
with target.open('x', encoding='utf-8') as out:
    out.write(body)
print('已生成', target)
