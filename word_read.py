import os
from io import StringIO
from docx import Document
import re

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def remove_header_footer(text):
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        if not re.match(r'^\s*-\s*\d+\s*-\s*$', line):  # Exclude page numbers
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def is_table_line(line):
    return "|" in line  # Basic table line detection

def split_text_into_segments(text, max_length=500):
    segments = []
    current_segment = ""
    lines = text.split("\n")
    in_table = False
    prev_segment = ""  # 添加一个变量来存储上一个段落
    for line in lines:
        if is_table_line(line):
            in_table = True  # Skip table lines
        else:
            if in_table:
                in_table = False  # End of table
            sentences = re.split(r'([。！？])', line)  # Split by Chinese punctuation
            sentences = [s for s in sentences if s.strip()]
            for i in range(0, len(sentences), 2):
                sentence = sentences[i] + (sentences[i + 1] if i + 1 < len(sentences) else "")
                if len(current_segment) + len(sentence) <= max_length:
                    current_segment += sentence
                else:
                    if current_segment:
                        if current_segment != prev_segment:  # 检查当前段落是否与上一个段落相同
                            segments.append(current_segment)
                            prev_segment = current_segment  # 更新上一个段落
                    current_segment = sentence
            if sentences and not re.search(r'[。！？]$', current_segment):
                current_segment += sentences[-1]  # Append last sentence if needed
    if current_segment and current_segment != prev_segment:  # 检查最后一个段落是否与上一个段落相同
        segments.append(current_segment)
    return segments

def process_docx(docx_path):
    text = extract_text_from_docx(docx_path)
    cleaned_text = remove_header_footer(text)
    segments = split_text_into_segments(cleaned_text)
    result = ""
    for segment in segments:
        result += f"{segment}\n￥￥￥￥￥￥￥￥￥￥￥￥￥￥\n\n"
    return result

def write_to_txt(content, txt_path):
    with open(txt_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Example usage
docx_path = "C:/Users/刁敏/Documents/Project/AI/word/远东电池-人力资源制度.docx"  # Replace with your Word path
txt_path = os.path.splitext(docx_path)[0] + ".txt"
result = process_docx(docx_path)
write_to_txt(result, txt_path)
print(f"拆分后的段落已写入: {txt_path}")