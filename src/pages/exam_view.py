import streamlit as st
from src import connection as conn

# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading ..."):
        st.markdown(
            """## Quiz - Exams""",unsafe_allow_html=True
            )
        col1,col2,col3 = st.columns(3)
        sql_all_terms = "SELECT DISTINCT term FROM course;"
        try:
            all_terms = conn.query_db_all(sql_all_terms)["term"].tolist()
            with col1:
                term = st.selectbox("Choose a term", all_terms)
        except:
            st.write("Sorry! Something went wrong with your query, please try again.")
        else:
            if term:
                sql_all_course_in_term = f"SELECT DISTINCT cid,course_title FROM course WHERE term='{term}';"
                try:
                    df = conn.query_db_all(sql_all_course_in_term)
                    all_courses = df["cid"]+': '+df["course_title"].tolist()
                    with col2:
                        course = st.selectbox("Choose a course", all_courses)
                    cid = course.split(': ')[0]
                except:
                    st.write("Sorry! Something went wrong with your query, please try again.")
                else:
                    if term and course:
                        cid = course.split(': ')[0]
                        sql_table = f"SELECT eid FROM exam E WHERE E.cid = '{cid}' AND E.term = '{term}' ORDER BY due_date,due_time;"
                        try:
                            exams = conn.query_db_all(sql_table)
                            exams_eid = exams['eid'].tolist()
                            with col3:
                                exam_eid = st.selectbox("Choose a exam", exams_eid)
                            if exam_eid and term and course:
                                sql_table = f"SELECT * FROM questions WHERE eid = {exam_eid};"
                                try:
                                    df = conn.query_db_all(sql_table)
                                except:
                                    st.write("Sorry! Something went wrong with your query, please try again.")
                                else:
                                    # st.dataframe(df)
                                    cols = st.columns(3)
                                    select_exam_meta = f"SELECT firstname || ' ' || lastname AS name,managed_by,is_released,due_date,due_time FROM users, exam WHERE uid = managed_by AND eid={exam_eid} LIMIT 1;"
                                    try:
                                        exam_meta = conn.query_db_all(select_exam_meta).iloc[0]
                                    except:
                                        st.write("Sorry! Something went wrong with your query, please try again.")
                                    else:
                                        with cols[0]:
                                            st.markdown("**Exam Managed By:**")
                                            st.markdown(f"**{exam_meta['name']}**")
                                        with cols[1]:
                                            st.markdown(f"**Due:**")
                                            st.markdown(f"**{exam_meta['due_date']} {exam_meta['due_time']}**")
                                        with cols[2]:
                                            if exam_meta['is_released']:
                                                st.success('Released')
                                            else:
                                                st.warning('Not Released')
                                        st.markdown("---")
                                        for idx in range(len(df)):
                                            create_question_card(df,idx)
                        except Exception as e:
                            st.write(
                                "Sorry! Something went wrong with your query, please try again."+str(e)
                            )

def create_question_card(df,idx):
    # print(row)
    row = df.iloc[idx]
    container = st.container()
    container.markdown(f"#### Q{idx+1}) {row['description']}")
    col,_ = container.columns(2)
    with col:
        container.write(f"A) {row['opt_a']}")
        container.write(f"B) {row['opt_b']}")
        container.write(f"C) {row['opt_c']}")
        container.write(f"D) {row['opt_d']}")
        container.write("")
        correct_ans = row[f'opt_{row["opt_answer"].lower()}']
        container.markdown(f"**Answer: ({row['opt_answer']})** {correct_ans}")
        container.write("")
    st.markdown("---")