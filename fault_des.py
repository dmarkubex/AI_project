from zhipuai import ZhipuAI

machine_name = "特种电缆一厂三楼4#70挤塑机"
text_description ="特种电缆一厂三楼4#70挤塑机线路老化、绝缘破坏--吹干机不动作故障经过组合维修--线路老化处理。已维修"

# Initialize ZhipuAI client
client = ZhipuAI(api_key="2c73c724a105a9661f1b37902e9b09ee.VqRHCphCjnmpCVTV")

# Generate standardized description using ZhipuAI
response = client.chat.completions.create(
        model="glm-4",
        messages=[
                {"role": "system", "content": "你是一个严谨的设备故障知识管理员"},
                {"role": "user", "content": f"请你作为设备故障知识管理员，严格按照{text_description}的信息回答问题，回答问题的格式要符合要求"},
                {"role": "user", "content": f"对{machine_name}的故障进行分析后进行分类，长度限制为40个字，只给出具体故障类型，如果有多个故障类型，请进行合并，不要进行详细和补充说明"},     
        ],
)
standardized_description =  response.choices[0].message.content

print(standardized_description)



docker run --name one-api -d --restart always -p 13000:3000 -e SQL_DSN="datauser:Dkyo198246@@tcp(10.1.90.179:3306)/oneapi" -e TZ=Asia/Shanghai -v /home/ubuntu/data/one-api:/data justsong/one-api:0.5.11

docker run -e XINFERENCE_MODEL_SRC=modelscope -p 6006:9997 --gpus all xprobe/xinference:v0.82 xinference-local -H 0.0.0.0 --log-level debug