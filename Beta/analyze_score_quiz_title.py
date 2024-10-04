import query_score_quiz_title
import pandas as pd
from collections import defaultdict

def create_score_table(user_id):
    quiz_title, quiz_score_under = query_score_quiz_title.query_score_title(user_id)

    if not quiz_title or not quiz_score_under:
        return pd.DataFrame(columns=['0-25', '26-50', '51-69'])
    
    # Dictionary để lưu trữ tiêu đề theo nhóm điểm
    score_groups = defaultdict(list)
    
    for title, score in zip(quiz_title, quiz_score_under):
        if 0 <= score <= 25:
            score_groups['0-25'].append(title)
        elif 26 <= score <= 50:
            score_groups['26-50'].append(title)
        elif 51 <= score <= 69:
            score_groups['51-69'].append(title)
    
    # Tìm độ dài lớn nhất trong các nhóm
    max_length = max(len(group) for group in score_groups.values())
    
    # Tạo DataFrame với các cột có độ dài bằng nhau
    df_score_title = pd.DataFrame({
        '0-25': score_groups['0-25'] + [''] * (max_length - len(score_groups['0-25'])),
        '26-50': score_groups['26-50'] + [''] * (max_length - len(score_groups['26-50'])),
        '51-69': score_groups['51-69'] + [''] * (max_length - len(score_groups['51-69']))
    })
    
    # print(df_score_title)

    return df_score_title

# create_score_table("dc139449-56ea-4fd6-89b2-a7db8a0dd46f")