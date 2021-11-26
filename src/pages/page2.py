import streamlit as st

# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading Page2 ..."):
        st.markdown(
            """## Quiz - Page2""",unsafe_allow_html=True
            )