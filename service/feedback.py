from uuid import uuid4
from streamlit_modal import Modal
from database.connection import gpt_connection


def create_feedback(user_name, c_id, m_id, feedback_type, feedback_content):
    cursor = gpt_connection.cursor()
    sql = "INSERT INTO feedback (user_name, conversation_id, message_id, feedback_type, feedback_content) VALUES (?, ?, ?, ?, ?)"
    try:
        cursor.execute(sql, (user_name, c_id, m_id, feedback_type, feedback_content))
        gpt_connection.commit()
    except Exception as e:
        print('create_feedback报错：', e)
        gpt_connection.rollback()


def add_feedback(st_object, message_id):
    c_id = st_object.session_state.conversation_id
    user_name = st_object.session_state.user_name
    real_idx = int((message_id + 1) / 2)  # 大模型永远是奇数位置
    col1, col2, col3, _ = st_object.columns([1, 1, 1, 7])
    if col1.button('👍', key=f'thumbs_up{real_idx}'):
        st_object.session_state.feedback_event = 'thumbs_up'
    if col2.button('👎', key=f'thumbs_down{real_idx}'):
        st_object.session_state.feedback_event = 'thumbs_down'
    if col3.button('🗨️', key=f'advice{real_idx}'):
        st_object.session_state.feedback_event = 'advice'
    # TODO: 要修复多对话的情况下打开的问题
    if st_object.session_state.feedback_event:
        feedback_modal = Modal(title="用户反馈", key=f"feedback_modal_{real_idx}", max_width=400)
        with feedback_modal.container():  # 弹出控件
            if st_object.session_state.feedback_event == 'thumbs_up':
                st_object.write("谢谢您的点赞！")
                create_feedback(user_name, c_id, message_id, 'thumbs_up', '')
                st_object.session_state.feedback_event = ''
            elif st_object.session_state.feedback_event == 'thumbs_down':
                st_object.write("我们将继续努力，期待您的宝贵建议。")
                create_feedback(user_name, c_id, message_id, 'thumbs_up', '')
                st_object.session_state.feedback_event = ''
            else:
                advice = st_object.text_input(label="请输入您的意见和建议", placeholder="")
                _, f1, f2, _ = st_object.columns([3, 2, 2, 3])
                if f1.button("提交", key='submit_feedback', type='primary'):
                    create_feedback(user_name, c_id, message_id, 'advice', advice)
                    st_object.session_state.feedback_event = ''
                    feedback_modal.close()
                if f2.button("返回", key='return_feedback'):
                    st_object.session_state.feedback_event = ''
                    feedback_modal.close()