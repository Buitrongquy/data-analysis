import plotly.graph_objects as go
from plotly.subplots import make_subplots
import analyze_quiz


def score_6(user_id):
    scores_above_half, scores_below_half = analyze_quiz.group_scores(user_id)

    # Tổng số điểm
    total_scores = len(scores_above_half) + len(scores_below_half)

    #Vẽ biểu đồ gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge",
        gauge = {
            'axis': {
                'range': [0, total_scores],  # Tầm giá trị của gauge
                'tickvals': list(range(1, total_scores + 1)),  # Giá trị hiển thị là 1, 2, 3, ...
                'ticktext': [str(i) for i in range(1, total_scores + 1)],  # Chuyển đổi các giá trị thành chuỗi để hiển thị
            },
            'steps': [
                {'range': [0, len(scores_above_half)], 'color': "green"},  
                {'range': [len(scores_above_half), total_scores], 'color': "orange"}  
            ],
            'threshold': {
                'value': len(scores_above_half)
            }
        }
    ))

    # Thêm số bài kiểm tra đã làm vào giữa biểu đồ
    fig.add_trace(go.Indicator(
        mode = "number",
        value = total_scores,
        title = {'text': "Số lượng<br>bài đã làm", 'font': {'size': 38}, 'align': 'center'},  
        domain = {'x': [0, 1], 'y': [0, 0.3]}  
    ))

    # Thêm chú thích bên ngoài biểu đồ
    fig.update_layout(
        title={
            'text': "Thống kê điểm kiểm tra",
            'y':0.95, 
            'x':0.5,  
            'xanchor': 'center', 
            'yanchor': 'auto'  
        },
        shapes=[
            # Ô màu xanh
            {
                'type': 'rect',
                'x0': 0, 'y0': 0.95, 'x1': 0.02, 'y1': 1,
                'xref': 'paper', 'yref': 'paper',
                'fillcolor': 'green',
                'line': {'width': 0}
            },
            # Ô màu cam
            {
                'type': 'rect',
                'x0': 0, 'y0': 0.8, 'x1': 0.02, 'y1': 0.85,
                'xref': 'paper', 'yref': 'paper',
                'fillcolor': 'orange',
                'line': {'width': 0}
            }
        ],
        annotations=[
            # Chú thích cho điểm trên trung bình
            {
                'x': 0.03, 'y': 1,
                'xref': 'paper', 'yref': 'paper',
                'text': f"<b>Điểm từ 70 trở lên ({len(scores_above_half)}) </b>",
                'showarrow': False,
                'font': {'size': 14, 'color': 'black'},
                'align': 'left'
            },
            # Chú thích cho điểm dưới trung bình
            {
                'x': 0.03, 'y': 0.85,
                'xref': 'paper', 'yref': 'paper',
                'text': f"<b>Điểm dưới 70 ({len(scores_below_half)}) </b>",
                'showarrow': False,
                'font': {'size': 14, 'color': 'black'},
                'align': 'left'
            }
        ]
    )

    # fig.show()

    # Trả về JSON
    fig_json = fig.to_json()
    return fig_json

# score_6('8e8f1ac2-44ee-4413-88d1-23072e0144fc')

