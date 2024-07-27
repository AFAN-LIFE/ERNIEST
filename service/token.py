import json, datetime
from database.connection import gpt_connection
from config import token_limit, token_input_limit, token_output_limit


def create_token_stat(user_name, c_id, model_name, length, token_type):
    cursor = gpt_connection.cursor()
    sql = "INSERT INTO token_stats (user_name, conversation_id, model_name, length, token_type) VALUES (?, ?, ?, ?, ?)"
    try:
        cursor.execute(sql, (user_name, c_id, model_name, length, token_type))
        gpt_connection.commit()
    except Exception as e:
        print('create_token_stat报错：', e)
        gpt_connection.rollback()


def save_token_input(st_object, model_name: str, messages: list):
    # 多轮会话要统计历史输入，这里简单计数，不转换成token计数了
    # 如果触发了function_call，则第一轮返回的内容只有function_call没有content
    length = sum([len(i['content']) if i['content'] else len(json.dumps(i['function_call'])) for i in messages])
    c_id = st_object.session_state.conversation_id
    user_name = st_object.session_state.user_name
    create_token_stat(user_name, c_id, model_name, length, 0)


def save_token_output(st_object, model_name: str, message: str):
    length = len(message)  # 简单计数，不转换成token计数了
    c_id = st_object.session_state.conversation_id
    user_name = st_object.session_state.user_name
    create_token_stat(user_name, c_id, model_name, length, 1)


def judge_token_limit(user_name):
    # 这边简单统计1天有没有达到token的上限
    today = datetime.datetime.now()
    cursor = gpt_connection.cursor()
    sql = "SELECT * FROM token_stats WHERE user_name = ? AND date(timestamp) = date('now')"
    cursor.execute(sql, (user_name,))
    token_stat: list = cursor.fetchall()
    # 还可以单独统计各模型当日使用
    input_sum = sum([i['length'] if i['token_type'] == 0 else 0 for i in token_stat])
    output_sum = sum([i['length'] if i['token_type'] == 1 else 0 for i in token_stat])
    total_sum = input_sum + output_sum
    # 可区分总输入输出、输入、输出
    if total_sum >= token_limit:
        return 1, '当前已超过超过今日用户token上限，请明日再来使用'
    elif input_sum >= token_input_limit:
        return 1, '当前已超过超过今日用户token输入上限，请明日再来使用'
    elif output_sum >= token_output_limit:
        return 1, '当前已超过超过今日用户token输出上限，请明日再来使用'
    else:
        return 0, '未超过token限制'
