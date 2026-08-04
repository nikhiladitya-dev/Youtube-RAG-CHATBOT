import streamlit as st
import time


def animate():

    placeholder = st.empty()

    steps = [

        ("⚡", "Extracting transcript..."),

        ("✂", "Chunking transcript..."),

        ("🧠", "Creating embeddings..."),

        ("👷", "Building vector database..."),

        ("🤖", "Initializing Panda..."),

        ("✅", "Ready to Chat"),

    ]

    for icon, message in steps:

        placeholder.markdown(
f"""
<div class="status-card">

<div class="status-icon">

{icon}

</div>

<div>

<h4 class="status-title">

{message}

</h4>

</div>

</div>
""",
            unsafe_allow_html=True,
        )

        time.sleep(2)

    placeholder.empty()