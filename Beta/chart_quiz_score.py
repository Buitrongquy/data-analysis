import analyze_quiz
import query_quiz
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math

def quiz_score(user_id):
    try:
        # Lấy dữ liệu
        average_student_scores, max_score, min_score, Q1, Q3 = analyze_quiz.analyze_student_score(user_id)
        quiz_id, content_title, quiz_score, open_dates, close_dates = query_quiz.get_quiz_data(user_id)
        
        # Kiểm tra và gán giá trị 0 nếu biến không có dữ liệu
        average_student_scores = average_student_scores if average_student_scores is not None else 0
        max_score = max_score if max_score is not None else 0
        min_score = min_score if min_score is not None else 0
        Q1 = Q1 if Q1 is not None else 0
        Q3 = Q3 if Q3 is not None else 0
        quiz_score = quiz_score if quiz_score else [0]
        
        # Chuyển đổi quiz_score thành pandas Series
        quiz_score_series = pd.Series(quiz_score)
        
        # Tính toán số lượng bài kiểm tra cho mỗi điểm số
        score_counts = quiz_score_series.value_counts().sort_index()
        max_count = math.ceil(score_counts.max()) if not score_counts.empty else 1
        
        # Tạo histogram
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=quiz_score,
            nbinsx=101,
            name='Số lượng bài kiểm tra',
            texttemplate='%{y}',
            textposition='auto',
            marker_color='#4c956c',
        ))
        
        # Thêm đường thẳng biểu thị điểm trung bình
        fig.add_trace(go.Scatter(
            x=[average_student_scores, average_student_scores],
            y=[0, quiz_score_series.value_counts().max() + 0.5 if not quiz_score_series.empty else 1],
            mode='lines',
            name=f'Điểm trung bình ({average_student_scores:.2f})',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        # Thêm đường Q1
        fig.add_trace(go.Scatter(
            x=[Q1, Q1],
            y=[0, max(quiz_score_series.value_counts()) + 0.5 if not quiz_score_series.empty else 1],
            mode='lines',
            name=f'Q1 ({Q1:.2f})',
            line=dict(color='black', width=2, dash='dot')
        ))
        
        # Thêm đường Q3
        fig.add_trace(go.Scatter(
            x=[Q3, Q3],
            y=[0, max(quiz_score_series.value_counts()) + 0.5 if not quiz_score_series.empty else 1],
            mode='lines',
            name=f'Q3 ({Q3:.2f})',
            line=dict(color='black', width=2, dash='dot')
        ))
        
        # Thêm đường nối giữa Q1 và Q3
        y_position = max(quiz_score_series.value_counts()) * 1.1 if not quiz_score_series.empty else 1
        fig.add_trace(go.Scatter(
            x=[Q1, Q3],
            y=[y_position, y_position],
            mode='lines',
            name='Khoảng điểm phổ biến',
            line=dict(color='#3a86ff', width=2, dash='dot'),
        ))
        
        # Cập nhật layout
        fig.update_layout(
            title={
                'text': "Phân bố điểm bài kiểm tra",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='Điểm',
            yaxis_title='Số lượng bài kiểm tra',
            bargap=0.1,
            showlegend=True
        )
        
        # Cập nhật trục x để hiển thị tất cả các giá trị từ 0 đến 100
        fig.update_xaxes(
            tickmode='linear',
            tick0=0,
            dtick=5,
            range=[-1, 101],
            tickangle=0
        )

        # Hiển thị biểu đồ
        # fig.show()

        # Trả về JSON
        fig_json = fig.to_json()
        return fig_json
    except Exception as e:
        print(f"An error occurred: {e}")
        # Trả về một JSON rỗng hoặc một giá trị mặc định nếu có lỗi
        return "{}"

# quiz_score('8e8f1ac2-44ee-4413-88d1-23072e0144fc')