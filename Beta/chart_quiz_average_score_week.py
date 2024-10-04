import analyze_quiz
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

def quiz_average_score(user_id):
    # Lấy dữ liệu
    quiz_average_score_week = analyze_quiz.get_quiz_average_score_week(user_id)

    # Tạo danh sách ngày từ ngày đầu tiên đến ngày hiện tại
    current_date = datetime.now().date()
    first_week_date = min([datetime.strptime(date, '%Y-%m-%d').date() for date in quiz_average_score_week.keys()])
    all_dates = [first_week_date + timedelta(weeks=i) for i in range((current_date - first_week_date).days // 7 + 1)]
    all_dates_str = [date.strftime('%Y-%m-%d') for date in all_dates]

    # Chuẩn bị dữ liệu cho biểu đồ
    dates = []
    average_scores = []
    colors = []
    
    for date_str in all_dates_str:
        dates.append(date_str)
        if date_str in quiz_average_score_week:
            average_scores.append(quiz_average_score_week[date_str]['average_score'])
        else:
            average_scores.append(0)  # Không có dữ liệu thì trung bình là 0

        # Đổi màu cho tuần hiện tại
        start_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        end_date = start_date + timedelta(days=6)
        if start_date <= current_date <= end_date:
            colors.append('#0e6ba8')
        else:
            colors.append('#62b6cb')

    # Tìm điểm cao nhất
    processed_scores = []
    for score in average_scores:
        if score is None:
            processed_scores.append(0)
        else:
            processed_scores.append(score)

    if processed_scores:
        max_score = max(processed_scores)
    else:
        max_score = 0

    # Tạo nhãn tuần với ngày bắt đầu và kết thúc
    week_labels = [f"{date} - {(datetime.strptime(date, '%Y-%m-%d') + timedelta(days=6)).strftime('%Y-%m-%d')}" for date in dates]

    # Tạo biểu đồ cột
    fig = go.Figure(data=[
        go.Bar(
            x=week_labels,
            y=average_scores,
            name='Điểm trung bình',
            textposition='auto',
            marker_color=colors
        )
    ])

    # Cập nhật layout
    fig.update_layout(
        title={
            'text': "Điểm trung bình theo tuần",
            'y':0.9, 
            'x':0.5,  
            'xanchor': 'center', 
            'yanchor': 'top'  
        },
    xaxis_title='Tuần',
        yaxis_title='Điểm trung bình',
        yaxis_range=[0, (max_score * 1.1) if max_score != 0 else 10],   
    )

    # # Hiển thị biểu đồ
    # fig.show()

    # Trả về JSON
    fig_json = fig.to_json()
    return fig_json

# quiz_average_score('8e8f1ac2-44ee-4413-88d1-23072e0144fc')