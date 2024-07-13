import datetime, sqlite3
from database.connection import gpt_connection

def get_convsation_via_user(user_name) -> list:
    cursor = gpt_connection.cursor()
    sql = "SELECT * FROM Conversations WHERE user_name = ? AND is_deleted = 0 ORDER BY end_time DESC"
    cursor.execute(sql, (user_name,))
    conversations = cursor.fetchall()
    return conversations

def get_conversation_dict(user_name) -> dict:
    conversations = get_convsation_via_user(user_name)
    # 获取今天的日期
    today = datetime.datetime.now()
    # 初始化不同时间段的会话列表
    today_sessions = []
    yesterday_sessions = []
    past_7_days_sessions = []
    past_30_days_sessions = []
    earlier_sessions = []
    # 将会话按时间分类，以最后的对话时间来算
    print(conversations)
    for conv in conversations:
        start_time = datetime.datetime.strptime(conv["end_time"], '%Y-%m-%d %H:%M:%S.%f')
        delta_days = (today - start_time).days
        if delta_days == 0:
            today_sessions.append(conv)
        elif delta_days == 1:
            yesterday_sessions.append(conv)
        elif delta_days <= 7:
            past_7_days_sessions.append(conv)
        elif delta_days <= 30:
            past_30_days_sessions.append(conv)
        else:
            earlier_sessions.append(conv)
    return {'今天': today_sessions, '昨天': yesterday_sessions, '前7天': past_7_days_sessions,
            '前30天': past_30_days_sessions, '更早': earlier_sessions}


def create_conversation(user_name, prompt):
    cursor = gpt_connection.cursor()
    sql = "INSERT INTO Conversations (user_name, start_time, end_time, theme) VALUES (?, ?, ?, ?)"
    start_time = end_time = datetime.datetime.now()
    try:
        cursor.execute(sql, (user_name, start_time, end_time, prompt[:100]))
        gpt_connection.commit()
    except Exception as e:
        print('create_conversation报错：', e)
        gpt_connection.rollback()
    conversation_id = cursor.lastrowid
    return conversation_id


def update_conversation_time(c_id):
    cursor = gpt_connection.cursor()
    sql = "UPDATE Conversations SET end_time = ? WHERE id = ? AND is_deleted = 0"
    end_time = datetime.datetime.now()
    try:
        cursor.execute(sql, (end_time, c_id))
        gpt_connection.commit()
    except Exception as e:
        print('update_conversation_time报错：', e)
        gpt_connection.rollback()


def create_message(c_id, user_name, prompt):
    cursor = gpt_connection.cursor()
    sql = "INSERT INTO Messages (conversation_id, sender, message) VALUES (?, ?, ?)"
    try:
        cursor.execute(sql, (c_id, user_name, prompt))
        gpt_connection.commit()
    except Exception as e:
        print('create_message报错：', e)
        gpt_connection.rollback()

def get_message_via_cid(c_id):
    cursor = gpt_connection.cursor()
    sql = "SELECT * FROM Messages WHERE conversation_id = ? AND is_deleted = 0"
    cursor.execute(sql, (c_id,))
    messages = cursor.fetchall()
    return messages