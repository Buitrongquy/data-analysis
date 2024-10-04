import myconnutils 
import pandas as pd
from datetime import datetime

connection = myconnutils.getConnection() 
# print ("Connect successful!") 

def query_lesson_datetime(user_id):
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT l.duration, als.start_timestamp, als.finished_timestamp
            FROM user u
            JOIN analytics_lesson_session als ON als.user_id = u.id
            JOIN lesson l ON als.lesson_id = l.id
            WHERE u.id = %s 
            """
            cursor.execute(query, (user_id))
            data_lesson = cursor.fetchall()
            data_lesson_df = pd.DataFrame(data_lesson, columns=['duration', 'open_timestamp', 'close_timestamp'])

        # Chuyển đổi cột timestamp thành datetime
        data_lesson_df['open_timestamp'] = pd.to_datetime(data_lesson_df['open_timestamp'])
        data_lesson_df['close_timestamp'] = pd.to_datetime(data_lesson_df['close_timestamp'])

        # Tách ngày và giờ
        data_lesson_df['open_date'] = data_lesson_df['open_timestamp'].dt.date
        data_lesson_df['close_date'] = data_lesson_df['close_timestamp'].dt.date

        # Xóa cột open_timestamp và close_timestamp gốc 
        data_lesson_df = data_lesson_df.drop(columns=['open_timestamp', 'close_timestamp'])

        #duration = 0
        duration = data_lesson_df['duration'].tolist()
        open_time = data_lesson_df['open_date'].tolist()
        finish_time = data_lesson_df['close_date'].tolist()

        # # In ra kết quả
        # print("Duration tuple:", duration)
        # print("Open time tuple:", open_time)
        # print("Finish time tuple:", finish_time)

        
    except Exception as e:
        print(f"Lỗi khi thực hiện truy vấn: {e}")

    return duration, open_time, finish_time

#query_lesson_datetime("dc139449-56ea-4fd6-89b2-a7db8a0dd46f")
