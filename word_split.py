import os
import re
from docx import Document

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

def process_docx_with_paragraphs_separated(docx_path):
    text = extract_text_from_docx(docx_path)
    cleaned_text = remove_header_footer(text)
    
    # Split the text into lines
    lines = cleaned_text.split("\n")
    
    # Identify the start of the third page
    third_page_index = next((i for i, line in enumerate(lines) if re.match(r'^\s*-\s*3\s*-\s*$', line)), len(lines))
    
    # Separate the first two pages and the rest of the text
    first_two_pages = "\n".join(lines[:third_page_index])
    rest_of_text = "\n".join(lines[third_page_index:])
    
    # Split the rest of the text into paragraphs
    paragraphs = re.split(r'\n{2,}', rest_of_text)
    
    # Split each paragraph into sentences
    processed_paragraphs = []
    for paragraph in paragraphs:
        sentences = re.split(r'([。！？.!?])', paragraph)
        processed_sentences = []
        for i in range(0, len(sentences), 2):
            sentence = sentences[i].strip()
            if sentence:
                processed_sentences.append(sentence + (sentences[i + 1] if i + 1 < len(sentences) else ""))
        processed_paragraphs.append("￥￥￥￥￥￥".join(processed_sentences))
    
    # Combine the first two pages and the processed paragraphs
    result = first_two_pages + "￥￥￥￥￥￥" + "￥￥￥￥￥￥".join(processed_paragraphs)
    
    return result

def write_to_txt(content, txt_path):
    with open(txt_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Example usage (Commented out)
docx_path = "C:/Users/刁敏/Documents/Project/AI/word/远股-财务资产制度.docx"
txt_path = os.path.splitext(docx_path)[0] + ".txt"
result = process_docx_with_paragraphs_separated(docx_path)
write_to_txt(result, txt_path)
print(f"Processed text written to: {txt_path}")