from config import default_token
from streamlit_modal import Modal
from view.tool import get_image_base64
from config import default_robot_name, default_user_name
from service.conversation import get_conversation_dict, get_message_via_cid


def generate_token(API_KEY, Secret_Key):
    import requests
    import json
    def main():
        url = f"https://aip.baidubce.com/oauth/2.0/token?client_id={API_KEY}&client_secret={Secret_Key}&grant_type=client_credentials"
        payload = json.dumps("")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    try:
        response = main()
        access_token = response.get("access_token")
        return "success", access_token
    except Exception as e:
        return "error", e


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
    if 'token' not in st_object.session_state:  # 增加token统计
        st_object.session_state.token = ''
    t1, t2 = st_object.sidebar.columns([2, 1])
    token_text = t1.text_input("", placeholder="请输入token", type="password", value=default_token)
    if token_text:
        st_object.session_state.token = token_text
    if 'generator_modal' not in st_object.session_state:
        st_object.session_state.generator_modal = False
    if 'generate_button' not in st_object.session_state:
        st_object.session_state.generate_button = False
    t2.text("")
    t2.text("")
    generator = t2.button("生成", key='generate_token_button')
    if generator:
        st_object.session_state.generator_modal = True
    if st_object.session_state.generator_modal:
        generator_modal = Modal(title="生成token", key="generate_modal", max_width=400)
        with generator_modal.container():  # 弹出控件
            API_KEY = st_object.text_input(label="请输入API KEY", placeholder="")
            Secret_KEY = st_object.text_input(label="请输入Secret KEY", placeholder="")
            g1, g2, g3 = st_object.columns([1, 1, 1])
            generate_button = g1.button("生成token", key='start_generate', type='primary')
            g2.link_button("帮助文档", 'https://cloud.baidu.com/article/1089328')
            if API_KEY != "" and Secret_KEY != "" and generate_button:
                token_status, token_data = generate_token(API_KEY, Secret_KEY)
                if token_status == "success":
                    st_object.markdown(
                        f'<div style="color: green; font-weight: bold; text-align: center;">token产生成功，请复制：{token_data}</div>',
                        unsafe_allow_html=True)
                else:
                    st_object.markdown(
                        f'<div style="color: red; font-weight: bold; text-align: center;">token生成失败，原因是：{token_data}</div>',
                        unsafe_allow_html=True)
            if g3.button('点击返回', key='return_back'):
                st_object.session_state.generator_modal = False
                generator_modal.close()

    model = st_object.sidebar.selectbox('请选择模型', ('ernie-speed-128k', 'ernie-3.5-8k'))
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
        from view.chat import fix_abnormal_chat
        conversation_history: dict = get_conversation_dict(user_name)
        # 显示多个 sidebar，并确保只能选择一个
        for k, v in conversation_history.items():
            if len(v) > 0:
                generator.markdown(f"### {k}")
                select_zip = zip([str(i['id']) for i in v], [str(i['theme']) for i in v])
                for id, theme in select_zip:
                    # 用会话的第一条消息作为主题概括，只展示前15个字符，不然会跨行
                    if generator.button(theme[:15], use_container_width=True, key=id):  # 防止请求返回过程中被打断
                        st_object.session_state.conversation_id = id
                        messages = get_message_via_cid(st_object.session_state.conversation_id)
                        adj_messages = [
                            {'role': default_robot_name if i['sender'] == default_robot_name else default_user_name,
                             'content': i['message']} for i in messages]
                        st_object.session_state.messages = adj_messages  # 更新当前的消息列表
                        fix_abnormal_chat(st_object)  # 修复异常会话

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
