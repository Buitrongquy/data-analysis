import myconnutils 
import pandas as pd
from datetime import datetime

connection = myconnutils.getConnection() 
# print ("Connect successful!") 

def query_time(user_id):
    start_timestamps = []
    finished_timestamps = []

    try:
        with connection.cursor() as cursor:
            query = """
            Select acp.start_timestamp, acp.end_timestamp
            From lesson l
            Join analytics_user_lesson aul
            On aul.lesson_id = l.id
            Join user u
            On u.id = aul.user_id
            Join analytics_course_progress acp
            On l.course_id = acp.course_id
            where u.id = %s 
            """
            cursor.execute(query, (user_id))
            data_course = cursor.fetchall()
            
            # Tạo DataFrame từ kết quả truy vấn
            df_course = pd.DataFrame(data_course, columns=['start_timestamp', 'end_timestamp'])
            
            # Chuyển đổi timestamp thành chuỗi định dạng hoặc để None nếu không có giá trị
            df_course['start_timestamp'] = df_course['start_timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if x else None)
            df_course['end_timestamp'] = df_course['end_timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if x else None)
    
        # print (df_course)

    except Exception as e:
        print(f"Lỗi khi thực hiện truy vấn: {e}")

        
    return df_course['start_timestamp'], df_course['end_timestamp']

#query_time('8e8f1ac2-44ee-4413-88d1-23072e0144fc')


