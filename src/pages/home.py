import streamlit as st

# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading ..."):
        st.markdown(
            """
            <center>
            
            ## CS-GY 6083: Principles of Database Systems
            
            #### Project Title: Quiz Management System

            #### Team Members: Ansh Desai (asd9717) - Kevin Patel (krp6947)

            </center>
            """,unsafe_allow_html=True
        )
