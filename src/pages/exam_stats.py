import streamlit as st
from app import *
from src import connection as conn

def write():
    with st.spinner("Loading ..."):
        st.markdown('## Quiz - Exam Stats',unsafe_allow_html=True)
        st.info('For a given exam fetch the exam stats along with score of each student. If a student has multiple attempts show the latest attempt details.')
        col1, col2, col3 = st.columns(3)
        try:
            with col1:
                term_select = st.selectbox('Select Term',sorted(conn.connect('select distinct term from exam E',None)['term']))
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
                                exam_select = st.selectbox('Select Exam id',sorted(conn.connect('select distinct eid from exam E where term=%s and cid=%s',params_exam)['eid']))
                            if term_select and course_select and exam_select:
                                try:
                                    sql = f'''SELECT firstname || ' ' || lastname as Name,email,eid as ExamID,adate as submission_date,atime as submission_time,points as points
                                                FROM (SELECT R1.suid,R1.eid,split_part(adate_atime,' ',1) adate,split_part(adate_atime,' ',2) atime,A.points
                                                FROM (SELECT suid, eid, MAX(adate || ' ' || atime) adate_atime
                                                FROM appears_for A
                                                WHERE eid={exam_select}
                                                GROUP BY suid,eid) R1, appears_for A
                                                WHERE A.suid=R1.suid
                                                AND A.eid=R1.eid
                                                AND A.adate|| ' ' || A.atime=R1.adate_atime
                                                UNION
                                                SELECT R2.suid,{exam_select},'','',0
                                                FROM (SELECT DISTINCT suid 
                                                FROM enroll_in
                                                WHERE cid='{course_select}'
                                                AND term='{term_select}'
                                                EXCEPT
                                                SELECT DISTINCT suid
                                                FROM appears_for
                                                WHERE eid={exam_select}) R2
                                                ) R4, users
                                                WHERE uid=suid
                                                ORDER BY suid;'''
                                    table_df = conn.connect(sql,None)
                                    table_df["submission_time"] = table_df['submission_time'].astype(str)
                                    points = table_df['points']
                                    fig, ax = plt.subplots()
                                    ax.hist(points)
                                    st.pyplot(fig)
                                    sql_stats = f'''SELECT ROUND(MIN(A.points),2) as min,ROUND(MAX(A.points),2) as max,ROUND(AVG(A.points),2) as avg,
                                                        PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY A.points) as median,
                                                        ROUND(STDDEV(A.points),2) as stddev
                                                        FROM (SELECT suid, eid, MAX(adate || ' ' || atime) adate_atime
                                                        FROM appears_for A
                                                        WHERE eid={exam_select}
                                                        GROUP BY suid,eid) R1, appears_for A
                                                        WHERE A.suid=R1.suid
                                                        AND A.eid=R1.eid
                                                        AND A.adate|| ' ' || A.atime=R1.adate_atime; '''
                                    stats_df = conn.connect(sql_stats,None)
                                    col1, col2, col3,col4,col5 = st.columns(5)
                                    col1.metric("Min." ,value=round(float(stats_df['min'][0]),2))
                                    col2.metric("Max.",value=round(float(stats_df['max'][0]),2))
                                    col3.metric("Median",value=round(float(stats_df['median'][0]),2))
                                    col4.metric("Mean", value=round(float(stats_df['avg'][0]),2))
                                    col5.metric("Stddev", value=round(float(stats_df['stddev'][0]),2))
                                    st.dataframe(table_df)
                                except:
                                    st.write("Not able to fetch your results.")
                        except:
                            st.write("Not able to fetch your results.")
                        

    
    

  
