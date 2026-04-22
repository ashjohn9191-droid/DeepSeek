import streamlit as st
import requests
import json
from streamlit_mic_recorder import mic_recorder
from diffusers import StableDiffusionPipeline
import torch

# -----------------------------
# CONFIG
# -----------------------------

API_KEY = "YOUR_API_KEY"

st.set_page_config(page_title="Ashley AI", page_icon="🤖", layout="wide")

# -----------------------------
# UI STYLE
# -----------------------------

st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#eef2ff,#e0f7ff);
color:#111;
}

h1{
color:#0066ff;
text-align:center;
font-weight:700;
}

div.stChatMessage{
background:white;
border-radius:12px;
padding:12px;
margin-bottom:10px;
color:black;
box-shadow:0 2px 8px rgba(0,0,0,0.1);
}

[data-testid="stChatInput"] textarea{
background:white;
color:black;
border-radius:20px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------

st.markdown("""
<h1>⚡ Ashley AI</h1>
<p style='text-align:center;font-size:18px;color:#555'>
Next-Generation Futuristic AI Assistant
</p>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR SETTINGS
# -----------------------------

st.sidebar.title("⚙️ AI Settings")

model = st.sidebar.selectbox(
"Choose Model",
[
"x-ai/grok-3-mini",
"deepseek/deepseek-r1",
"openai/gpt-4o-mini"
]
)

# -----------------------------
# LOAD CHAT HISTORY
# -----------------------------

try:
    with open("history.json") as f:
        history = json.load(f)
except:
    history = []

if "messages" not in st.session_state:
    st.session_state.messages = history

# -----------------------------
# DISPLAY CHAT
# -----------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -----------------------------
# VOICE INPUT
# -----------------------------

voice = mic_recorder(
    start_prompt="🎤 Speak",
    stop_prompt="Stop recording"
)

if voice is not None:
    st.audio(voice["bytes"])

# -----------------------------
# CHAT INPUT
# -----------------------------

user_prompt = st.chat_input("Ask Ashley AI...")

# -----------------------------
# CHAT AI
# -----------------------------

if user_prompt:

    st.session_state.messages.append({"role":"user","content":user_prompt})

    with st.chat_message("user"):
        st.write(user_prompt)

    try:

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type":"application/json"
            },
            json={
                "model": model,
                "messages": st.session_state.messages
            }
        )

        result = response.json()
        reply = result["choices"][0]["message"]["content"]

    except:
        reply = "⚠️ API Error. Check API key or balance."

    st.session_state.messages.append({"role":"assistant","content":reply})

    with st.chat_message("assistant"):
        st.write(reply)

    with open("history.json","w") as f:
        json.dump(st.session_state.messages,f)

# -----------------------------

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Ashley AI", page_icon="⚡", layout="wide")

st.markdown("""
<h1 style='text-align:center;'>⚡ Ashley AI</h1>
<p style='text-align:center;font-size:18px;color:gray'>
Next-Generation Futuristic AI Assistant
</p>
""", unsafe_allow_html=True)

# ==============================
# API KEY
# ==============================

# ==============================
#import streamlit as st
#import requests

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Ashley AI", page_icon="⚡", layout="wide")

st.markdown("""
<h1 style='text-align:center;'>⚡ Ashley AI</h1>
<p style='text-align:center;font-size:18px;color:gray'>
Next-Generation Futuristic AI Assistant
</p>
""", unsafe_allow_html=True)

# ==============================
# API KEY
# ==============================

API_KEY = "YOUR_API_KEY"

# ==============================
# IMAGE GENERATION
# ==============================

prompt = st.text_input("Enter image prompt")

if st.button("Generate Image"):

    with st.spinner("Generating Image..."):

        url = "https://api.x.ai/v1/images/generations"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "grok-vision-beta",
            "prompt": prompt
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            st.error(response.text)

        else:
            try:
                data = response.json()
                image_url = data["data"][0]["url"]
                st.image(image_url)
            except:
                st.error("Image generation failed")
                st.write(response.text)
