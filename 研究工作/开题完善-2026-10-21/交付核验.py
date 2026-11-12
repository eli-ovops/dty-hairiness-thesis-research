"""Offline checks binding the final DOCX, bibliography and QA render. No network."""
from pathlib import Path
from zipfile import ZipFile
from collections import Counter
from datetime import datetime, timezone
import hashlib, json, re, unicodedata
from lxml import etree as E
from pypdf import PdfReader

root = Path(__file__).resolve().parent
doc = root.parent / '03-开题报告-提交准备稿-v0.2-2026-10-21.docx'
base = root.parent / '开题准备-2026-10-21/模板转换/（1）开题报告.docx'
original = root.parent.parent / '论文项目交接包-2026-09-27/展开模板/（1）开题报告.doc'
old = root.parent / '03-开题报告-讨论稿-v0.1-2026-10-21.docx'
qa = root / '校验'
pdf = root / 'Word预览-交付' / (doc.stem + '.pdf')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(original) == 'fe0bd31bffc463aee55ffde1e4b9c3d30a2ff5110bc7125a860f5d64ea003458'
assert sha(old) == '2dca806bf823b69113d2e0dda269aaa863c8791b615efc4a6f210e8bbe9439e8'
assert sha(base) == '4cd2b8ddb17106d294d707d4837e9482e63587226360e6ef1533db4e240ef8e0'
with ZipFile(doc) as z, ZipFile(base) as b:
    assert z.testzip() is None
    assert set(z.namelist()) == set(b.namelist())
    changed = [n for n in z.namelist() if z.read(n) != b.read(n)]
    assert set(changed) == {'word/document.xml', 'word/settings.xml'}
    for n in z.namelist():
        if n.endswith(('.xml', '.rels')): E.fromstring(z.read(n))
    tree = E.fromstring(z.read('word/document.xml'))
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
full = ''.join(tree.findall('.//w:t', ns)[i].text or '' for i in range(len(tree.findall('.//w:t', ns))))
actual = json.loads((root / '开题报告实际填入内容.json').read_text())
records = json.loads((root / '参考文献-正文排序.json').read_text())
for row in actual['rows']:
    for e in row: assert e['text'] in full
for r in records: assert r['formatted'] in full
body = '\n'.join(e['text'] for row in actual['rows'][:4] for e in row)
assert len(records) == 16
assert all(x in full for x in ['曹子建', '2531410010', '2025本化工春华1', '陈碧芬', '职称：________'])
teacher = ''.join(tree.findall('.//w:tbl/w:tr', ns)[-1].itertext())
assert teacher == '指导教师审核意见指导教师签名：________________年      月      日'
first_seen = []
for token in re.findall(r'\[([0-9,\u2011-]+)\]', body):
    for chunk in token.replace('\u2011', '-').split(','):
        nums = range(int(chunk.split('-')[0]), int(chunk.split('-')[1])+1) if '-' in chunk else [int(chunk)]
        for n in nums:
            if n not in first_seen: first_seen.append(n)
assert first_seen == list(range(1, 17)), first_seen
assert '\u2060' not in full  # No invisible word-joiner workaround in deliverable.

reader = PdfReader(pdf)
assert len(reader.pages) == 6
pdftext = '\n'.join(p.extract_text() or '' for p in reader.pages)
han = lambda s: ''.join(re.findall(r'[\u4e00-\u9fff]', s))
for row in actual['rows'][:4]:
    for e in row:
        if han(e['text']): assert han(e['text']) in han(pdftext), e['text'][:30]
norm = lambda s: re.sub(r'\s+', '', unicodedata.normalize('NFKC', s)).lower()
for r in records:
    if r.get('doi'): assert norm(r['doi']) in norm(pdftext), r['doi']
assert '\ufffd' not in pdftext
for n in range(1, 7): assert (root / f'Word预览-交付/page-{n}.png').is_file()

