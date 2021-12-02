import streamlit as st
from src import connection as conn

# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading ..."):
        st.markdown(
            """## Quiz - Display All Tables""",unsafe_allow_html=True
            )

        sql_all_table_names = "SELECT relname FROM pg_class WHERE relkind='r' AND relname !~ '^(pg_|sql_)' ORDER BY relname;"
        try:
            all_table_names = conn.query_db_all(sql_all_table_names)["relname"].tolist()
            table_name = st.selectbox("Choose a table", all_table_names)
        except:
            st.write("Sorry! Something went wrong with your query, please try again.")
        else:
            if table_name:
                f"Display the table"

                sql_table = f"SELECT * FROM {table_name};"
                try:
                    df = conn.query_db_all(sql_table)
                    st.dataframe(df)
                except:
                    st.write(
                        "Sorry! Something went wrong with your query, please try again."
                    )
