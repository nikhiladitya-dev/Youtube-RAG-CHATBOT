import streamlit as st


def render_user(
    message: str,
):

    st.markdown(
f"""
<div class="message-row user-row">
<div class="message-card user-card">
<div class="message-header">
<span>👤 You</span>
</div>
<div class="message-body">
{message}
</div>
</div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_panda(
    message: str,
    sources: list | None = None,
):

    if sources is None:
        sources = []

    html = f"""
<div class="message-row assistant-row">
<div class="assistant-avatar">
🐼
</div>
<div class="message-card assistant-card">
<div class="message-header">
Panda
</div>
<div class="message-body">
{message}
</div>
"""

    if sources:

        html += """

<div class="sources-title">
📍 Sources
</div>
<div class="sources-container">

"""

        for source in sources:

            html += f"""

<div class="source-chip">
{source["timestamp"]}

</div>

"""

        html += """
</div>
"""

    html += """
</div>

</div>
"""

    st.markdown(
        html,
        unsafe_allow_html=True,
    )