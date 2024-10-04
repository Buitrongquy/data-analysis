import plotly.graph_objects as go
import numpy as np
import query
from collections import Counter

# Thời gian làm bài của quiz
def get_time_quiz(quiz_title):
    get_time_quiz = query.get_time_quiz(quiz_title)
    hours = int(get_time_quiz//60)
    minutes = int(get_time_quiz%60)
    if hours != 0:
        fig = go.Figure(go.Indicator(
        mode="number",
        value=hours,
        number={
            'suffix': f" giờ {minutes} phút",
            'valueformat': ".0f",
        },
        title={'text': "THỜI GIAN LÀM BÀI KIỂM TRA"},
    ))
    else:
        
        fig = go.Figure(go.Indicator(
            mode="number",
            value=minutes,
            number={
            'suffix': f"phút",
            'valueformat': ".0f",
        },
            title={'text': "THỜI GIAN LÀM BÀI KIỂM TRA"},
        ))

    # Cập nhật layout
    fig.update_layout(
        height=300,
        width = 500,
        shapes=[
            dict(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="black", width=0.5),
                fillcolor="#F5F5F5",  
                layer='below' 
            )
        ],
        margin=dict(t=50, b=50, l=50, r=50)
    )


    # # Hiển thị biểu đồ
    #fig.show()
    fig_json = fig.to_json()
    return fig_json

# chart mức độ hoàn thành trung bình của quiz
# def calculate_completion_rate(quiz_title):
#     calculate_completion_rate = query.calculate_completion_rate(quiz_title)
#     labels = ['Tỷ lệ hoàn thành trung bình',' ']
#     color = ['rgb(220,20,60)',"#DCDCDC"]
#     values = [calculate_completion_rate, 100-calculate_completion_rate]

#     # Use `hole` to create a donut-like pie chart
#     fig = go.Figure(data=[go.Pie( labels=labels, values=values, hole=.5,marker_colors=color,name=" ")])
#     fig.update_traces(hoverinfo='label+percent+name', textinfo='none')
#     fig.update_layout(title={  'text': "MỨC ĐỘ HOÀN THÀNH TRUNG BÌNH",
#                                 'x':0.5,
#                                 'xanchor': 'center',
#                                 'yanchor': 'top'
#                             },
#                                 annotations=[dict(text=f"{calculate_completion_rate}%", x=0.5, y=0.5, font_size=50, showarrow=False)],
#                                 width=800,
#                                 height=800,
#                                 showlegend=False
#                     )
#     #fig.show()
#     fig_json = fig.to_json()
#     return fig_json
    #print(calculate_completion_rate)

#số lượng học viên tham gia
def number_user_join(quiz_title):
    number_user_join = query.number_user_join(quiz_title)
    fig = go.Figure(go.Indicator(
        mode="number",
        value=number_user_join,
        number={
            'suffix': f" ",
            'valueformat': ".0f",
        },
        title={'text': "SỐ LƯỢNG HỌC VIÊN THAM GIA BÀI KIỂM TRA"},
    ))

    # Cập nhật layout
    fig.update_layout(
        height=300,
        width = 600,
        shapes=[
            dict(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="black", width=0.5),
                fillcolor="#F5F5F5",  
                layer='below' 
            )
        ],
        margin=dict(t=50, b=50, l=50, r=50)
    )


    # # Hiển thị biểu đồ
    #fig.show()
    fig_json = fig.to_json()
    return fig_json

# thời gian làm bài trung bình
def get_avg_duration_per_quiz(quiz_title):
    get_avg_duration_per_quiz = float(query.get_avg_duration_per_quiz(quiz_title))
    #print(get_avg_duration_per_quiz)
    hours = int(get_avg_duration_per_quiz//60)
    minutes = int(get_avg_duration_per_quiz%60)
    if hours != 0:
        fig = go.Figure(go.Indicator(
        mode="number",
        value=hours,
        number={
            'suffix': f" giờ {minutes} phút",
            'valueformat': ".0f",
        },
        title={'text': "THỜI GIAN TRUNG BÌNH HOÀN THÀNH BÀI KIỂM TRA"},
    ))
    else:
        
        fig = go.Figure(go.Indicator(
            mode="number",
            value=minutes,
            number={
            'suffix': f"phút",
            'valueformat': ".0f",
        },
            title={'text': "THỜI GIAN TRUNG BÌNH HOÀN THÀNH BÀI KIỂM TRA"},
        ))

    # Cập nhật layout
    fig.update_layout(
        height=300,
        width = 700,
        shapes=[
            dict(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="black", width=0.5),
                fillcolor="#F5F5F5",  
                layer='below' 
            )
        ],
        margin=dict(t=50, b=50, l=50, r=50)
    )


    # # Hiển thị biểu đồ
    #fig.show()
    fig_json = fig.to_json()
    return fig_json

