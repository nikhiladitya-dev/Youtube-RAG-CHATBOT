import streamlit as st


def render():

    st.markdown(
"""
<div class="success-card">

<h3>

✅ Video Ready

</h3>

<p>

Panda has successfully indexed the video.

You can now ask questions below.

</p>

</div>
""",
        unsafe_allow_html=True,
    )