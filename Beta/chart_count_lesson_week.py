import analyze_count_lesson
import plotly.graph_objects as go
import pandas as pd

def count_lesson_week(user_id):
    # Lấy dữ liệu
    week_day_lesson = analyze_count_lesson.average_lesson_week(user_id)

    # Nhóm thành các tuần
    lesson_week_df = week_day_lesson.groupby('Week Start').agg({
        'Week Average': 'first',
        'Week End': 'first'  
    }).reset_index()

    # Đổi tên cột 
    lesson_week_df.columns = ['Week Start', 'Week average lesson', 'Week End']

    # Tạo chuỗi ngày để hiển thị trên trục x
    lesson_week_df['Date Range'] = lesson_week_df.apply(lambda row: f"{row['Week Start']} to {row['Week End']}", axis=1)

    # Tạo danh sách màu
    colors = ['#f2baaf'] * len(lesson_week_df)
    colors[-1] = '#e58087'

    # Tạo biểu đồ
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=lesson_week_df['Date Range'],
            y=lesson_week_df['Week average lesson'],
            text=lesson_week_df['Week average lesson'],
            marker_color=colors, 
            name="Trung bình số lượng bài học"
        )
    )

    # Cập nhật layout
    fig.update_layout(
        title={
            'text': "Số lượng bài học trung bình theo tuần",
            'y':0.9,  
            'x':0.5,  
            'xanchor': 'center', 
            'yanchor': 'top'  
        },
        xaxis_title="Tuần",
        xaxis=dict(tickangle=0),
        yaxis_title="Trung bình số bài đã học"
    )

    # # Hiển thị biểu đồ
    # fig.show()

    # Trả về JSON
    fig_json = fig.to_json()
    return fig_json

# count_lesson_week('8e8f1ac2-44ee-4413-88d1-23072e0144fc')