# chart phân bố điểm theo nhóm
def score_group(quiz_title):
    # Ví dụ dữ liệu
    score_distribution_data = query.score_group(quiz_title)
    #print(score_group)
    score_groups = [row['score_group'] for row in score_distribution_data]
    counts = [row['count'] for row in score_distribution_data]
    score_groups = score_groups
    counts = counts

    # Tạo biểu đồ thanh với Plotly
    fig = go.Figure(data=[
        go.Bar(x=score_groups, y=counts, marker_color=['rgb(46,139,87)', 'rgb(255,140,0)', 'rgb(255,215,0)', 'rgb(255,69,0)'])
    ])

    # Thêm tiêu đề và nhãn
    fig.update_layout(
        title={ 'text': "PHÂN BỐ ĐIỂM THEO NHÓM",
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
        xaxis_title='Nhóm điểm số',
        yaxis_title='Số lượng học viên',
        xaxis=dict(tickmode='linear'),
        yaxis=dict(tickmode='linear'),
        width=800,
        height=800
    )
    fig.update_yaxes(type="log") 

    # Hiển thị biểu đồ
    #fig.show()
    fig_json = fig.to_json()
    return fig_json

# Chart thống kê phân phối điểm
def distribution_score(quiz_title):
    distribution_score = query.distribution_scores(quiz_title)
    distribution_score = distribution_score if distribution_score is not None else [0]

    counter = Counter(distribution_score)
    # Lấy giá trị xuất hiện nhiều nhất
    most_common = counter.most_common(1)[0][1] + 0.5

    average_scores = sum(distribution_score) / len(distribution_score) if distribution_score is not None else 0
    Q1 = np.percentile(distribution_score, 25) if distribution_score is not None else 0
    Q3 = np.percentile(distribution_score, 75) if distribution_score is not None else 0
    #print(average_scores,Q1,Q3)
    fig = go.Figure()
        
    fig.add_trace(go.Histogram(
        x=distribution_score,
        nbinsx=50,
        name='Số lượng bài kiểm tra',
        texttemplate='%{y}',
        textposition='auto',
        marker_color='#8B008B',
    ))
    # Thêm đường thẳng biểu thị điểm trung bình
    fig.add_trace(go.Scatter(
        x=[average_scores, average_scores],
        y=[0, most_common],
        mode='lines',
        name=f'Điểm trung bình ({average_scores:.2f})',
        line=dict(color='#DC143C', width=2, dash='dot')
    ))
    
    # Thêm đường Q1
    fig.add_trace(go.Scatter(
        x=[Q1, Q1],
        y=[0, most_common],
        mode='lines',
        name=f'Q1 ({Q1:.2f})',
        line=dict(color='#696969', width=2, dash='longdash')
    ))
    
    # Thêm đường Q3
    fig.add_trace(go.Scatter(
        x=[Q3, Q3],
        y=[0, most_common],
        mode='lines',
        name=f'Q3 ({Q3:.2f})',
        line=dict(color='#696969', width=2, dash='longdash')
    ))
    
    # Thêm đường nối giữa Q1 và Q3
    y_position = most_common
    fig.add_trace(go.Scatter(
        x=[Q1, Q3],
        y=[y_position, y_position],
        mode='lines',
        name='Khoảng điểm phổ biến',
        line=dict(color='#C71585', width=2, dash='solid'),
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
    fig.update_layout(width=800,
                      height=800
                    )
    #fig.show()
    fig_json = fig.to_json()
    return fig_json

#chart so sánh
def compare_scores(user_id):
    compare_scores = query.compare_scores(user_id)
    #print(compare_scores)
    label= compare_scores["quiz_title"].to_list()
    #print(label)
    fig = go.Figure(data=[
        go.Bar(name='Điểm của bạn', x=label, y=compare_scores['user_score'].to_list(),marker_color = "lightsalmon",width=0.42),
        go.Bar(name='Điểm của người cao nhất', x=label, y=compare_scores['highest_score'].to_list(),marker_color = "indianred",width=0.42)
    ])  
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.update_layout(
        title={
            'text': "SO SÁNH CÁC BÀI KIỂM TRA",
            'x':0.4,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        height=800,
        bargap=0.1,
        showlegend=True
    )
    #fig.show()
    fig_json = fig.to_json()
    return fig_json

#chart điểm học viên
def get_user_score(user_id, quiz_title):
    get_user_score = query.get_user_score(user_id, quiz_title)
    print(get_user_score)

    labels = ['Điểm của bạn',' ']
    color = ['rgb(220,20,60)',"#DCDCDC"]
    values = [get_user_score, 100-get_user_score]

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie( labels=labels, values=values, hole=.5,marker_colors=color,name=" ")])
    fig.update_traces(hoverinfo='label+name', textinfo='none')
    fig.update_layout(title={  'text': "ĐIỂM CỦA BẠN",
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'
                            },
                                annotations=[dict(text=f"{get_user_score}", x=0.5, y=0.5, font_size=50, showarrow=False)],
                                width=800,
                                height=800,
                                showlegend=False
                    )
    #fig.show()
    fig_json = fig.to_json()
    return fig_json

#vị trí xếp hạng
def get_rank(user_id, quiz_title):
    get_rank = query.get_rank(user_id, quiz_title)
    fig = go.Figure(go.Indicator(
        mode="number",
        value=get_rank,
        number={
            'suffix': f" ",
            'valueformat': ".0f",
        },
        title={'text': "VỊ TRÍ XẾP HẠNG"},
    ))

    # Cập nhật layout
    fig.update_layout(
        height=300,
        width = 400,
        shapes=[
            dict(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="black", width=0.5),
                fillcolor="#F5F5F5",  
                layer='below' 
            )
        ],
        margin=dict(t=50, b=50, l=50, r=50)
    )


    # # Hiển thị biểu đồ
    #fig.show()
    fig_json = fig.to_json()
    return fig_json

if __name__ == "__main__":
    compare_scores("dc139449-56ea-4fd6-89b2-a7db8a0dd46f")