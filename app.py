import streamlit as st
import google.generativeai as genai

# --- 1. SET UP THE PAGE ---
st.set_page_config(page_title="My Gemini AI", page_icon="✨", layout="centered")

# --- 2. CUSTOM GEMINI-STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: white; }
    .stChatMessage { border-radius: 15px; padding: 10px; margin-bottom: 10px; }
    .stChatInputContainer { padding-bottom: 20px; }
    h1 { font-family: 'Google Sans', sans-serif; font-weight: 400; color: #e3e3e3; }
    </style>
    """, unsafe_allow_html=True)

st.title("Hello, I'm your AI")

# --- 3. CONFIGURE API ---
# Replace with your actual key
genai.configure(api_key="AIzaSyAj_qYn99MGPRnq5jxqBHpZyYBPwGhuqAo")
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 4. SESSION STATE (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. CHAT INPUT ---
if prompt := st.chat_input("Enter a prompt here"):
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Call Gemini
        response = model.generate_content(prompt)
        full_response = response.text
        message_placeholder.markdown(full_response)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})