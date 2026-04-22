import zipfile
import xml.etree.ElementTree as ET
import sys

def extract_text_from_docx(docx_path):
    document_xml = ""
    with zipfile.ZipFile(docx_path, 'r') as z:
        document_xml = z.read('word/document.xml')
    
    root = ET.fromstring(document_xml)
    namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    texts = []
    for p in root.iterfind('.//w:p', namespaces):
        p_texts = []
        for elem in p.iterfind('.//w:t', namespaces):
            if elem.text:
                p_texts.append(elem.text)
        if p_texts:
            texts.append(''.join(p_texts))
            
    return '\n'.join(texts)

content = extract_text_from_docx(r'e:\prescription_system\Hospital_Prescription_System_PRD.docx')
with open(r'e:\prescription_system\prd.txt', 'w', encoding='utf-8') as f:
    f.write(content)
