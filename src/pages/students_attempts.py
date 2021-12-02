import streamlit as st
from app import *
from src import connection as conn

# pylint: disable=line-too-long

def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading ..."):
        st.markdown('## Quiz - Previous Attempts',unsafe_allow_html=True)
        col1, col2, col3,col4 = st.columns(4)
        try:
            with col1:
                term_select = st.selectbox('Select Term',sorted(conn.connect('select distinct term from exam',None)['term']))
        except:
            st.write('Not able to fetch your results.')    
        else:
            if term_select:
                try:
                    # print(term_select)
                    params_course = [str(term_select)]
                    with col2:
                        course_select = st.selectbox('Select Course id',sorted(conn.connect('select distinct cid from exam where term=%s',params_course)['cid']))
                except:
                    st.write("Not able to fetch your results")
                else:
                    if term_select and course_select:
                        try:
                            params_exam = (str(term_select),str(course_select))
                            with col3:
                                exam_select = st.selectbox('Select Exam id',sorted(conn.connect('select distinct eid from exam where term=%s and cid=%s',params_exam)['eid']))
                        except:
                                st.write("Not able to fetch your resutls")
                        else:
                            if term_select and course_select and exam_select:
                                try:
                                    params_suid = (str(term_select),str(course_select))
                                    with col4:
                                        suid_select = st.selectbox('Select Student id',sorted(conn.connect('select distinct suid from enroll_in where term=%s and cid=%s',params_suid)['suid']))    
                                    if term_select and course_select and exam_select and suid_select:
                                        try:
                                            params_attempts = (str(term_select),str(course_select),str(exam_select),str(suid_select))
                                            sql = "Select U.firstname  ||  '  '  || U.lastname as Name,U.email as Email,A.points as Points,A.adate as Submission_Date,A.atime as Submission_Time from appears_for A, users U, Exam E where E.eid=A.eid and A.suid = U.uid and term=%s and cid=%s and E.eid=%s and suid=%s order by submission_date desc,submission_time"
                                            table_df = conn.connect(sql,params_attempts)
                                            table_df["submission_time"] = table_df['submission_time'].astype(str)
                                            # print(table_df['submission_time'])
                                            st.dataframe(table_df)
                                        except:
                                            st.write("Not able to fetch your results.")
                                except:
                                    st.write("Not able to fetch your results.")
                            