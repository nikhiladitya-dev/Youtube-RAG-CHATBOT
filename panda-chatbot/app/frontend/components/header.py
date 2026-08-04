import streamlit as st

from utils.constants import (
    APP_NAME,
    TAGLINE,
    APP_ICON,
)


def render():

    st.markdown(
f"""
<div class="header-card">

<h1>{APP_ICON} {APP_NAME}</h1>

<p>{TAGLINE}</p>

</div>
""",
unsafe_allow_html=True,
)