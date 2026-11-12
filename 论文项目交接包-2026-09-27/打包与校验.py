from pathlib import Path, PurePosixPath
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO
from hashlib import sha256
import shutil
import subprocess
import re
from lxml import etree
from pypdf import PdfReader

root = Path(__file__).resolve().parent
source = Path('/Users/USER/Downloads')
names = [
    '4-宁波工程学院高等学历继续教育本科毕业论文告知书27届（最终稿）.docx',
    '毕业论文（设计）模板27届.zip',
    '2-关于做好2027届本科学生毕业论文（设计）工作的通知.pdf',
    '宁工发〔2025〕104号关于印发《宁波工程学院成人高等教育学士学位授予工作实施细则》的通知.pdf',
]
output = source / '曹子建-宁波工程学院2027届论文项目交接包-2026-09-27.zip'
if output.exists():
    raise FileExistsError(output)
original = root / '原始材料'
expanded = root / '展开模板'
original.mkdir(exist_ok=True)
expanded.mkdir(exist_ok=True)
for name in names:
    target = original / name
    if not target.exists():
        shutil.copy2(source / name, target)
    assert sha256(target.read_bytes()).digest() == sha256((source / name).read_bytes()).digest()

with ZipFile(original / names[1]) as archive:
    assert archive.testzip() is None
    for info in archive.infolist():
        if info.is_dir():
            continue
        name = info.filename
        if not info.flag_bits & 0x800:
            try:
                name = name.encode('cp437').decode('gbk')
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass
        member = PurePosixPath(name)
        if member.is_absolute() or '..' in member.parts:
            raise ValueError(name)
        target = expanded / member.name
        if target.exists():
            raise FileExistsError(target)
        target.write_bytes(archive.read(info))
assert len(list(expanded.iterdir())) == 7

text = ['原文辅助提取。图片、嵌入公式、图形文字和版式可能遗漏。以原件为准。\n']
for path in [original / names[0], original / names[2], original / names[3], *sorted(expanded.iterdir())]:
    text.append('\nFILE: ' + path.name)
    if path.suffix == '.pdf':
        for index, page in enumerate(PdfReader(path).pages, 1):
            text.append(f'\nPAGE {index}\n' + (page.extract_text() or '[无可提取文字]'))
    elif path.suffix == '.doc':
        result = subprocess.run(['/usr/bin/textutil', '-convert', 'txt', '-stdin', '-stdout', '-format', 'doc'], input=path.read_bytes(), capture_output=True, check=True)
        text.append(result.stdout.decode('utf-8'))
    elif path.suffix in ('.docx', '.pptx'):
        with ZipFile(path) as archive:
            if path.suffix == '.docx':
                document = etree.fromstring(archive.read('word/document.xml'))
                for para in document.xpath('//*[local-name()="p"]'):
                    text.append(''.join(para.xpath('.//*[local-name()="t"]/text()')))
                text.append('[告知书流程图请查看原DOCX；交接摘要已记录此前人工读取的流程。]')
            else:
                slides = sorted((n for n in archive.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)), key=lambda n: int(re.search(r'slide(\d+)', n).group(1)))
                for name in slides:
                    document = etree.fromstring(archive.read(name))
                    text.append('\n' + name + '\n' + ''.join(document.xpath('//*[local-name()="t"]/text()')))
(root / '03-原文提取参考.txt').write_text('\n'.join(text), encoding='utf-8')
files = sorted(p for p in root.rglob('*') if p.is_file() and p.name != 'SHA256SUMS.txt')
(root / 'SHA256SUMS.txt').write_text(''.join(sha256(p.read_bytes()).hexdigest() + '  ' + p.relative_to(root).as_posix() + '\n' for p in files), encoding='utf-8')
files.append(root / 'SHA256SUMS.txt')
with ZipFile(output, 'x', compression=ZIP_DEFLATED) as archive:
    for path in files:
        archive.write(path, arcname=path.relative_to(root).as_posix())
with ZipFile(output) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist()) == len(files)
    for path in files:
        assert archive.read(path.relative_to(root).as_posix()) == path.read_bytes()
print('ZIP:', output)
print('FILES:', len(files), 'BYTES:', output.stat().st_size)
print('SHA256:', sha256(output.read_bytes()).hexdigest())
print('VERIFIED: four originals byte-identical; seven template files; every archive member checked; CRC passed')
