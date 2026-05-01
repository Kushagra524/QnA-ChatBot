import os
import time
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key:
    os.environ["GROQ_API_KEY"] = groq_api_key

langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
if langchain_api_key:
    os.environ["LANGCHAIN_API_KEY"] = langchain_api_key

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "QnA ChatBot with GROQ"

# Page Config
st.set_page_config(
    page_title="QnA ChatBot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0a0f;
    color: #e2e2e2;
}

/* Hide streamlit default elements */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 2rem;}

/* App background */
.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #0f0f1a 50%, #0a0a0f 100%);
}

/* Title */
.main-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.8rem;
    background: linear-gradient(90deg, #00d4ff, #7b2fff, #ff2d78);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.2rem;
    letter-spacing: -1px;
}

.sub-title {
    text-align: center;
    color: #555577;
    font-size: 0.9rem;
    font-family: 'Space Mono', monospace;
    margin-bottom: 2rem;
    letter-spacing: 2px;
}

/* Chat container */
.chat-container {
    max-height: 520px;
    overflow-y: auto;
    padding: 1rem;
    border-radius: 16px;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 1rem;
    scrollbar-width: thin;
    scrollbar-color: #7b2fff #0a0a0f;
}

/* User bubble */
.user-bubble {
    display: flex;
    justify-content: flex-end;
    margin: 0.8rem 0;
    animation: slideInRight 0.3s ease;
}
.user-bubble .bubble {
    background: linear-gradient(135deg, #7b2fff, #4a00c8);
    color: white;
    padding: 0.75rem 1.1rem;
    border-radius: 18px 18px 4px 18px;
    max-width: 70%;
    font-size: 0.95rem;
    box-shadow: 0 4px 20px rgba(123,47,255,0.3);
    line-height: 1.5;
}

/* Bot bubble */
.bot-bubble {
    display: flex;
    justify-content: flex-start;
    margin: 0.8rem 0;
    animation: slideInLeft 0.3s ease;
}
.bot-bubble .bubble {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(0,212,255,0.2);
    color: #e2e2e2;
    padding: 0.75rem 1.1rem;
    border-radius: 18px 18px 18px 4px;
    max-width: 70%;
    font-size: 0.95rem;
    box-shadow: 0 4px 20px rgba(0,212,255,0.08);
    line-height: 1.6;
}

/* Avatar */
.avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
    margin: 0 0.5rem;
}
.user-avatar { background: linear-gradient(135deg, #7b2fff, #4a00c8); }
.bot-avatar  { background: linear-gradient(135deg, #00d4ff22, #00d4ff44); border: 1px solid #00d4ff44; }

/* Typing animation */
.typing-indicator {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 0.75rem 1rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 18px 18px 18px 4px;
    width: fit-content;
}
.typing-dot {
    width: 8px; height: 8px;
    background: #00d4ff;
    border-radius: 50%;
    animation: typingBounce 1.2s infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

/* Input box */
.stTextInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(123,47,255,0.4) !important;
    border-radius: 12px !important;
    color: #e2e2e2 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: border 0.2s ease !important;
}
.stTextInput input:focus {
    border-color: #7b2fff !important;
    box-shadow: 0 0 0 2px rgba(123,47,255,0.2) !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, #7b2fff, #4a00c8) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(123,47,255,0.3) !important;
}
.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(123,47,255,0.5) !important;
}

/* Clear button */
.clear-btn button {
    background: rgba(255,45,120,0.15) !important;
    border: 1px solid rgba(255,45,120,0.4) !important;
    color: #ff2d78 !important;
    box-shadow: none !important;
}
.clear-btn button:hover {
    background: rgba(255,45,120,0.25) !important;
    box-shadow: 0 4px 15px rgba(255,45,120,0.2) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(10,10,20,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
section[data-testid="stSidebar"] * { color: #cccccc !important; }

/* Selectbox & Slider */
.stSelectbox select, .stSlider {
    background: rgba(255,255,255,0.04) !important;
}

/* Animations */
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(20px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes typingBounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
    30%            { transform: translateY(-8px); opacity: 1; }
}

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(123,47,255,0.4), transparent);
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a smart and helpful AI assistant. Respond clearly and concisely."),
    ("user", "Question: {question}")
])

# Generate Response
def generate_response(question, llm_model, temperature, max_tokens):
    llm = ChatGroq(
        model=llm_model,
        temperature=temperature,
        max_tokens=max_tokens
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"question": question})

# Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    llm_model = st.selectbox("🧠 Model", [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "openai/gpt-oss-120b"
    ])

    temperature = st.slider("🌡️ Temperature", 0.0, 1.0, 0.6, 0.1)
    max_tokens  = st.slider("📏 Max Tokens",  50,  1000, 300, 50)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(f"💬 **{len(st.session_state.chat_history)}** messages in history")

# Title
st.markdown('<div class="main-title">🤖 QnA ChatBot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">POWERED BY GROQ + LANGCHAIN</div>', unsafe_allow_html=True)

# Chat History Display
chat_html = '<div class="chat-container" id="chat-box">'
if not st.session_state.chat_history:
    chat_html += '<p style="text-align:center;color:#333355;font-family:Space Mono,monospace;margin-top:4rem;">Start a conversation below ↓</p>'
else:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            chat_html += f'''
            <div class="user-bubble">
                <div class="bubble">{msg["content"]}</div>
                <div class="avatar user-avatar">👤</div>
            </div>'''
        else:
            chat_html += f'''
            <div class="bot-bubble">
                <div class="avatar bot-avatar">🤖</div>
                <div class="bubble">{msg["content"]}</div>
            </div>'''
chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# Input + Buttons
col1, col2, col3 = st.columns([6, 1, 1])

with col1:
    user_input = st.text_input("", placeholder="Ask me anything...", label_visibility="collapsed")

with col2:
    send = st.button("Dump my Query")

with col3:
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    clear = st.button("Clear the Chat")
    st.markdown('</div>', unsafe_allow_html=True)

# Handle Send
if send and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Typing animation placeholder
    with st.spinner(""):
        typing_placeholder = st.markdown("""
        <div class="bot-bubble">
            <div class="avatar bot-avatar">🤖</div>
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>""", unsafe_allow_html=True)
        time.sleep(0.5)
        response = generate_response(user_input, llm_model, temperature, max_tokens)

    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.rerun()

elif send and not user_input.strip():
    st.warning("Please type a message first!")

# Handle Clear
if clear:
    st.session_state.chat_history = []
    st.rerun()

# Auto scroll to bottom
st.markdown("""
<script>
    const chatBox = document.getElementById('chat-box');
    if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;
</script>
""", unsafe_allow_html=True)

