import streamlit as st


def render(
    message: str,
):

    st.markdown(
f"""
<div class="error-card">

<h3>
❌ Something went wrong
</h3>

<p>

{message}

</p>

</div>
""",
        unsafe_allow_html=True,
    )