import streamlit as st

# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading Page4 ..."):
        st.markdown(
            """## Quiz - Page4""",unsafe_allow_html=True
            )