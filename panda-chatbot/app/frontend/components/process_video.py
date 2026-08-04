import streamlit as st


def render():

    st.markdown(
"""
<div class="card">

<h3 class="card-title">
🔗 YouTube Video
</h3>

<p class="card-subtitle">
Paste a YouTube URL below to begin chatting with the video...
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    url = st.text_input(
        "",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed",
    )

    process = st.button(
        "🚀 Process Video",
        use_container_width=True,
    )

    return url, process