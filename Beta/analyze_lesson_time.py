import query_lesson_time
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
#     duration, open_time, finish_time= query_lesson_time.query_lesson_datetime(first_name, last_name)
#     return duration, open_time, finish_time

# Tạo list chứa các ngày cho đến ngày hiện tại
def date_list (number_of_first_day, number_of_last_day):
    date_ago = list((current_date - timedelta(days=i)) 
                    for i in range(number_of_first_day, number_of_last_day, -1))
    return date_ago

# Tính thời gian học của 1 ngày
def day_hour (date_hour_study, datetime_list, open_time, finish_time, duration):
    for day in datetime_list:
        current_list = []
        for open_day in open_time:
            ind = open_time.index(open_day)
            if day >= open_day and day <= finish_time[ind]:
                current_list.append(duration[ind] / 60)
                hour_sum = sum(current_list)
                date_hour_study[day] = hour_sum
                

        if len(current_list) == 0:
            date_hour_study[day] = 0

    return date_hour_study

# Tìm thời gian học trong 7 ngày gần nhất 
def date_study_hour (user_id):
    duration, open_time, finish_time= query_lesson_time.query_lesson_datetime(user_id)
    # duration, open_time, finish_time = split_name(full_name)
    date_hour_study = {}
    datetime_list = date_list(6,-1)
    date_hour_study = day_hour (date_hour_study, datetime_list, open_time, finish_time, duration)

    # print("Result Dictionary:")
    # for key, value in date_hour_study.items():
    #     print(f"{key}: {value}")

    return date_hour_study 


# Thời gian học trung bình 1 ngày
def average_time_today (user_id):
    # duration, open_time, finish_time = split_name(full_name)
    duration, open_time, finish_time= query_lesson_time.query_lesson_datetime(user_id)
    today_minutes = []
    number_lesson_today = 0
    
    for open_day in open_time:
        ind = open_time.index(open_day)
        if current_date >= open_day and current_date <= finish_time[ind]:
            number_lesson_today += 1
            today_minutes.append(duration[ind])
    
    # Tổng số phút học trong ngày
    total_minutes_today = sum(today_minutes)
    
    # Tính trung bình
    if number_lesson_today == 0:
        average_minutes_today = 0
    else:
        average_minutes_today = total_minutes_today / number_lesson_today

    # Chuyển đổi từ phút sang giờ và phút
    hour = int(average_minutes_today // 60)
    minutes = int(average_minutes_today % 60)

    # print("Số giờ học trung bình là:", hour, "giờ", minutes, "phút")
    return hour, minutes

# Tìm danh sách các ngày của 4 tuần trước hiện tại
def create_date_list(start_date, end_date):

    date_list = []
    
    # Lặp qua từng ngày và thêm vào danh sách
    while start_date <= end_date:
        date_list.append(start_date)
        start_date += timedelta(days=1)

    return date_list

# Tính thời gian học theo từng ngày của 4 tuần trước
def four_week_hour (user_id):
    duration, open_time, finish_time= query_lesson_time.query_lesson_datetime(user_id)
    # duration, open_time, finish_time = split_name(full_name)

    # Tính ngày bắt đầu của tuần hiện tại (thứ 2)
    current_week_start = current_date - timedelta(days=current_date.weekday())
    
    # Tính ngày bắt đầu của 4 tuần trước
    four_weeks_ago_start = current_week_start - timedelta(weeks=4)

    date_list = create_date_list(four_weeks_ago_start, current_date)
    day_hour_study = {}

    day_hour_study = day_hour (day_hour_study, date_list, open_time, finish_time, duration)

    # print("Result Dictionary:")
    # for key, value in day_hour_study.items():
    #     print(f"{key}: {value}")

    return day_hour_study

# Nhóm các ngày thành tuần
def group_days_by_week(day_hour_study):
    weeks = defaultdict(lambda: {"days": {}, "total_hours": 0})
    
    for date_str, hours in day_hour_study.items():
        week_start = date_str - timedelta(days=date_str.weekday())
        week_key = week_start.strftime("%Y-%m-%d")
        
        weeks[week_key]["days"][date_str] = hours
        weeks[week_key]["total_hours"] += hours
    
    return dict(weeks)

# Tổng giờ học của mỗi tuần
def sum_hour_week (user_id):
    day_hour_study = four_week_hour(user_id)
    grouped_weeks = group_days_by_week(day_hour_study)

    week_day_hour = []
    for week_start, week_data in grouped_weeks.items():
        for date, hours in week_data['days'].items():
            week_day_hour.append({
                'Week Start': week_start,
                'Date': date,
                'Hours': hours,
                'Week Total Hours': week_data['total_hours']
            })

    week_day_hour = pd.DataFrame(week_day_hour)
    # print(week_day_hour)

    return week_day_hour

# average_time_today ('dc139449-56ea-4fd6-89b2-a7db8a0dd46f')
#sum_hour_week ('dc139449-56ea-4fd6-89b2-a7db8a0dd46f')
