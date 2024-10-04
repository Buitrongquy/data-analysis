import myconnutils as myconnutils
import pandas as pd

# thời gian bài test
def get_time_quiz(quiz_title):
    connection = myconnutils.getConnection()
    time_stats_query = """
    SELECT duration 
    FROM quiz 
    WHERE title = %s;
    """
    
    try:
        cursor = connection.cursor()
        cursor.execute(time_stats_query,quiz_title)
        time_stats_data = cursor.fetchall()
        #print(time_stats_data)
        if not time_stats_data:
            time_stats_data = 0
        else:
            time_stats_data = time_stats_data[0][0]
        return time_stats_data
    finally:
        connection.close()

# Mức độ hoàn thành trung bình
# def calculate_completion_rate(quiz_title):
#     connection = myconnutils.getConnection()
#     try:
#         with connection.cursor() as cursor:
#             # đếm số câu hỏi từng quiz
#             query = """
#                 SELECT 
#                     q.title AS quiz_title, 
#                     COUNT(qu.id) AS number_of_questions 
#                 FROM 
#                     quiz q 
#                 JOIN 
#                     quiz_question qu ON q.id = qu.quiz_id
#                 WHERE 
#                     q.title = %s -- Replace with the actual quiz title
#                 GROUP BY 
#                     q.title;
#             """
#             cursor.execute(query, quiz_title)
#             number_question = cursor.fetchone()
#             if not number_question:
#                 number_question = 0
#             else:
#                 number_question = number_question[1]
#             print("ket qua",number_question)

#             # đếm số người tham gia từng quiz
#             query = """
#                 SELECT 
#                 q.title AS quiz_title,
#                 COUNT(DISTINCT qa.user_id) AS number_of_participants
#                 FROM 
#                     quiz q
#                 JOIN 
#                     quiz_attempt qa ON q.id = qa.quiz_id
#                 WHERE 
#                     q.title = %s  -- Thay thế bằng tên bài quiz bạn muốn
#                 GROUP BY 
#                     q.title;
#             """
#             cursor.execute(query, quiz_title)
#             number_user = cursor.fetchone()
            
#             if not number_user:
#                 number_user = 0
#             else:
#                 number_user = number_user[1]
#             print("ket qua user",number_user)
#             # đếm số câu trả lời cho từng quiz
#             query = """
#                 SELECT                         
#                         q.title AS quiz_title,
#                         COUNT(DISTINCT qa.user_id) AS number_of_unique_users
#                     FROM 
#                         quiz q
#                     JOIN 
#                         quiz_question qq ON q.id = qq.quiz_id
#                     JOIN 
#                         quiz_user_choice ua ON qq.id = ua.question_id
#                     JOIN 
#                         quiz_attempt qa ON qa.id = ua.attempt_id -- Liên kết bảng quiz_attempt với bảng quiz_user_choice
#                     WHERE 
#                         q.title = %s -- Thay thế bằng tên bài quiz bạn muốn
#                     GROUP BY 
#                         q.title;


#             """
#             cursor.execute(query, quiz_title)
#             number_answer = cursor.fetchone()
#             if not number_answer:
#                 number_answer = 0
#             else:
#                 number_answer = number_answer[1] 
#             print("ket qua anser",number_answer)

#             average_completion_rate = (number_answer/(number_question*number_user))*100 if (number_user !=0 and number_question !=0) else 0
#             return round(average_completion_rate, 1)
#     finally:
#         connection.close()

#thống kê số lượng học viên tham gia
def number_user_join(quiz_title):    
    # Kết nối tới cơ sở dữ liệu
    connection = myconnutils.getConnection()
    #print("Connect successful!")

    # Truy vấn số lượng học viên tham gia
    student_count_query = """
    SELECT 
    q.title AS quiz_title,
    COUNT(DISTINCT qa.user_id) AS student_count
    FROM 
        quiz_attempt qa
    JOIN 
        quiz q ON qa.quiz_id = q.id
    WHERE 
        q.title = %s -- Dùng biến đầu vào cho tên bài test
    GROUP BY 
    q.title;
    """

    try:
        cursor = connection.cursor()
        
        # Thực thi truy vấn số lượng học viên tham gia
        cursor.execute(student_count_query,quiz_title)
        student_count_data = cursor.fetchall()
        #print(f"Tiêu đề quiz: {student_count_data['quiz_title']}, Số lượng học viên: {student_count_data['student_count']}")
        #print(student_count_data)
        if not student_count_data:
            student_count_data = 0
        else:
            student_count_data = student_count_data[0][1]
        #print(student_count_data)
        return student_count_data
    finally:
        # Đóng kết nối
        connection.close()

