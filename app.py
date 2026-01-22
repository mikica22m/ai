import streamlit as st
import google.generativeai as genai
import time

# --- 1. SET UP THE PAGE ---
st.set_page_config(page_title="Lumora AI", page_icon="🔮", layout="wide")

# --- 2. LIQUID PURPLE GLASS iOS 26 CSS ---
st.markdown("""
    <style>
    /* Global Background: Deep Purple Fluid Gradient */
    .stApp {
        background: radial-gradient(circle at top right, #2D1B4E, #0A0514);
        color: #F3E8FF;
    }

    /* Glassmorphic Chat Containers with Purple Tint */
    div[data-testid="stChatMessage"] {
        background: rgba(147, 51, 234, 0.07);
        backdrop-filter: blur(25px) saturate(200%);
        -webkit-backdrop-filter: blur(25px) saturate(200%);
        border: 1px solid rgba(192, 132, 252, 0.2);
        border-radius: 28px;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }
    
    /* Liquid Sidebar - Dark Purple Glass */
    [data-testid="stSidebar"] {
        background: rgba(15, 5, 25, 0.7) !important;
        backdrop-filter: blur(40px);
        border-right: 1px solid rgba(192, 132, 252, 0.15);
    }

    /* Buttons: Neon Purple Glow */
    .stButton>button {
        background: rgba(168, 85, 247, 0.2);
        border: 1px solid rgba(192, 132, 252, 0.4);
        border-radius: 16px;
        backdrop-filter: blur(12px);
        color: #E9D5FF;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stButton>button:hover {
        background: rgba(168, 85, 247, 0.4);
        border: 1px solid #C084FC;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.5);
        transform: translateY(-2px);
    }

    /* Floating Input: Ultra-modern Purple Glass */
    .stChatInputContainer {
        background: transparent !important;
        padding-bottom: 30px;
    }
    .stChatInputContainer > div {
        background: rgba(88, 28, 135, 0.15) !important;
        backdrop-filter: blur(25px);
        border-radius: 35px !important;
        border: 1px solid rgba(192, 132, 252, 0.3) !important;
    }

    /* Titles and Text */
    h1 { font-weight: 800; letter-spacing: -1px; color: #F3E8FF; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONFIGURE API (High Speed Flash) ---
AI_NAME = "Lumora AI"
AI_AVATAR = "https://cdn-icons-png.flaticon.com/512/8943/8943377.png" # Purple bot icon

genai.configure(api_key="AIzaSyAV0MyY2C_7ftOnUn1K0qrB-j7YqR--wjA") # Use your actual key
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 4. SESSION STATE FOR CHATS ---
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

def start_new_chat():
    new_id = str(time.time())
    st.session_state.chats[new_id] = {"title": "New Session", "messages": []}
    st.session_state.current_chat_id = new_id

if not st.session_state.chats:
    start_new_chat()

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("## 🔮 Lumora OS")
    if st.button("➕ New Chat", use_container_width=True):
        start_new_chat()
        st.rerun()
    
    st.divider()
    st.markdown("### History")
    for chat_id, chat_data in reversed(list(st.session_state.chats.items())):
        if st.button(f"🟣 {chat_data['title']}", key=chat_id, use_container_width=True):
            st.session_state.current_chat_id = chat_id
            st.rerun()

# --- 6. CHAT INTERFACE ---
current_chat = st.session_state.chats[st.session_state.current_chat_id]
st.title(current_chat["title"])

for message in current_chat["messages"]:
    avatar = AI_AVATAR if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- 7. INPUT & FASTEST STREAMING ---
if prompt := st.chat_input("What's on your mind?"):
    current_chat["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Quick Title Update
    if current_chat["title"] == "New Session":
        current_chat["title"] = prompt[:20] + "..." if len(prompt) > 20 else prompt

    # Real-time Streaming
    with st.chat_message("assistant", avatar=AI_AVATAR):
        placeholder = st.empty()
        full_text = ""
        
        # Flash model for speed
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                full_text += chunk.text
                placeholder.markdown(full_text)
        
    current_chat["messages"].append({"role": "assistant", "content": full_text})