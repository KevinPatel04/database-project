import streamlit as st

# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading Page1 ..."):
        st.markdown(
            """## Quiz - Page1""",unsafe_allow_html=True
            )