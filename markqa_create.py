import time
import pandas as pd
from openai import OpenAI

# OpenAI 客户端初始化
client = OpenAI(
    api_key="sk-PDlvahz7X5OoaCzMZQN9gTf3mkulC8YKcvhlgRWj0BJYV0mT",
    base_url="https://api.moonshot.cn/v1",
)

# 读取整个文件
file_path = r'C:\Users\刁敏\Documents\Project\AI\word\远股-数字信息制度.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# 分割文本为较小部分（示例：按照字符数分割）
# 假设每个部分约有1000个字符
text_parts = [text[i:i + 2000] for i in range(0, len(text), 1000)]

output_list = []

# 限制循环次数
max_iterations = 50
current_iteration = 0

for part in text_parts:
    if current_iteration >= max_iterations:
        break

    try:
        # API调用
        completion = client.chat.completions.create(
            model="moonshot-v1-32k",
            messages=[
                {"role": "system", "content": "你是一个问答生成器。给定一段文本,你会从用户实际使用中的各种情形出发提出不同的问题,并提供相应的答案，问题以'q:'开始，答案以'a:'开始，不要加序号。"},
                {"role": "user", "content": f"请为以下文本生成20个问题和答案,涵盖不同方面:\n\n{part}"}
            ],
            temperature=0.2,
        )

        qa_pairs = completion.choices[0].message.content.split('\n\n')
        for pair in qa_pairs[:20]:  # 只取前20个问答对
            parts = pair.split('\n', 1)
            if len(parts) == 2:
                question, answer = parts
                output_list.append((question.replace('q: ', ''), answer.replace('a: ', '')))

    except Exception as e:
        print(f"处理段落时出错：{e}")

    current_iteration += 1
    time.sleep(1)  # API调用之间的延迟

# 输出到文件
df = pd.DataFrame(output_list)
output_file_path = r'C:\Users\刁敏\Documents\Project\AI\word\output.xlsx'
df.to_excel(output_file_path, index=False)

print("处理完成。")
