import streamlit as st
from src import connection as conn

# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading ..."):
        st.markdown(
            """## Quiz - Course List""",unsafe_allow_html=True
            )

        sql_all_terms = "SELECT DISTINCT term FROM course;"
        try:
            all_terms = conn.query_db_all(sql_all_terms)["term"].tolist()
            term = st.selectbox("Choose a term", all_terms)
        except:
            st.write("Sorry! Something went wrong with your query, please try again.")
        else:
            if term:
                f"Display the Course List"

                sql_table = f"SELECT DISTINCT cid AS course_id,course_title AS title,U.firstname || ' ' || U.lastname AS instructor,U.email AS instructor_email FROM course C,users U WHERE term='{term}' AND U.uid = C.instructor;"
                try:
                    df = conn.query_db_all(sql_table)
                    st.dataframe(df)
                except Exception as e:
                    st.write(
                        "Sorry! Something went wrong with your query, please try again."+str(e)
                    )