overlap_path = qa / '本地文字来源检查.json'
overlap = json.loads(overlap_path.read_text())
body_han = han(body)
grams = {body_han[i:i+18] for i in range(max(0, len(body_han)-17))}
for src in overlap['sources']:
    source = root / '全文' / src['source']
    textfile = source.with_suffix('.txt')
    assert sha(source) == src['source_sha256']
    chars = han(textfile.read_text())
    other = {chars[i:i+18] for i in range(max(0, len(chars)-17))}
    src['common_chinese_18grams'] = sorted(grams & other)
    src['source_text_sha256'] = sha(textfile)
    src['extracted_chinese_character_count'] = len(chars)
overlap['document_sha256'] = sha(doc)
overlap['checked_at'] = datetime.now(timezone.utc).isoformat()
overlap['limitations'] += ['English passages and cross-language reuse are not assessed by Chinese character matching']
overlap['limitations'] = list(dict.fromkeys(overlap['limitations']))
overlap_path.write_text(json.dumps(overlap, ensure_ascii=False, indent=2)+'\n')

online_path = qa / '提交准备稿引用在线核验.json'
online = json.loads(online_path.read_text())
assert online['verdict_line'] == 'PASS: 10/16 verified, 0 errors, 0 warnings (0 checks skipped)'
assert Counter(e['status'] for e in online['entries']) == {'VERIFIED': 10, 'PARSED_ONLY': 6}
assert {e['key'] for e in online['entries']} == {'source'+str(r['source_id']) for r in records}
for e in online['entries']:
    if e.get('resolved', {}).get('doi') if isinstance(e.get('resolved'), dict) else False:
        record = next(r for r in records if e['key'] == 'source'+str(r['source_id']))
        assert e['resolved']['doi'].lower() == record['doi'].lower()

audit = {
    'checked_at': datetime.now(timezone.utc).isoformat(),
    'document': str(doc), 'document_sha256': sha(doc), 'pdf_sha256': sha(pdf),
    'offline_structure_and_content_checks': 'PASS',
    'page_count': len(reader.pages),
    'hanzi_first_four_sections': len(han(body)), 'references': len(records),
    'reference_first_occurrence_order': first_seen,
    'recent_journal_articles_2022_2025': sum(2022 <= int(r['year']) <= 2025 and r.get('entry_type', 'article') == 'article' for r in records),
    'changed_zip_parts': changed,
    'source_template_and_v0_1_unchanged': True,
    'teacher_opinion_signature_date_blank': True,
    'qa_text_extraction': 'All first-four-section Chinese paragraph strings and listed DOIs present in six-page PDF',
    'visual_review': 'All six final PNG pages reviewed; cover, Chinese text, citation wrapping, tables, pagination, bibliography and blank teacher form checked',
    'preview_image_sha256': {f'page-{n}.png': sha(root / f'Word预览-交付/page-{n}.png') for n in range(1, 7)},
    'bibliography_sha256': sha(root / '参考文献-最终排序.bib'),
    'online_report_sha256': sha(online_path),
    'online_verdict_verbatim': online['verdict_line'],
    'online_limits': '10 selected DOIs; 6 parsed only and manually sourced; no canonical-instance cross-index scan; earlier default run aborted on 429',
    'literal_overlap_report_sha256': sha(overlap_path),
    'academic_and_submission_status': 'Prepared for student/advisor review; not uploaded, approved, formally plagiarism/AIGC-tested or defended',
    'remaining_limits': ['Updated 260922 school template not obtained', 'Direct quantitative broken-filament evidence remains limited', 'Some references abstract/metadata only', 'Student understanding and advisor review pending', 'Platform opening and deadline not refreshed this turn'],
}
(qa / '交付核验.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({k:audit[k] for k in ['offline_structure_and_content_checks','document_sha256','page_count','hanzi_first_four_sections','references','online_verdict_verbatim']}, ensure_ascii=False, indent=2))
