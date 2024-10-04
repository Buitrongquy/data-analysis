from flask import Flask, jsonify, request, render_template
import json
import chart_course
import chart_lesson_day
import chart_average_time_day
import chart_time_week
import chart_count_lesson_day
import chart_count_lesson_week
import chart_quiz_week
import chart_quiz_score
import chart_score_6
import chart_quiz_average_score_week
import chart_score_quiz_title
import chart
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('web.html')

@app.route('/api/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400

        user_id = data.get('user_id', '')
        test = data.get('test', '')

        if not user_id:
            return jsonify({"error": "Vui lòng nhập họ tên."}), 400

        if test:
             #print("Đây là chế độ phân tích bài test cho", full_name)
            
            get_time_quiz = chart.get_time_quiz(test)
            #calculate_completion_rate = chart.calculate_completion_rate(test)
            number_user_join = chart.number_user_join(test)
            get_avg_duration_per_quiz = chart.get_avg_duration_per_quiz(test)
            score_group = chart.score_group(test)
            distribution_score = chart.distribution_score(test)
            compare_scores = chart.compare_scores(user_id)
            get_user_score = chart.get_user_score(user_id, test)
            get_rank = chart.get_rank(user_id, test)
            respone = {
                "mode":"analysis test",
                "full_name": user_id,
                "get_time_quiz": get_time_quiz,
                #"calculate_completion_rate": calculate_completion_rate,
                "number_user_join": number_user_join,
                "get_avg_duration_per_quiz": get_avg_duration_per_quiz,
                "score_group": score_group,
                "distribution_score": distribution_score,
                "compare_scores": compare_scores,
                "get_user_score": get_user_score,
                "get_rank": get_rank,
            }

            # with open("respone analysis test.json",'w',encoding='utf-8') as file:
            #     json.dump(respone,file)

            return jsonify(respone),200
        else:
            average_time_chart = chart_average_time_day.average_time_day(user_id)
            course_chart = chart_course.course(user_id)
            lesson_day_chart = chart_lesson_day.lesson_day(user_id)
            time_week_chart = chart_time_week.time_week(user_id)
            count_lesson_day_chart = chart_count_lesson_day.count_lesson_day(user_id)
            count_lesson_week_chart = chart_count_lesson_week.count_lesson_week(user_id)
            quiz_week_chart = chart_quiz_week.quiz_week(user_id)
            quiz_score_chart = chart_quiz_score.quiz_score(user_id)
            score_6_chart = chart_score_6.score_6(user_id)
            score_title = chart_score_quiz_title.chart_score_title(user_id)
            quiz_average_score_chart = chart_quiz_average_score_week.quiz_average_score(user_id)
            respone = {
                "mode":"analysis performance",
                "user_id": user_id,
                "course_chart": course_chart,
                "lesson_day_chart": lesson_day_chart,
                "average_time_chart": average_time_chart,
                "time_week_chart": time_week_chart,
                "count_lesson_day_chart": count_lesson_day_chart,
                "count_lesson_week_chart": count_lesson_week_chart,
                "quiz_week_chart": quiz_week_chart,
                "quiz_score_chart": quiz_score_chart,
                "score_6_chart": score_6_chart,
                "score_title": score_title,
                "quiz_average_score_chart": quiz_average_score_chart,
            }
            # with open("respone analysis performence.json",'w',encoding='utf-8') as file:
            #     json.dump(respone,file)
            #print("value",respone)

            return jsonify(respone),200

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "Đã xảy ra lỗi nội bộ server"}), 500

if __name__ == '__main__':
    app.run(debug=True)