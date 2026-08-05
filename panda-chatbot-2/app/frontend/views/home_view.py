import streamlit as st

from services.api_client import APIClient

from components.layout import render as render_layout
from components.sidebar import render as render_sidebar
from components.header import render as render_header
from components.process_video import render as render_process
from components.processing_status import animate
from components.success_card import render as render_success
from components.error_card import render as render_error
from components.conversation import render as render_conversation
from components.chat_input import render as render_chat_input

api = APIClient()


def render_home():

    if "video_ready" not in st.session_state:

        st.session_state.video_ready = False

    if "video_id" not in st.session_state:

        st.session_state.video_id = None

    left, right = render_layout()

    with left:

        render_sidebar()

    with right:

        render_header()

        url, process = render_process()

        if process:

            if not url.strip():

                render_error("Please enter a valid YouTube URL.")

            else:

                try:

                    animate()

                    response = api.process_video(url)

                    st.session_state.video_ready = True

                    st.session_state.video_id = response["video_id"]

                except Exception as e:

                    render_error(str(e))

            

        if st.session_state.video_ready:

            render_success()

            # Conversation will come here
            question = render_conversation()
            if question:

                st.session_state.messages.append({ "role": "user","content": question, "sources": []})
                response = api.chat(question=question, video_id=st.session_state.video_id,)
                st.session_state.messages.append({ "role": "assistant", "content": response["answer"], "sources": response["sources"] })

                st.rerun()