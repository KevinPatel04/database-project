import streamlit as st
from src import connection as conn

# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading ..."):
        st.markdown(
            """## Quiz - Exams""",unsafe_allow_html=True
            )
        
        sql_all_terms = "SELECT DISTINCT term FROM course;"
        try:
            all_terms = conn.query_db_all(sql_all_terms)["term"].tolist()
            term = st.selectbox("Choose a term", all_terms)
        except:
            st.write("Sorry! Something went wrong with your query, please try again.")
        else:
            if term:
                sql_all_course_in_term = f"SELECT DISTINCT cid,course_title FROM course WHERE term='{term}';"
                try:
                    df = conn.query_db_all(sql_all_course_in_term)
                    all_courses = df["cid"]+': '+df["course_title"].tolist()
                    course = st.selectbox("Choose a course", all_courses)
                    cid = course.split(': ')[0]
                except:
                    st.write("Sorry! Something went wrong with your query, please try again.")
                else:
                    if term and course:
                        cid = course.split(': ')[0]
                        sql_table = f"SELECT eid FROM exam E WHERE E.cid = '{cid}' AND E.term = '{term}' ORDER BY due_date,due_time;"
                        try:
                            exams = conn.query_db_all(sql_table)['eid'].tolist()
                            exam = st.selectbox("Choose a exam", exams)
                            if exam and term and course:
                                sql_table = f"SELECT * FROM questions WHERE eid = {exam};"
                                try:
                                    df = conn.query_db_all(sql_table)
                                except:
                                    st.write("Sorry! Something went wrong with your query, please try again.")
                                else:
                                    st.dataframe(df)
                        except Exception as e:
                            st.write(
                                "Sorry! Something went wrong with your query, please try again."+str(e)
                            )