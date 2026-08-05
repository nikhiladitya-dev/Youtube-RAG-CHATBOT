import streamlit as st


def render():

    st.markdown(
"""
<div class="sidebar-card">

<div style="text-align:center;">

<h1 style="margin-bottom:0;">🐼</h1>

<h1 style="margin-top:6px;margin-bottom:6px;style="font-family: 'Monoton', cursive;"">
PANDA CHATBOT
</h1>

<p style="margin-bottom:24px;">
Video Intelligence, Unlocked.</p>

</div>

<div class="info-card">

<div class="info-label">
🤖 AI Assistant
</div>

<div class="info-value">
Panda
</div>

</div>

<div class="info-card">

<div class="info-label">
🧠 Embeddings
</div>

<div class="info-value">
BAAI / bge-small-en-v1.5
</div>

</div>

<div class="info-card">

<div class="info-label">
⚙ Backend
</div>

<div class="info-value success">
🟢 Connected
</div>

</div>

<div class="info-card">

<div class="info-label">
🛠 Built With
</div>

<div class="tech-list">

<span>FastAPI</span>

<span>LangChain</span>

<span>ChromaDB</span>

<span>Hugging Face</span>

</div>

</div>

<p style="text-align:center;color:#888;font-size:13px;">
Version 1.0<br>
© 2026 PANDA CHATBOT. All rights reserved.
</p>

</div>
""",
        unsafe_allow_html=True,
    )