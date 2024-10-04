import analyze_quiz
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def quiz_week(user_id):
    # Lấy dữ liệu
    quiz_four_weeks = analyze_quiz.quiz_four_weeks(user_id)

    # Chuẩn bị dữ liệu cho biểu đồ đường
    keys = list(quiz_four_weeks.keys())

    quizzes = []

    for quiz_day in quiz_four_weeks.values():
        total_quizzes = quiz_day['total_quizzes']  # Lấy giá trị 'total_quizzes'
        quizzes.append(total_quizzes)


    dict_columns = {
        'date':keys,
        'quizzes':quizzes,
    }

    df = pd.DataFrame(dict_columns)

    # Chuyển cột 'date' thành định dạng datetime
    df['date'] = pd.to_datetime(df['date']).dt.date

    # Tính toán ngày bắt đầu và kết thúc của tuần
    df['end_date'] = df['date'] + pd.Timedelta(days=6)
    df['end_date'] = pd.to_datetime(df['end_date']).dt.date

    # Gộp ngày bắt đầu và kết thúc để hiển thị trên biểu đồ
    df['week_range'] = df.apply(lambda row: f"{row['date']} to {row['end_date']}", axis=1)

    # Tạo biểu đồ đường tổng số bài kiểm tra đã làm theo tuần
    fig = px.line(df, x='week_range', y='quizzes', markers=True, title='Tổng số bài kiểm tra đã làm theo tuần')

    # Cập nhật layout cho biểu đồ đường
    fig.update_layout(
        title={
            'text': "Tổng số bài kiểm tra đã làm theo tuần",
            'y': 0.9,  
            'x': 0.5,  
            'xanchor': 'center',  
            'yanchor': 'top'  
        }
    )

    # Cập nhật layout cho biểu đồ đường
    fig.update_yaxes(range=[0, max(df['quizzes']) + 1], dtick=0.5, title_text="Bài kiểm tra")
    fig.update_xaxes(title_text="Tuần", tickangle=30)

    # # Hiển thị biểu đồ
    # fig.show()

    # Trả về JSON
    fig_json = fig.to_json()
    return fig_json

# quiz_week('8e8f1ac2-44ee-4413-88d1-23072e0144fc')

