import streamlit as st


def render():

    question = st.chat_input(
        "Ask Panda anything about this video..."
    )

    return question