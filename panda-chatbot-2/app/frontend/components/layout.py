import streamlit as st


def render():

    left, right = st.columns(
        [1.15, 3.85],
        gap="large",
    )

    return left, right