#thống kê thời gian làm bài trung bình
def get_avg_duration_per_quiz(quiz_title):
    connection = myconnutils.getConnection()
    with connection.cursor() as cursor:
        # Truy vấn để tính toán thời gian làm bài trung bình cho một bài kiểm tra cụ thể
        query = """
        SELECT AVG(TIMESTAMPDIFF(MINUTE, qa.time_start, qa.time_ended)) AS avg_duration
        FROM quiz_attempt qa
        JOIN quiz q ON qa.quiz_id = q.id
        WHERE q.title = %s; -- Sử dụng tên bài kiểm tra làm đầu vào

        """
        cursor.execute(query, (quiz_title,))
        result = cursor.fetchone()   
        #print("thời gian làm bài",result)
        if not result or not result[0]:
            result = 0
        else:
            result = result[0] 
        #print(result)
        return result

#thống kê điểm theo nhóm
def score_group(quiz_title):
    # Kết nối tới cơ sở dữ liệu
    connection = myconnutils.getConnection()
    #print("Connect successful!")

    # Truy vấn phân phối điểm số theo nhóm
    score_distribution_query = """
    SELECT
        CASE
            WHEN qa.quiz_score >= 85 THEN 'A'
            WHEN qa.quiz_score >= 70 THEN 'B'
            WHEN qa.quiz_score >= 50 THEN 'C'
            ELSE 'D'
        END AS score_group,
        COUNT(*) AS count
    FROM
        quiz_attempt qa
    JOIN 
        quiz q ON qa.quiz_id = q.id
    WHERE 
        q.title = %s -- Sử dụng tên bài kiểm tra làm đầu vào
    GROUP BY
        score_group;

    """

    try:
        cursor = connection.cursor()
        
        # Thực thi truy vấn phân phối điểm số
        cursor.execute(score_distribution_query, quiz_title)
        score_distribution_data = cursor.fetchall()
        #print(score_distribution_data)

        # Tạo danh sách các nhóm điểm mặc định
        full_groups = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        #print("kq",score_distribution_data)
        # Cập nhật các giá trị có trong kết quả của bạn
        for entry in score_distribution_data:
            group = entry[0]
            count = entry[1]
            full_groups[group] = count
        
        # Chuyển đổi từ dict sang list và sắp xếp theo thứ tự nhóm điểm
        sorted_result = [{'score_group': k, 'count': v} for k, v in sorted(full_groups.items())]
        #score_distribution_data = ensure_full_groups(score_distribution_data)
        #print(sorted_result)
        return sorted_result
    finally:
        # Đóng kết nối
        connection.close()

#thống kê phân phối điểm
def distribution_scores(quiz_title):
    connection = myconnutils.getConnection()
    try:
        with connection.cursor() as cursor:
            sql = '''
            SELECT qa.quiz_score 
            FROM quiz_attempt qa
            JOIN quiz q ON qa.quiz_id = q.id
            WHERE q.title = %s;
            '''
            cursor.execute(sql, quiz_title)
            results = cursor.fetchall()
            if not results or not results[0]:
                scores = [0]
            else:
                scores = [score[0] for score in results]
            #print(results)
    finally:
        connection.close()
    return scores

