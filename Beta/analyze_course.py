import query_course
from datetime import datetime


def statistics_course(user_id):

    start_timestamp, finished_timestamp = query_course.query_time(user_id)
    tong_da_hoc = 0
    tong_chua_hoc = 0
    tong_dang_hoc = 0
    current_time = datetime.now()


    for i in range(len(start_timestamp)):

        if start_timestamp[i] == "None" or finished_timestamp[i] == "None":
            continue
        
        else:
            start_time = datetime.strptime(start_timestamp[i], "%Y-%m-%d %H:%M:%S")
            finish_time = datetime.strptime(finished_timestamp[i], "%Y-%m-%d %H:%M:%S")
        
        if current_time < start_time:
            tong_chua_hoc = tong_chua_hoc + 1
        elif current_time > finish_time:
            tong_da_hoc = tong_da_hoc + 1
        else:
            tong_dang_hoc = tong_dang_hoc + 1

    # print("chua", tong_chua_hoc)
    # print("da", tong_da_hoc)
    # print("dang", tong_dang_hoc)

    return tong_chua_hoc, tong_dang_hoc, tong_da_hoc

# statistics_course("8e8f1ac2-44ee-4413-88d1-23072e0144fc")

