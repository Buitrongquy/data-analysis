import analyze_lesson_time
import pandas as pd
import plotly.graph_objects as go

def time_week(user_id):
    # Lấy dữ liệu
    week_day_hour = analyze_lesson_time.sum_hour_week(user_id)

    # Nhóm thành các tuần
    weekly_df = week_day_hour.groupby('Week Start').agg({
        'Week Total Hours': 'first',
        'Date': 'max'  
    }).reset_index()

    # Làm tròn Week Total Hours  
    weekly_df['Week Total Hours'] = weekly_df['Week Total Hours'].round(1)
    # print(weekly_df)

    # Đổi tên cột 
    weekly_df.columns = ['Week Start', 'Week Total Hours', 'Week End']

    # Tạo chuỗi ngày để hiển thị trên trục x
    weekly_df['Date Range'] = weekly_df.apply(lambda row: f"{row['Week Start']} to {row['Week End']}", axis=1)

    # Tạo danh sách màu
    colors = ['#fbba72'] * len(weekly_df)
    colors[-1] = '#ff7b00'

    # Tạo biểu đồ
    fig = go.Figure(data=[
        go.Bar(
            x=weekly_df['Date Range'],
            y=weekly_df['Week Total Hours'],
            text=weekly_df['Week Total Hours'],
            marker_color=colors,
            name="Số giờ học"
        )
    ])

    # Cập nhật layout
    fig.update_layout(
        title={
            'text': "Tổng số giờ học theo tuần",
            'y':0.9,  
            'x':0.5,  
            'xanchor': 'center', 
            'yanchor': 'top'  
        },
        xaxis_title="Tuần",
        yaxis_title="Tổng số giờ"
    )

    # # Hiển thị biểu đồ
    # fig.show()

    # Trả về JSON
    fig_json = fig.to_json()
    return fig_json

# time_week('8e8f1ac2-44ee-4413-88d1-23072e0144fc')