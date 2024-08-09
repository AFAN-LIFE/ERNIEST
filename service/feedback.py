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
    @st_object.dialog('用户反馈')
    def feedback_dialog(st_object, real_idx, user_name, c_id, message_id):
        if st_object.session_state.feedback_event == 'thumbs_up':
            st_object.write("谢谢您的点赞！")
        elif st_object.session_state.feedback_event == 'thumbs_down':
            st_object.write("我们将继续努力，期待您的宝贵建议。")
        else:
            advice = st_object.text_input(label="请输入您的意见和建议", placeholder="", key=f"advice_input_{real_idx}")
            _, f1, f2, _ = st_object.columns([3, 2, 2, 3])
            if f1.button("提交", key=f'submit_feedback_{real_idx}', type='primary'):
                create_feedback(user_name, c_id, message_id, 'advice', advice)
                st_object.rerun()
    c_id = st_object.session_state.conversation_id
    user_name = st_object.session_state.user_name
    real_idx = int((message_id + 1) / 2)  # 大模型永远是奇数位置
    col1, col2, col3, _ = st_object.columns([1, 1, 1, 7])
    if col1.button('👍', key=f'thumbs_up{real_idx}'):
        st_object.session_state.feedback_event = 'thumbs_up'
        feedback_dialog(st_object, real_idx, user_name, c_id, message_id)
    if col2.button('👎', key=f'thumbs_down{real_idx}'):
        st_object.session_state.feedback_event = 'thumbs_down'
        feedback_dialog(st_object, real_idx, user_name, c_id, message_id)
    if col3.button('🗨️', key=f'advice{real_idx}'):
        st_object.session_state.feedback_event = 'advice'
        feedback_dialog(st_object, real_idx, user_name, c_id, message_id)

@DeprecationWarning
def feedback_by_modal(st_object, real_idx, user_name, c_id, message_id):
    if st_object.session_state.feedback_event:
        feedback_modal = Modal(title="用户反馈", key=f"feedback_modal_{real_idx}", padding=20, max_width=400)
        with feedback_modal.container():  # 弹出控件
            if st_object.session_state.feedback_event == 'thumbs_up':
                st_object.write("谢谢您的点赞！")
                create_feedback(user_name, c_id, message_id, 'thumbs_up', '')
            elif st_object.session_state.feedback_event == 'thumbs_down':
                st_object.write("我们将继续努力，期待您的宝贵建议。")
                create_feedback(user_name, c_id, message_id, 'thumbs_up', '')
            else:
                advice = st_object.text_input(label="请输入您的意见和建议", placeholder="", key=f"advice_input_{real_idx}")
                _, f1, f2, _ = st_object.columns([3, 2, 2, 3])
                if f1.button("提交", key=f'submit_feedback_{real_idx}', type='primary'):
                    create_feedback(user_name, c_id, message_id, 'advice', advice)
                    feedback_modal.close()
                if f2.button("返回", key=f'return_feedback_{real_idx}'):
                    feedback_modal.close()
            # 点击后就可以把状态置空了
            st_object.session_state.feedback_event = ''

