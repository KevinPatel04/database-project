import streamlit as st
from app import *
from src import connection as conn

def write():
    with st.spinner("Loading ..."):
        st.markdown('## Quiz - Exam Trends',unsafe_allow_html=True)
        st.info("What does the past exams trends in terms of median scores looks like for a given course?")
        try:
            course_title = conn.connect('select distinct course_title from course',None)['course_title']
            course_id =conn.connect('select distinct cid from course',None)['cid']
            all_courses = course_id+': '+ course_title
            course_select = st.selectbox('Select Course id',all_courses)
            cid = course_select.split(': ')[0]
        except Exception as e:
            st.write(str(e)+'Not able to fetch your results.')    
        else: 
            if course_select:
                    try:
                        sql = f'''SELECT R3.eid, ROUND((R3.avgpoints/(SUM(Q.points)))*100,2) as average FROM questions Q,exam E,  
                                    (SELECT eid ,AVG(points) as avgpoints
                                    FROM (SELECT R1.suid,R1.eid,split_part(adate_atime,' ',1) adate,split_part(adate_atime,' ',2) atime,A.points
                                    FROM (SELECT suid, eid, MAX(adate || ' ' || atime) adate_atime
                                    FROM appears_for A
                                    WHERE eid in (select eid from exam where cid='{cid}')
                                    GROUP BY suid,eid) R1, appears_for A
                                    WHERE A.suid=R1.suid
                                    AND A.eid=R1.eid
                                    AND A.adate|| ' ' || A.atime=R1.adate_atime
                                    ) R2 GROUP BY eid ORDER BY eid) R3 
                                    where R3.eid = Q.eid and R3.eid = E.eid
                                    GROUP BY R3.eid,R3.avgpoints,E.due_date,E.due_time
                                    ORDER BY E.due_date,E.due_time;
                                    '''
                        table_df = conn.connect(sql,None)
                        fig = plt.figure()
                        ax = fig.add_axes([0,0,1,1])
                        examids = table_df['eid'].astype(str)
                        ax.bar(examids,table_df['average'])
                        plt.xlabel('Exam Ids')
                        plt.ylabel('Percentage Mean (%)')
                        plt.title(f'Exam trends for course: {course_select}')
                        st.pyplot(plt)
                        sql_all_total_mean =f"""SELECT ROUND(AVG(R2.normpoints),2) as avgpoints FROM 
                                                            (SELECT A.suid,A.eid,SUM(Q.points) as Total_questions,A.points as Total_score,
                                                            ROUND((A.points::decimal/SUM(Q.points))*100,2) as normpoints
                                                            FROM questions Q,
                                                            (SELECT suid, eid, MAX(adate || ' ' || atime) adate_atime
                                                            FROM appears_for A
                                                            WHERE eid in (select eid from exam where cid='{cid}')
                                                            GROUP BY suid,eid) R1, appears_for A
                                                            WHERE A.suid=R1.suid
                                                            AND A.eid=R1.eid
                                                            AND Q.eid = A.eid
                                                            AND A.adate|| ' ' || A.atime=R1.adate_atime
                                                            GROUP BY A.suid,A.eid,A.points
                                                            ) R2"""
                        all_time_mean = conn.connect(sql_all_total_mean,None)['avgpoints'][0]
                        st.markdown(f"#### **FYI: On an average students score {all_time_mean} in the exams for course {course_select}.**")
                    except:
                        st.write('Not able to fetch your results.')   