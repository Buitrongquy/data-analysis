import query_count_lesson
from datetime import datetime, timedelta
import pandas as pd
from collections import defaultdict

# Lấy ngày hiện tại
current_date = datetime.now().date()

# #Tách tên đầy đủ thành first_name và last_name
# def split_name(full_name):
#     names = full_name.split()   
#     first_name = names[0]
#     last_name = names[-1]
#     open_dates, close_dates= query_count_lesson.get_lesson_data(first_name, last_name)
#     return open_dates, close_dates

# Tạo list chứa các ngày cho đến ngày hiện tại
def date_list (number_of_first_day, number_of_last_day):
    date_ago = list((current_date - timedelta(days=i)) 
                    for i in range(number_of_first_day, number_of_last_day, -1))
    return date_ago

# Tính số lượng bài học theo ngày
def count_lesson (datetime_list, date_sum_lesson, open_dates, close_dates):
    for day in datetime_list:
        sum_lesson_today = 0
        for open_day in open_dates:
            ind = open_dates.index(open_day)
            if day >= open_day and day <= close_dates[ind]:
                sum_lesson_today = sum_lesson_today + 1
                date_sum_lesson[day] = sum_lesson_today
            else:
                sum_lesson_today = sum_lesson_today + 0
                date_sum_lesson[day] = sum_lesson_today

    # print("Tổng số bài học trong hôm nay", sum_lesson_today)
    return date_sum_lesson

# Tìm tổng số bài học trong 7 ngày gần nhất 
def sum_lesson_date (user_id):
    open_dates, close_dates= query_count_lesson.get_lesson_data(user_id)
    # open_dates, close_dates = split_name(user_id)
    datetime_list = date_list(6,-1)
    date_sum_lesson = {}
    date_sum_lesson = count_lesson(datetime_list, date_sum_lesson, open_dates, close_dates)

    # print("Result Dictionary:")
    # for key, value in date_sum_lesson.items():
    #     print(f"{key}: {value}")

    return date_sum_lesson

# Tìm danh sách các ngày của 4 tuần trước hiện tại
def create_list_date(start_date, end_date):

    date_list = []
    
    # Lặp qua từng ngày và thêm vào danh sách
    while start_date <= end_date:
        date_list.append(start_date)
        start_date += timedelta(days=1)

    return date_list

# Tính tổng số bài học theo từng ngày của 4 tuần trước
def lesson_four_week (user_id):
    # open_dates, close_dates = split_name(full_name)
    open_dates, close_dates= query_count_lesson.get_lesson_data(user_id)

    # Tính ngày bắt đầu của tuần hiện tại (thứ 2)
    current_week_start = current_date - timedelta(days=current_date.weekday())
    
    # Tính ngày bắt đầu của 4 tuần trước
    four_weeks_ago_start = current_week_start - timedelta(weeks=4)

    date_list = create_list_date(four_weeks_ago_start, current_date)
    lesson_day = {}

    lesson_day = count_lesson (date_list, lesson_day, open_dates, close_dates)

    # print("Result Dictionary:")
    # for key, value in lesson_day.items():
    #     print(f"{key}: {value}")

    return lesson_day

# Nhóm các ngày thành tuần
def group_by_week(list_day):
    weeks = defaultdict(lambda: {"days": {}, "sum_lesson": 0})
    
    for date_str, lesson in list_day.items():
        week_start = date_str - timedelta(days=date_str.weekday())
        week_end = week_start + timedelta(days=6)
        week_key = week_start.strftime("%Y-%m-%d")
        
        weeks[week_key]["days"][date_str] = lesson
        weeks[week_key]["sum_lesson"] += lesson
        weeks[week_key]["end_date"] = week_end

    # print(weeks)
    
    return dict(weeks)

# Số lượng bài học trung bình của mỗi tuần
def average_lesson_week (user_id):
    list_day = lesson_four_week(user_id)
    grouped_weeks = group_by_week (list_day)

    current_week_start = current_date - timedelta(days=current_date.weekday())
    four_weeks_ago_start = current_week_start - timedelta(weeks=4)
    
    week_keys = [four_weeks_ago_start + timedelta(weeks=i) for i in range(5)]  # 5 tuần bao gồm tuần hiện tại và 4 tuần trước
    week_keys = [week_key.strftime("%Y-%m-%d") for week_key in week_keys]

    week_day_lesson = []
    for week_start in week_keys:
        if week_start in grouped_weeks:
            week_data = grouped_weeks[week_start]
            week_avg = week_data['sum_lesson'] // 7 if week_data['days'] else 0
            for date, lesson in week_data['days'].items():
                week_day_lesson.append({
                    'Week Start': week_start,
                    'Week End': week_data['end_date'].strftime("%Y-%m-%d"),
                    'Date': date,
                    'Lesson': lesson,
                    'Week Average': week_avg
                })
        else:
            week_end = (four_weeks_ago_start + timedelta(weeks=week_keys.index(week_start) + 1) - timedelta(days=1)).strftime("%Y-%m-%d")
            week_day_lesson.append({
                'Week Start': week_start,
                'Week End': week_end,
                'Date': None,
                'Lesson': 0,
                'Week Average': 0
            })


    week_day_lesson_df = pd.DataFrame(week_day_lesson)
    # print(week_day_lesson_df)

    return week_day_lesson_df

# average_lesson_week ('dc139449-56ea-4fd6-89b2-a7db8a0dd46f')
# lesson_four_week ('dc139449-56ea-4fd6-89b2-a7db8a0dd46f')

