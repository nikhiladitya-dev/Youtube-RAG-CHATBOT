import streamlit as st


def render(
    documents,
):

    if not documents:

        return

    st.markdown("### 📍 Sources")

    for index, doc in enumerate(
        documents,
        start=1,
    ):

        with st.expander(
            f"Source {index}"
        ):

            st.markdown(

                f"""
**Timestamp**

{doc["timestamp"]}

**Transcript**

{doc["content"]}
"""
            )