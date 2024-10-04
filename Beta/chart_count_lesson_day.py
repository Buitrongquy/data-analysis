import analyze_count_lesson
import plotly.graph_objects as go
import pandas as pd

def count_lesson_day(user_id):
    # Lấy dữ liệu
    date_sum_lesson = analyze_count_lesson.sum_lesson_date(user_id)

    # Chuẩn bị dữ liệu cho biểu đồ đường
    sum_lesson_keys = list(date_sum_lesson.keys())
    sum_lesson_values = list(date_sum_lesson.values())

    sum_lesson_columns = {
        'date': sum_lesson_keys,
        'lesson': sum_lesson_values,
    }

    sum_lesson_df = pd.DataFrame(sum_lesson_columns)

    # Tạo biểu đồ
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=sum_lesson_df['date'], y=sum_lesson_df['lesson'], mode='lines+markers', name="Số bài học")
    )

    if not sum_lesson_df['lesson'].empty:
        y_max = max(sum_lesson_df['lesson']) + 1
    else:
        y_max = 1

    # Cập nhật layout
    fig.update_layout(
        title={
            'text': "Số lượng bài học theo ngày",
            'y':0.9, 
            'x':0.5,  
            'xanchor': 'center', 
            'yanchor': 'top'  
        },
        xaxis_title="Ngày",
        yaxis_title="Số bài đã học",
        yaxis=dict(range=[0, y_max], dtick=0.5)
    )

    # # Hiển thị biểu đồ
    # fig.show()

    # Trả về JSON
    fig_json = fig.to_json()
    return fig_json

# count_lesson_day('8e8f1ac2-44ee-4413-88d1-23072e0144fc')