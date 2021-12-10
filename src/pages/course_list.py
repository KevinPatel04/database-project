import streamlit as st
from src import connection as conn

# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading ..."):
        st.markdown(
            """## Quiz - Course List""",unsafe_allow_html=True
            )
        st.info('List all the courses offered in a given term along with the instructors information and student enrollment count. Also, find the most popular course for a given term among students purely based on enrollment information.')
        sql_all_terms = "SELECT DISTINCT term FROM course;"
        try:
            all_terms = conn.query_db_all(sql_all_terms)["term"].tolist()
            term = st.selectbox("Choose a term", all_terms)
        except:
            st.write("Sorry! Something went wrong with your query, please try again.")
        else:
            if term:
                f"Display the Course List"

                sql_table = f"""SELECT C.cid course_id,course_title title,U.firstname || ' ' || U.lastname instructor,U.email instructor_email, COUNT(suid) students_enrolled 
                                FROM course C,users U, enroll_in EI
                                WHERE C.term='{term}' 
                                AND U.uid = C.instructor
                                AND EI.cid = C.cid
                                AND EI.term = C.term
                                GROUP BY C.cid,course_title,U.firstname || ' ' || U.lastname,U.email;"""
                try:
                    df = conn.query_db_all(sql_table)
                    st.dataframe(df)
                except:
                    st.write(
                        "Sorry! Something went wrong with your query, please try again."
                    )
                
                sql_most_popular_course = f"""SELECT EI.cid, course_title, COUNT(suid) max_enrollment
                                        FROM enroll_in EI, course C
                                        WHERE EI.term='{term}'
                                        AND EI.term = C.term
                                        AND EI.cid = C.cid
                                        GROUP BY EI.cid,course_title
                                        HAVING COUNT(suid) IN (SELECT MAX(R1.students_enrolled)
                                            FROM (SELECT EI.cid, COUNT(suid) students_enrolled
                                                FROM enroll_in EI
                                                WHERE EI.term='{term}'
                                                GROUP BY EI.cid
                                            ) R1
                                        );"""
                try:
                    df = conn.query_db_all(sql_most_popular_course)
                    lst = [f"{df.iloc[i]['cid']}: {df.iloc[i]['course_title']}" for i in range(len(df))]
                    most_popular_courses = ""
                    for i,elem in enumerate(lst):
                        if i==0:
                            most_popular_courses=elem
                        elif i==len(lst)-1:
                            most_popular_courses+=f", and {elem}"
                        else:
                            most_popular_courses+=f", {elem}"

                    st.markdown(f"""
                    The most popular course for **{term.upper()}** {'is' if len(lst)==1 else 'are'} **{most_popular_courses}**.
                    """,unsafe_allow_html=True)
                except:
                    st.write(
                        "Sorry! Something went wrong with your query, please try again."
                    )