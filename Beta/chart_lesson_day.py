import analyze_lesson_time
import pandas as pd
import plotly.express as px

def lesson_day(user_id):
    # Lấy dữ liệu
    result_course = analyze_lesson_time.date_study_hour(user_id)

    # Chuẩn bị dữ liệu cho biểu đồ đường
    keys = list(result_course.keys())
    values = list(result_course.values())

    dict_columns = {
        'date': keys,
        'hours': values,
    }

    df = pd.DataFrame(dict_columns)

    # Tạo biểu đồ đường
    fig = px.line(df, x='date', y='hours', markers=True)

    # Cập nhật layout
    fig.update_layout(
        title={
            'text': "Thời gian học theo từng ngày",
            'y':0.95,  
            'x':0.5,  
            'xanchor': 'center', 
            'yanchor': 'top'  
        },
        xaxis_title="Ngày",
        yaxis_title="Thời gian học (Giờ)",
        yaxis=dict(range=[0, max(df['hours']) + 1])
    )

    # Hiển thị biểu đồ
    # fig.show()

    # Trả về JSON
    fig_json = fig.to_json()
    return fig_json

# lesson_day('8e8f1ac2-44ee-4413-88d1-23072e0144fc')