# thống kê so sánh điểm học viên với điểm cao nhất trong tất cả các bài test
def compare_scores(user_id):
    connection = myconnutils.getConnection()
    try:
        query = """
        WITH user_max_scores AS (
    SELECT 
            qa.quiz_id,
            q.title AS quiz_title,
            MAX(qa.quiz_score) AS user_score
        FROM 
            quiz_attempt qa
        JOIN 
            quiz q ON qa.quiz_id = q.id
        JOIN 
            user u ON qa.user_id = u.id
        WHERE 
            u.id = %s -- Thay bằng ID của học viên
        GROUP BY 
            qa.quiz_id, q.title
    ),
    max_scores AS (
        SELECT 
            quiz_id,
            MAX(quiz_score) AS highest_score
        FROM 
            quiz_attempt
        GROUP BY 
            quiz_id
    )
    SELECT 
        ums.quiz_title,
        ums.user_score,
        ms.highest_score
    FROM 
        user_max_scores ums
    JOIN 
        max_scores ms ON ums.quiz_id = ms.quiz_id;
        """
    
        df = pd.read_sql(query, connection, params=(user_id,))        
        #print("df",df)
        # Sắp xếp DataFrame theo 'user_score' giảm dần và sau đó theo 'quiz_title' tăng dần
        df_sorted = df.sort_values(['user_score', 'quiz_title'], ascending=[False, True])

        # Loại bỏ các bản sao trùng lặp của 'quiz_title', giữ lại bản ghi đầu tiên (điểm cao nhất)
        df_unique = df_sorted.drop_duplicates(subset='quiz_title', keep='first')

        #print(df_unique)
        #print("df",df)
        return df_unique
        
    finally:
        connection.close()

# xác định điểm của học viên
def get_user_score(user_id, quiz_title):
    connection = myconnutils.getConnection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT MAX(qa.quiz_score) 
            FROM quiz_attempt qa
            JOIN user u ON qa.user_id = u.id
            JOIN quiz q ON qa.quiz_id = q.id
            WHERE u.id = %s AND q.title = %s
            """
            cursor.execute(query, (user_id, quiz_title))
            result = cursor.fetchone()
            print(result)
            if not result or not result[0]:
                result = 0
            else:
                result = result[0]
            #print(result)
            return result
    finally:
        connection.close()

# thứ hạng của học viên
def get_rank(user_id, quiz_title):
    connection = myconnutils.getConnection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT u.id, MAX(qa.quiz_score),
            FIND_IN_SET(MAX(qa.quiz_score), 
                (SELECT GROUP_CONCAT(quiz_score ORDER BY quiz_score DESC) 
                FROM quiz_attempt WHERE quiz_id = (
                    SELECT id FROM quiz WHERE title = %s)
                )
            ) AS user_rank
            FROM quiz_attempt qa
            JOIN `user` u ON qa.user_id = u.id
            JOIN quiz q ON qa.quiz_id = q.id
            WHERE u.id = %s AND q.title = %s
            """
            cursor.execute(query, (quiz_title, user_id, quiz_title))
            result = cursor.fetchone()
            #print(result)
            if not result or not result[2]:
                result = 0
            else:
                result = result[2]
            
            return result
    finally:
        connection.close()

def recomment_content(user_id,quiz_title):
    connection = myconnutils.getConnection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT 
                c.title AS content_title
            FROM 
                quiz q
            JOIN 
                quiz_question qq ON q.id = qq.quiz_id
            JOIN 
                quiz_option qo ON qq.id = qo.quiz_question_id
            JOIN 
                quiz_user_choice quc ON quc.selected_option_id = qo.id
            JOIN 
                quiz_attempt qa ON qa.id = quc.attempt_id
            JOIN 
                content c ON q.content_id = c.id
            WHERE 
                qa.user_id = %s   -- Input user_id
            AND 
                q.title = %s     -- Input quiz_title
            AND 
                qo.is_correct_answer = 0  -- Only incorrect answers
            AND 
                qa.quiz_id = q.id;

            """
            cursor.execute(query, (user_id, quiz_title))
            result = cursor.fetchone()
            print(result)
            # if not result or not result[2]:
            #     result = 0
            # else:
            #     result = result[2]
            
            # return result
    finally:
        connection.close()

if __name__ == "__main__":
    print(recomment_content("dc139449-56ea-4fd6-89b2-a7db8a0dd46f","C++ Basics" ))
    #('Quiz on Programming')
    #get_rank("user1",'Quiz on Programming' )