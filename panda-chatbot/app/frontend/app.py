import streamlit as st

from utils.helpers import load_css
from views.home_view import render_home


st.set_page_config(
    page_title="PANDA CHATBOT",
    page_icon="🐼",
    layout="wide",
)

load_css()

render_home()