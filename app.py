import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

import src.pages.page1 as page1
import src.pages.page2 as page2
import src.pages.page3 as page3
import src.pages.page4 as page4

"""Main module for the streamlit app"""

PAGES = {
    "Page1": page1,
    "Page2": page2,
    "Page3": page3,
    "Page4": page4
}


def main():
    """Main function of the App"""
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        page.write()
  
if __name__ == "__main__":
    main()
