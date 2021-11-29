import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

import src.pages.all_tables_view as all_tables_view
import src.pages.course_list as course_list
import src.pages.exam_view as exam_view
import src.pages.roster_view as roster_view

"""Main module for the streamlit app"""

PAGES = {
    "Display All Tables": all_tables_view,
    "Course List": course_list,
    "Exams": exam_view,
    "View Roster": roster_view
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
