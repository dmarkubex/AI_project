import os
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import re

def extract_text_from_pdf(pdf_path):
    output_string = StringIO()
    with open(pdf_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    return output_string.getvalue()

def remove_header_footer(text):
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        if not re.match(r'^\s*-\s*\d+\s*-\s*$', line) and not line.startswith("远东智慧能源股份有限公司"):
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def is_table_line(line):
    return "|" in line

def split_text_into_segments(text, max_length=500):
    segments = []
    current_segment = ""
    lines = text.split("\n")
    in_table = False
    for line in lines:
        if is_table_line(line):
            if not in_table:
                if current_segment:
                    segments.append(current_segment)
                segments.append("TABLE-TABLE")
                current_segment = ""
                in_table = True
        else:
            if in_table:
                in_table = False
            sentences = re.split(r'([。！？])', line)
            sentences = [s for s in sentences if s.strip()]
            for i in range(0, len(sentences), 2):
                sentence = sentences[i] + (sentences[i + 1] if i + 1 < len(sentences) else "")
                if len(current_segment) + len(sentence) <= max_length:
                    current_segment += sentence
                else:
                    if current_segment:
                        segments.append(current_segment)
                    current_segment = sentence
            if sentences and not re.search(r'[。！？]$', current_segment):
                current_segment += sentences[-1]
    if current_segment:
        segments.append(current_segment)
    return segments

def process_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    cleaned_text = remove_header_footer(text)
    segments = split_text_into_segments(cleaned_text)
    result = ""
    prev_segment = ""
    for segment in segments:
        if segment != prev_segment:
            result += f"{segment}\n￥￥￥￥￥￥￥￥￥￥￥￥￥￥\n\n"
            prev_segment = segment
    return result

def write_to_txt(content, txt_path):
    with open(txt_path, 'w', encoding='utf-8') as file:
        file.write(content)

# 示例用法
pdf_path = "C:/Users/刁敏/Documents/Project/AI/pdf/员工手册.pdf"
txt_path = os.path.splitext(pdf_path)[0] + ".txt"

result = process_pdf(pdf_path)
write_to_txt(result, txt_path)
print(f"拆分后的段落已写入: {txt_path}")