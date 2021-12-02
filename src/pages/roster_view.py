import streamlit as st
from src import connection as conn

# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading ..."):
        st.markdown(
            """## Quiz - Course Roster""",unsafe_allow_html=True
            )
        col1, col2 = st.columns(2)
        sql_all_terms = "SELECT DISTINCT term FROM course;"
        try:
            all_terms = conn.query_db_all(sql_all_terms)["term"].tolist()
            with col1:
                term = st.selectbox("Choose a term", all_terms)
        except:
            st.write("Sorry! Something went wrong with your query, please try again.")
        else:
            if term:
                f"Display the Course List"
                
                sql_all_course_in_term = f"SELECT DISTINCT cid,course_title FROM course WHERE term = '{term}';"
                try:
                    df = conn.query_db_all(sql_all_course_in_term)
                    all_courses = df["cid"]+': '+df["course_title"].tolist()
                    with col2:
                        course = st.selectbox("Choose a course", all_courses)
                    cid = course.split(': ')[0]
                    sql_instructor_in_course = f"SELECT U.firstname || ' ' || U.lastname AS name FROM users U,course C WHERE U.uid = C.instructor AND C.cid = '{cid}' AND C.term = '{term}' LIMIT 1;"
                    instructor = conn.query_db_all(sql_instructor_in_course)['name'].iloc[0]
                except Exception as e:
                    st.write("Sorry! Something went wrong with your query, please try again."+str(e))
                else:
                    if term and course:
                        sql_table = f"SELECT U.firstname || ' ' || U.lastname AS name,U.email,U.username FROM course C, users U, enroll_in EI WHERE EI.suid=U.uid AND EI.cid = C.cid AND EI.term = C.term AND C.cid = '{cid}' AND C.term = '{term}' ORDER BY name;"
                        try:
                            df = conn.query_db_all(sql_table)
                            st.markdown(f"**Instructor:** {instructor}")
                            st.write("List of Students Enrolled:")
                            st.dataframe(df)
                        except:
                            st.write(
                                "Sorry! Something went wrong with your query, please try again."
                            )