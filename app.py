import streamlit as st
import requests

API_KEY = "YOUR_API_KEY"

st.set_page_config(
    page_title="Ashley AI",
    page_icon="🤖",
    layout="wide"
)

# DARK THEME CSS
st.markdown("""
<style>

/* Full black background */
.stApp{
background-color:black;
}

/* Make ALL text white */
html, body, [class*="css"]{
color:white !important;
}

/* Title style */
h1{
color:white;

text-align:center;
}

/* Chat message container */
[data-testid="stChatMessage"]{
background-color:#111111;
border-radius:15px;
padding:15px;
margin-bottom:10px;
}

/* AI response text */
[data-testid="stMarkdownContainer"]{
color:white !important;
}

/* Paragraph text */
p{
color:white !important;
}

/* Chat input */
[data-testid="stChatInput"] textarea{
background:#ff1493 !important;
color:white !important;
border-radius:25px;
border:none;
}

/* Placeholder */
textarea::placeholder{
color:white !important;
}

/* Remove header background */
[data-testid="stHeader"]{
background:transparent;
}

</style>
""", unsafe_allow_html=True)

st.title("🤖 Ashley AI Assistant")

# Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask Ashley AI anything...")

if user_input:

    st.session_state.messages.append({
        "role":"user",
        "content":user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    try:

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model":"deepseek/deepseek-r1",
                "messages": st.session_state.messages
            }
        )

        result = response.json()

        if "choices" in result:
            ai_reply = result["choices"][0]["message"]["content"]
        else:
            ai_reply = "⚠️ API Error: " + str(result)

    except Exception as e:
        ai_reply = str(e)

    st.session_state.messages.append({
        "role":"assistant",
        "content":ai_reply
    })

    with st.chat_message("assistant"):
        st.markdown(ai_reply)
