import analyze_lesson_time
import plotly.graph_objects as go

def average_time_day(user_id):
    # Lấy dữ liệu
    hour, minutes = analyze_lesson_time.average_time_today(user_id)

    # Tạo biểu đồ chỉ số
    fig = go.Figure(go.Indicator(
        mode="number",
        value=hour,
        number={
            'suffix': f" giờ {minutes:02d} phút",
            'valueformat': ".0f",
        },
        title={'text': "Thời gian học trung bình hôm nay"},
    ))

    # Cập nhật layout
    fig.update_layout(
        height=300,
        shapes=[
            dict(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="black", width=2),
                fillcolor="#c1d3fe",  
                layer='below' 
            )
        ],
        margin=dict(t=50, b=50, l=50, r=50)
    )


    # # Hiển thị biểu đồ
    # fig.show()

    # Trả về JSON
    fig_json = fig.to_json()
    return fig_json

# average_time_day('8e8f1ac2-44ee-4413-88d1-23072e0144fc')

