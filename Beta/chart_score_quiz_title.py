import analyze_score_quiz_title
import plotly.graph_objects as go

def chart_score_title(user_id):
    df_score_title = analyze_score_quiz_title.create_score_table(user_id)

    columns = ['Điểm từ 0 đến 25', 'Điểm từ 26 đến 50', 'Điểm từ 51 đến 69']

    if df_score_title.empty:
        fig = go.Figure(data=[go.Table(
            header= dict(values=columns, fill_color='#fcbf49'),
            cells= dict(values=[[], [], []])
        )])

        fig.update_layout(
            title={
                'text': "Danh sách các bài kiểm tra có điểm dưới 70",
                'x': 0.2,
                'xanchor': 'left',
                'yanchor': 'top',
                'font': dict(size=20, family='Times New Roman', color='black')
            },
            height= 600,  
            width = 600,
            margin=dict(l=10, r=10, t=50, b=10)
        )

        # fig.show()

        fig_json = fig.to_json()
        return fig_json
    
    else:
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=list(columns),
                fill_color='#fcbf49',
                align='center',
                height=30,
                font=dict(size=14, color='black', family='Times New Roman')
            ),
            cells=dict(
                values=[df_score_title[col] for col in df_score_title.columns],
                fill_color='#ffe6a7',
                align='center',
                height=30,
                font=dict(size=13, color='black', family='Times New Roman')
            )
        )])
        
        # Cập nhật layout
        fig.update_layout(
            title={
                'text': "Danh sách các bài kiểm tra có điểm dưới 70",
                'x': 0.2,
                'xanchor': 'left',
                'yanchor': 'top',
                'font': dict(size=20, family='Times New Roman', color='black')
            },
            height= 600,  
            width = 600,
            margin=dict(l=10, r=10, t=50, b=10)
        )

        # fig.show()

        fig_json = fig.to_json()
        return fig_json

# chart_score_title("dc139449-56ea-4fd6-89b2-a7db8a0dd46f")
    
