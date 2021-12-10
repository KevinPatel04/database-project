import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser
import matplotlib.pyplot as plt
from urllib.error import URLError

# pages view
import src.pages.home as home
import src.pages.all_tables_view as all_tables_view
import src.pages.course_list as course_list
import src.pages.exam_view as exam_view
import src.pages.roster_view as roster_view
import src.pages.exam_stats as exam_stats
import src.pages.exam_trends as exam_trends
import src.pages.students_attempts as student_attempts


PAGES = {
    "Home": home,
    "Course List": course_list,
    "View Roster": roster_view,
    "Exams": exam_view,
    "Exam Stats": exam_stats,
    "Exam Trends": exam_trends,
    "Student Attempts": student_attempts,
    "Display All Tables": all_tables_view
}

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    # with st.spinner(f"Loading {selection} ..."):
    page.write()
  
if __name__ == "__main__":
    main()
