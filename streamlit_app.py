import streamlit as st
import requests

# --- CONFIG ---
API_KEY = "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"
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"

st.set_page_config(page_title="Dream Analyzer Chatbot", page_icon="🌙", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    body {
        background-color: #000000;
        color: #00ffff;
    }
    .stApp {
        background-color: #000000;
    }
    .css-18e3th9 {
        background-color: #000000 !important;
    }
    .css-1cpxqw2 {
        color: #00ffff !important;
    }
    .stTextInput > div > div > input {
        background-color: #111111;
        color: #00ffff;
        border: 1px solid #00ffff;
    }
    .stChatMessage {
        background-color: #111111;
        border-left: 2px solid #00ffff;
        margin: 8px 0;
        padding: 10px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.title("🌙 Dream Analyzer")

# --- INITIAL MESSAGE STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a kind and insightful dream interpretation assistant. Greet the user warmly. Ask them to describe their dream in detail, and then provide a gentle and meaningful analysis from a psychological or emotional perspective."},
        {"role": "assistant", "content": "Hello dreamer 🌌\n\nI'm here to explore the depths of your dream with you. Please share your dream in as much detail as you remember — I'm listening."}
    ]

# --- DISPLAY MESSAGES ---
for msg in st.session_state.messages[1:]:  # skip initial system prompt
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- USER INPUT ---
if prompt := st.chat_input("Tell me about your dream..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("🔍 Interpreting the hidden messages in your dream..."):
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL,
            "messages": st.session_state.messages
        }

        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            st.chat_message("assistant").markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        else:
            st.error("Something went wrong: " + response.text)
