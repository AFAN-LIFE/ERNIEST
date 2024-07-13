from view.tool import get_image_base64
from config import default_robot_name, default_user_name
from service.conversation import update_conversation_time, create_conversation, create_message, get_conversation_dict, \
    get_message_via_cid

def sidebar_view(st_object):
    image_path = 'asset/erniest.png'
    img_base64 = get_image_base64(image_path)
    # 使用HTML和CSS居中对齐图片
    html_string = f"""
        <div style="display: flex; flex-direction: column; align-items: center;">
            <img src="data:image/png;base64,{img_base64}" alt="changtianml.com" style="width: 50%;">
        </div>
    """
    st_object.sidebar.markdown(html_string, unsafe_allow_html=True)
    st_object.sidebar.title(f"你好{st_object.session_state.user_name}")
    # st_object.sidebar.markdown('<div style="text-align:center"><a href="https://github.com/AFAN-LIFE/ERNIEST">项目介绍</a> &emsp;<a href="https://cloud.baidu.com/article/1089328">获取token</a></div>', unsafe_allow_html=True)
    if 'token' not in st_object.session_state:
        st_object.session_state.token = ''
    token = st_object.sidebar.text_input("请输入你的token", type="password")
    if token:
        st_object.session_state.token = token
    model = st_object.sidebar.selectbox('请选择模型', ('ernie-speed', 'ernie-4.0'))
    if model:
        st_object.session_state.model = model
    if "conversation_id" not in st_object.session_state:
        st_object.session_state.conversation_id = None
    if "messages" not in st_object.session_state:
        st_object.session_state.messages = []
    if st_object.sidebar.button('创建新会话  +', use_container_width=True, type='primary'):
        st_object.session_state.conversation_id = None
        st_object.session_state.messages = []

    def show_history_conversations(user_name, generator):
        conversation_history: dict = get_conversation_dict(user_name)
        # 显示多个 sidebar，并确保只能选择一个
        for k, v in conversation_history.items():
            if len(v) > 0:
                generator.markdown(f"### {k}")
                select_zip = zip([str(i['id']) for i in v], [str(i['theme']) for i in v])
                for id, theme in select_zip:
                    # 用会话的第一条消息作为主题概括，只展示前10个字符，不然会跨行
                    if generator.button(theme[:10], use_container_width=True, key=id):
                        st_object.session_state.conversation_id = id
                        messages = get_message_via_cid(st_object.session_state.conversation_id)
                        adj_messages = [
                            {'role': default_robot_name if i['sender'] == default_robot_name else default_user_name,
                             'content': i['message']} for i in messages]
                        st_object.session_state.messages = adj_messages


    col1, col2 = st_object.sidebar.columns([2, 1])
    col1.markdown("### 历史会话记录")
    refresh = col2.button('⟳')

    # 点击刷新后会更新历史主题列表
    st_object.session_state.refresh_conversation_list = False
    placeholder = st_object.sidebar.container()  # 创建一个容器占位符
    if refresh:
        st_object.session_state.refresh_conversation_list = True
    if st_object.session_state.refresh_conversation_list:
        with placeholder:
            show_history_conversations(st_object.session_state.user_name, st_object.sidebar)
        st_object.session_state.refresh_conversation_list = False
    else:
        with placeholder:
            show_history_conversations(st_object.session_state.user_name, st_object.sidebar)

