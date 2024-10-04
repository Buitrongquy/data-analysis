import myconnutils 
import pandas as pd
from datetime import datetime

connection = myconnutils.getConnection() 
# print ("Connect successful!") 

def query_score_title(user_id):
    try:
        with connection.cursor() as cursor:
            query = """
            Select q.title, qa.quiz_score
            From user u
            Join quiz_attempt qa
            On u.id = qa.user_id
            Join quiz q
            On q.id = qa.quiz_id
            where u.id = %s  and qa.quiz_score < 70
            """
            cursor.execute(query, (user_id))
            data_quiz = cursor.fetchall()
            data_score_title = pd.DataFrame(data_quiz, columns=['title', 'quiz_score'])


        quiz_title = data_score_title['title'].tolist()
        quiz_score_under = data_score_title['quiz_score'].tolist()

        # # In ra kết quả
        # print(data_score_title)
        # print(quiz_title)
        # print(quiz_score_under)
        
    except Exception as e:
        print(f"Lỗi khi thực hiện truy vấn: {e}")

    return quiz_title, quiz_score_under

#query_score_title("dc139449-56ea-4fd6-89b2-a7db8a0dd46f")