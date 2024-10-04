import myconnutils 
import pandas as pd
from datetime import datetime

connection = myconnutils.getConnection() 
# print ("Connect successful!") 

def get_quiz_data(user_id):
    try:
        with connection.cursor() as cursor:
            query = """
            Select q.id, c.title, qa.quiz_score, qa.time_start, qa.time_ended
            From quiz_attempt qa
            Join quiz q
            On qa.quiz_id = q.id
            Join user u
            On qa.user_id = u.id
            Join content c
            On q.content_id = c.id
            Where u.id = %s 
            """
            cursor.execute(query, (user_id))
            data_quiz = cursor.fetchall()
            data_quiz_df = pd.DataFrame(data_quiz, columns=['id', 'title', 'quiz_score', 'time_start', 'time_ended'])

        # Chuyển đổi cột timestamp thành datetime
        data_quiz_df['time_start'] = pd.to_datetime(data_quiz_df['time_start'])
        data_quiz_df['time_ended'] = pd.to_datetime(data_quiz_df['time_ended'])

        # Tách ngày và giờ
        data_quiz_df['open_date'] = data_quiz_df['time_start'].dt.date
        data_quiz_df['close_date'] = data_quiz_df['time_ended'].dt.date

        # Xóa cột time_start và time_ended gốc 
        data_quiz_df = data_quiz_df.drop(columns=['time_start', 'time_ended'])

        quiz_id = data_quiz_df['id'].tolist()
        content_title = data_quiz_df['title'].tolist()
        quiz_score = data_quiz_df['quiz_score'].tolist()
        open_dates = data_quiz_df['open_date'].tolist()
        close_dates = data_quiz_df['close_date'].tolist()

        # # In ra kết quả
        # print("quiz id: ", quiz_id)
        # print("content_title: ", content_title)
        # print("quiz_score: ", quiz_score)
        # print("Open time tuple:", open_dates)
        # print("Finish time tuple:", close_dates)
        # print(data_quiz_df)
        
    except Exception as e:
        print(f"Lỗi khi thực hiện truy vấn: {e}")

    return quiz_id, content_title, quiz_score, open_dates, close_dates

#get_quiz_data("dc139449-56ea-4fd6-89b2-a7db8a0dd46f")
