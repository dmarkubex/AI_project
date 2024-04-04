import time
from openai import OpenAI

client = OpenAI(
    api_key="sk-PDlvahz7X5OoaCzMZQN9gTf3mkulC8YKcvhlgRWj0BJYV0mT",  
    base_url="https://api.moonshot.cn/v1",
)

# 读取txt文件
with open(r'c:\Users\刁敏\Documents\Project\AI\input1.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 分割文本into段落
paragraphs = text.split('#####################')

# 批次大小
batch_size = 20

# 遍历段落列表,每个段落生成问题和答案
output_list = []

for i in range(0, len(paragraphs), batch_size):
    batch_paragraphs = paragraphs[i:i+batch_size]
    
    for paragraph in batch_paragraphs:
        try:
            # 使用API生成问题和答案
            completion = client.chat.completions.create(
                model="moonshot-v1-32k",
                messages=[
                    {"role": "system", "content": "你是一个问答生成器。给定一段文本,你会从用户实际使用中的各种情形出发提出不同的问题,并提供相应的答案，问题以'q:'开始，答案以'a:'开始，不要加序号。"},
                    {"role": "user", "content": f"请为以下文本生成10个问题和答案,涵盖不同方面:\n\n{paragraph}"}
                ],
                temperature=0.5,
            )
            
            qa_pairs = completion.choices[0].message.content.split('\n\n')
            
            for pair in qa_pairs:
                parts = pair.split('\n', 1)
                if len(parts) == 2:
                    question, answer = parts
                    output_list.append({
                        "instruction": "回答以下用户问题,仅输出答案。",
                        "input": question.replace('q: ', ''),
                        "output": answer.replace('a: ', '')
                    })
                else:
                    print(f"Skipping malformed QA pair: {pair}")

            # 在API请求之间添加延迟以限制并发
            time.sleep(1)  

        except Exception as e:
            print(f"Error generating questions and answers for paragraph: {paragraph}. Error: {str(e)}")
            
    # 输出结果到txt文件        
    with open(f'output_{i}.txt', 'w', encoding='utf-8') as f:
        f.write(str(output_list))

    print(f"Processed paragraphs {i} to {i+len(batch_paragraphs)-1}")

    # 清空输出列表to节省内存
    output_list = []

print("Processing completed.")