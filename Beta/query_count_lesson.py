import myconnutils 
import pandas as pd
from datetime import datetime

connection = myconnutils.getConnection() 
# print ("Connect successful!") 

def get_lesson_data(user_id):
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT als.lesson_id, als.start_timestamp, als.finished_timestamp
            FROM analytics_lesson_session als
            JOIN analytics_user_lesson aul ON als.lesson_id = aul.lesson_id
            WHERE aul.user_id IN (
                SELECT u.id
                FROM user u
                WHERE u.id = %s 
            )
            """
            cursor.execute(query, (user_id))
            data_lesson = cursor.fetchall()
            data_lesson_df = pd.DataFrame(data_lesson, columns=['lesson_id', 'open_timestamp', 'close_timestamp'])

        # Chuyển đổi cột timestamp thành datetime
        data_lesson_df['open_timestamp'] = pd.to_datetime(data_lesson_df['open_timestamp'])
        data_lesson_df['close_timestamp'] = pd.to_datetime(data_lesson_df['close_timestamp'])

        # Tách ngày và giờ
        data_lesson_df['open_date'] = data_lesson_df['open_timestamp'].dt.date
        data_lesson_df['close_date'] = data_lesson_df['close_timestamp'].dt.date

        # Xóa cột open_timestamp và close_timestamp gốc 
        data_lesson_df = data_lesson_df.drop(columns=['open_timestamp', 'close_timestamp'])

        lesson_id = data_lesson_df['lesson_id'].tolist()
        open_dates = data_lesson_df['open_date'].tolist()
        close_dates = data_lesson_df['close_date'].tolist()

        # # In ra kết quả
        # print("Open time tuple:", open_dates)
        # print("Finish time tuple:", close_dates)
        # print(data_lesson_df)
        
    except Exception as e:
        print(f"Lỗi khi thực hiện truy vấn: {e}")

    return open_dates, close_dates

#get_lesson_data('dc139449-56ea-4fd6-89b2-a7db8a0dd46f')
