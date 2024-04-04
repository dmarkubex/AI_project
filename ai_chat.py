import streamlit as st
import requests
import fitz  # PyMuPDF

st.title("简历评分大师")
# 添加着重文字说明
st.markdown("远东简历大师能帮助您快速进行简历筛选，欢迎您的使用！")

user_avatar = "user_avatar.png"
ai_avatar = "ai_avatar.webp"

# 文件上传和PDF文本提取
uploaded_file = st.sidebar.file_uploader("上传简历（PDF格式）", type="pdf")
if uploaded_file is not None:
    # 当检测到新文件上传时，清空聊天历史记录
    st.session_state['chat_history'] = []

    resume_text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            resume_text += page.get_text()
else:
    resume_text = ""

input_text = st.text_area("输入您的消息", value=resume_text, height=100)

# 初始化 session_state 的值
if 'is_waiting' not in st.session_state:
    st.session_state['is_waiting'] = False
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if st.button("发送", disabled=st.session_state['is_waiting']):
    st.session_state['is_waiting'] = True
    payload = {
        "inputs": {},
        "query": input_text or resume_text,
        "response_mode": "blocking",
        "conversation_id": "",
        "user": "abc-123"
    }
    headers = {
        "Authorization": "Bearer app-Vs8TH4RchKdguzA2si7fSwGZ",
        "Content-Type": "application/json"
    }
    response = requests.post("https://ai.fegroup.cn:8800/v1/chat-messages", json=payload, headers=headers)

    if response.status_code == 200:
        try:
            response_data = response.json()
            ai_response = response_data.get("answer")
            if ai_response:
                chat_history = st.session_state['chat_history']
                chat_history.append({"role": "user", "content": input_text or "简历内容已发送"})
                chat_history.append({"role": "ai", "content": ai_response})
                st.session_state['chat_history'] = chat_history
        except ValueError:
            st.error("解析响应时发生错误：返回的内容不是有效的JSON格式。")
    else:
        st.error(f"无法获取AI回应，状态码：{response.status_code}, 响应：{response.text}")

    st.session_state['is_waiting'] = False

if st.session_state['is_waiting']:
    st.write("AI思考中...")

# 显示聊天记录和头像
for message in st.session_state.get('chat_history', []):
    col1, col2, col3 = st.columns([1, 5, 1])
    if message["role"] == "user":
        with col1:
            st.image(user_avatar, width=40)
        with col2:
            st.markdown(f"<div style='background-color: #f0f0f0; padding: 10px; border-radius: 10px;'>{message['content']}</div>", unsafe_allow_html=True)
    else:  # AI的回复
        with col2:
            st.markdown(f"<div style='background-color: #fde2e2; padding: 10px; border-radius: 10px;'>{message['content']}</div>", unsafe_allow_html=True)
        with col3:
            st.image(ai_avatar, width=40)
