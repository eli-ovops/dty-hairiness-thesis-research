# 毛宁、Basu 全文与 Retraction Watch 续查

日期：2026-11-05；范围为备用讨论稿 v0.3 的两篇文献和 15 条参考文献的撤稿线索。仅记录本次实际获得的材料及所查数据，未提交论文。

## 全文与页码

- **[13] 毛宁等**：《假捻变形工艺对涤纶DTY物理及染色性能的影响研究》。[国家科技期刊平台详情页](https://opaj.napstic.cn/periodicalArticle/0120240200348783)显示 61—67,7；其[2024 年第 1 期目录](https://opaj.napstic.cn/periodical/407?activeIssue=001&activeYear=2024&prePage=1)及[万方同期期刊目录](https://sns.wanfangdata.com.cn/perio/sichou?issueNum=1&publishYear=2024&tabId=article)显示 61—67。2026-11-05 本次通过详情页点击下载，页面进入国家科技期刊平台注册登录界面。登录后能否下载及是否免费未知；等待用户自行登录，不接收密码或验证码。尚无全文，尾部“7”含义待核。
- **[14] Basu、Maity**：出版社[2024 年第 115 卷第 2 期目录](https://www.tandfonline.com/toc/tjti20/115/2)及[文章检索记录](https://www.tandfonline.com/doi/full/10.1080/00405000.2023.2200301)列 278—283 页，2023 年在线发表、2024 年卷期。出版社原页面上次打开 403，本次查询到的公开索引仍显示付费访问；[ResearchGate 条目](https://www.researchgate.net/publication/370277211_Effects_of_stabilising_overfeed_on_the_properties_of_draw_textured_polyester_yarns)显示可向作者请求全文而非公开附件。尚未获得合法可读全文，页码为出版社目录级核验，不是对原刊 PDF 的核验。
- 查询包括两篇中英文全题名、作者、DOI、出版社、机构库、维普和万方等可见搜索记录；结果仅支持上述入口和摘要，未证明免费全文不存在。未给作者或他人发消息、未付款，未绕过限制。

## Retraction Watch 数据核查

从 Crossref [公开说明](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/)及其[公告所列原始 CSV](https://community.crossref.org/t/changes-to-delivery-of-retraction-watch-metadata/12368)获取数据，在内存中读取 67,900,410 字节、73,627 条记录，SHA-256 `2d92c4a05eb1faca0862db3dafa1f9679b8214c1d5c4dd6a86b729838dacdc0e`；仅保存精简核查回执，没有保存整份数据。查询时间以回执记录为准。

1. 以本项目 15 条参考文献的原书目标题做统一大小写、全半角和标点处理后的精确匹配，并对 9 条已有 DOI 作原论文 DOI 精确匹配；未发现匹配记录。
2. 额外以柳恩、刘海军、李谷成原刊中的英文题名和毛宁平台英文题名进行匹配，亦未发现匹配。禄倩倩的英文检索题名取自公开 PDF 文件名，不能保证涵盖其他译法。
3. 核验字段时最初误把一项**撤稿通知 DOI** `10.2147/CMAR.S358886` 当成原论文 DOI 搜索，因此未命中；随后在同一数据快照定位该通知对应的**原论文 DOI** `10.2147/CMAR.S324920`，用原文 DOI 字段的同一规范化规则核实可匹配。保留失败和更正回执，不把第一项零结果解释为系统不存在记录。此对照仅检查字段映射，不能证明数据库覆盖完整。
4. 这是对 **Retraction Watch 当前快照**的指定字符串查询；不同译名、录入错误、无记录、未收录的中文期刊撤稿与更正均可能漏掉。未发现匹配不等于证明 15 篇均未撤稿。上轮 7 条 Crossref/OpenAlex 结果见 `备用稿参考文献全文页码与撤稿续核-2026-11-05.md`；[5]、[13] 的 DOI 在这两个索引的 404 仍不能当成撤稿结论。

回执均位于 `完整论文初稿-v0.1-2026-11-05/初稿核查-2026-11-05/`：`RetractionWatch标题DOI续查-2026-11-05.json`、`RetractionWatch中文文献英文题名续查-2026-11-05.json`、`RetractionWatch检索阳性对照-2026-11-05.json`、`RetractionWatch控制样本定位-2026-11-05.json`、`RetractionWatch阳性对照字段更正-2026-11-05.json`。

本次没有修改参考文献或论文正文；上一轮离线检查原始回执仍为 `VERDICT-LINE: FAIL: 0/15 verified, 1 errors, 0 warnings (0 checks skipped)`，其中一处为两篇不同中文论文的重复题名误报，不是本次 Retraction Watch 查询结果。邮箱联网核验脚本此前因用户选择不提供邮箱而未运行。
