import query_quiz
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

# Lấy ngày hiện tại
current_date = datetime.now().date()

# #Tách tên đầy đủ thành first_name và last_name
# def split_name(full_name):
#     names = full_name.split()   
#     first_name = names[0]
#     last_name = names[-1]
#     quiz_id, content_title, quiz_score, open_dates, close_dates = query_quiz.get_quiz_data(first_name, last_name)
#     return quiz_id, content_title, quiz_score, open_dates, close_dates

# Tạo list chứa các ngày cho đến ngày hiện tại
def date_list (number_of_first_day, number_of_last_day):
    date_ago = list((current_date - timedelta(days=i)) 
                    for i in range(number_of_first_day, number_of_last_day, -1))
    return date_ago

# Tìm danh sách các ngày của 4 tuần trước hiện tại
def create_date_list(start_date, end_date):

    date_list = []
    
    # Lặp qua từng ngày và thêm vào danh sách
    while start_date <= end_date:
        date_list.append(start_date)
        start_date += timedelta(days=1)

    return date_list

# Tính số bài kiểm tra đã làm của 1 ngày
def count_quiz_by_day(date_range, open_dates, close_dates):
    quiz_counts = defaultdict(int) 
    counted_quizzes = set()  # Lưu các bài kiểm tra đã được đếm

    for day in date_range:
        for i, (open_date, close_date) in enumerate(zip(open_dates, close_dates)):
            if pd.isna(open_date) or pd.isna(close_date):
                continue
            if i not in counted_quizzes and open_date <= day <= close_date:
                    quiz_counts[day] += 1
                    counted_quizzes.add(i)  # Đánh dấu bài kiểm tra đã được đếm

    return quiz_counts

# Nhóm các ngày thành tuần
def group_by_week(daily_counts, start_date, end_date):
    weekly_counts = defaultdict(lambda: {"days": {}, "total_quizzes": 0})
    
    current_date = start_date
    while current_date <= end_date:
        week_start = current_date - timedelta(days=current_date.weekday())
        week_key = week_start.strftime("%Y-%m-%d")
        
        if week_key not in weekly_counts:
            weekly_counts[week_key] = {"days": {}, "total_quizzes": 0}
        
        count = daily_counts.get(current_date, 0)  # Thêm 0 nếu ngày không có bài kiểm tra

        weekly_counts[week_key]["days"][current_date] = count
        weekly_counts[week_key]["total_quizzes"] += count
        
        current_date += timedelta(days=1)
    
    return dict(weekly_counts)

# Tính tổng số bài kiểm tra đã làm của 4 tuần trước
def quiz_four_weeks(user_id):
    # quiz_id, content_title, quiz_score, open_dates, close_dates = split_name(full_name)
    quiz_id, content_title, quiz_score, open_dates, close_dates = query_quiz.get_quiz_data(user_id)
    
    current_date = datetime.now().date()
    current_week_start = current_date - timedelta(days=current_date.weekday())
    four_weeks_ago_start = current_week_start - timedelta(weeks=4)

    date_range = create_date_list(four_weeks_ago_start, current_date)
    
    daily_counts = count_quiz_by_day(date_range, open_dates, close_dates)
    weekly_counts = group_by_week(daily_counts, four_weeks_ago_start, current_date)
    
    # print("Tổng bài kiểm tra theo tuần:")
    # for week_start, week_data in weekly_counts.items():
    #     print(f"Ngày bắt đầu {week_start}:")
    #     for date, count in week_data["days"].items():
    #         print(f" {date}: {count} quizzes")
    #     print(f"Tổng bài kiểm tra : {week_data['total_quizzes']} quizzes")
    #     print()
    
    return weekly_counts

# Phân phối điểm số
def analyze_student_score(user_id):
    # quiz_id, content_title, quiz_score, open_dates, close_dates = split_name(full_name)
    quiz_id, content_title, quiz_score, open_dates, close_dates = query_quiz.get_quiz_data(user_id)
    
    if quiz_score:
        average_student_scores = sum(quiz_score) / len(quiz_score)
        max_score = max(quiz_score)
        min_score = min(quiz_score)
        Q1 = np.percentile(quiz_score, 25)
        Q3 = np.percentile(quiz_score, 75)
        
        # print(f"Điểm trung bình: {average_score:.2f}")
        # print(f"Điểm cao nhất: {max_score}")
        # print(f"Điểm thấp nhất: {min_score}")
    
    return average_student_scores, max_score, min_score, Q1, Q3

# Tìm nhóm điểm dưới 5 và trên 5
def group_scores(user_id):
    # quiz_id, content_title, quiz_score, open_dates, close_dates = split_name(full_name)
    quiz_id, content_title, quiz_score, open_dates, close_dates = query_quiz.get_quiz_data(user_id)
    
    scores_above_half = [score for score in quiz_score if score >= 70]
    scores_below_half = [score for score in quiz_score if score < 70]
    
    # print(scores_above_half)
    # print(scores_below_half)
    return scores_above_half, scores_below_half

# Tính điểm trung bình
def calculate_average_scores(user_id):
    # quiz_id, content_title, quiz_score, open_dates, close_dates = split_name(full_name)
    quiz_id, content_title, quiz_score, open_dates, close_dates = query_quiz.get_quiz_data(user_id)
    
    current_date = datetime.now().date()
    current_week_start = current_date - timedelta(days=current_date.weekday())
    four_weeks_ago_start = current_week_start - timedelta(weeks=4)

    weekly_averages = defaultdict(list)
    
    for score, open_date, close_date in zip(quiz_score, open_dates, close_dates):
        if pd.isna(close_date):
            continue
        if four_weeks_ago_start <= close_date <= current_date:
            week_start = close_date - timedelta(days=close_date.weekday())
            week_key = week_start.strftime("%Y-%m-%d")
            weekly_averages[week_key].append(score)
    
    average_scores = {}
    for week, scores in weekly_averages.items():
        if scores:
            average_scores[week] = statistics.mean(scores)
        else:
            average_scores[week] = None

    return average_scores

# Tính điểm trung bình theo tuần
def get_quiz_average_score_week(user_id):
    weekly_counts = quiz_four_weeks(user_id)
    average_scores = calculate_average_scores(user_id)
    
    quiz_average_score_week = {}

    for week_start, week_data in weekly_counts.items():
        quiz_average_score_week[week_start] = {
            "quiz_count": week_data['total_quizzes'],
            "average_score": average_scores.get(week_start, None)
        }

    # print(quiz_average_score_week)

    return quiz_average_score_week

# quiz_four_weeks("dc139449-56ea-4fd6-89b2-a7db8a0dd46f")
# get_quiz_average_score_week("dc139449-56ea-4fd6-89b2-a7db8a0dd46f")
