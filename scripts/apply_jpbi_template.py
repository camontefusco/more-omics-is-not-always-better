from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree

template = Path('/Users/cmontefusco/Downloads/jpbi-template.dot')
source = Path('/Users/cmontefusco/Coding_projects/more-omics-is-not-always-better/submission/jpbi_manuscript_package.docx')
output = source.with_name('jpbi_manuscript_package_template.docx')
tmp_template = Path('/tmp/jpbi_template_docx.docx')
NS = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def read_zip(path):
    with ZipFile(path) as z:
        return {i.filename:z.read(i.filename) for i in z.infolist()}

t = read_zip(template)
t['[Content_Types].xml'] = t['[Content_Types].xml'].replace(b'application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml', b'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml')
with ZipFile(tmp_template,'w',ZIP_DEFLATED) as z:
    for name,data in t.items(): z.writestr(name,data)
s = read_zip(source)
doc = etree.fromstring(s['word/document.xml'])
for p in doc.xpath('//w:body/w:p', namespaces=NS):
    text = ''.join(p.xpath('.//w:t/text()', namespaces=NS)).strip()
    pPr = p.find('w:pPr', NS)
    if pPr is None:
        pPr = etree.Element('{%s}pPr' % NS['w']); p.insert(0,pPr)
    old = pPr.find('w:pStyle', NS)
    if old is not None: pPr.remove(old)
    sid = 'MDPI_3.1_text'
    if text == 'Abstract': sid='MDPI_1.7_abstract'
    elif text.startswith('Keywords:'): sid='MDPI_1.8_keywords'
    elif text == 'Carlos Victor Montefusco-Pereira': sid='MDPI_1.3_authornames'
    elif text.startswith('When More Omics Is Not Always Better'): sid='MDPI_1.2_title'
    elif text and text[0].isdigit() and '. ' in text:
        sid='MDPI_2.1_heading1' if text.count('.')==1 else ('MDPI_2.2_heading2' if text.count('.')==2 else 'MDPI_2.3_heading3')
    ps=etree.Element('{%s}pStyle'%NS['w']); ps.set('{%s}val'%NS['w'],sid); pPr.insert(0,ps)
s['word/styles.xml'] = t['word/styles.xml']
with ZipFile(output,'w',ZIP_DEFLATED) as z:
    for name,data in s.items():
        if name == 'word/document.xml': data=etree.tostring(doc,xml_declaration=True,encoding='UTF-8',standalone=True)
        z.writestr(name,data)
print(output)
