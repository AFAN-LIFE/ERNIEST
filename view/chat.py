import time
from config import default_robot_name, default_user_name
from service.conversation import update_conversation_time, create_conversation, create_message

def chat_view(st_object):
    st_object.title("ERNIEST")
    st_object.markdown("百度ERNIE-SDK+Streamlit的大模型交流平台")

    def response_generator(messages: list):
        from llm.ernie import get_ernie_response
        response = get_ernie_response(messages, st_object)
        return response

    # 得到返回结果后，按照一个时间间隔缓慢输出
    # TODO: ERNIE-SDK的流式返回没有提供function_call的调用方式，因此使用全量返回方式，待官方提供文档：https://github.com/PaddlePaddle/ERNIE-SDK/issues/351
    def stream_return(string, interval=0.05):
        for word in string:
            yield word + ""
            time.sleep(interval)

    # 展示用户选择的历史会话的内容
    for message in st_object.session_state.messages:
        with st_object.chat_message(message["role"]):
            st_object.markdown(message["content"])

    # 获取用户输入的信息
    if prompt := st_object.chat_input("What is up?"):
        # 把用户的消息添加到前端的缓存中
        st_object.session_state.messages.append({"role": default_user_name, "content": prompt})
        # 如果是新会话
        if st_object.session_state.conversation_id == None:
            c_id = create_conversation(st_object.session_state.user_name, prompt)
            st_object.session_state.conversation_id = c_id
        else:  # 否则就更新老对话的时间
            update_conversation_time(st_object.session_state.conversation_id)
        # 存储用户发送的消息
        create_message(st_object.session_state.conversation_id, st_object.session_state.user_name, prompt)
        # 在用户的对话框中进行前端展示
        with st_object.chat_message(default_user_name):
            st_object.markdown(prompt)
        # 在机器的对话框中进行前端展示
        with st_object.chat_message(default_robot_name):
            default = '小天正在思考，请稍后...'
            st_object.write_stream(stream=iter(default))
            # try:
            response_content = response_generator(st_object.session_state.messages)
            # except Exception as e:
            #     response_content = f'抱歉，系统出错了，请稍后重试或联系管理员, {e}'
            # 先存储，防止用户觉得麻烦先退出了
            create_message(st_object.session_state.conversation_id, default_robot_name, response_content)
            response = st_object.write_stream(stream_return(response_content))
        # 把机器的消息添加到前端的缓存中
        st_object.session_state.messages.append({"role": default_robot_name, "content": response})
