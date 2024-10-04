import analyze_course
import plotly.graph_objects as go
import numpy as np

def course(user_id):
    try:
        result_course = analyze_course.statistics_course(user_id)

        labels = np.array(['Tổng số khóa học chưa học','Tổng số khóa học đang học','Tổng số khóa học đã hoàn thành'])
        values = np.array(result_course)

        # Kiểm tra nếu tất cả giá trị đều là 0
        if np.all(values == 0):
            values = np.array([1, 1, 1])  # Đặt các giá trị bằng nhau để chia đều biểu đồ
            text = ['0', '0', '0']  # Hiển thị giá trị 0 trên biểu đồ
        else:
            text = values.astype(str)  # Hiển thị giá trị thực tế

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, 
                                    textinfo='text',text=text, 
                                    marker=dict(colors=['#EF5A6F', '#FFDE4D', '#88D66C']))])

        fig.update_layout(
            title={
                'text': "Thống kê khóa học đã đăng ký",
                'y':0.95, 
                'x':0.5,  
                'xanchor': 'center', 
                'yanchor': 'top'  
            },
        )

        # fig.show()

        # Trả về JSON
        fig_json = fig.to_json()
        return fig_json
    except Exception as e:
        print(f"An error occurred: {e}")
        # Trả về một JSON rỗng hoặc một giá trị mặc định nếu có lỗi
        return "{}"

# course("8e8f1ac2-44ee-4413-88d1-23072e0144fc")
