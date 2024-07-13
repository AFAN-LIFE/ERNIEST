from view.tool import get_image_base64

def login_view(st_object):
    if 'login_success' not in st_object.session_state:
        st_object.session_state.login_success = False
    if 'user_name' not in st_object.session_state:
        st_object.session_state.user_name = None
    if 'prepare_login' not in st_object.session_state:
        st_object.session_state.prepare_login = False
    image_path = 'asset/erniest.png'
    img_base64 = get_image_base64(image_path)
    # 使用HTML和CSS居中对齐图片
    html_string = f"""
        <div style="display: flex; flex-direction: column; align-items: center;">
            <img src="data:image/png;base64,{img_base64}" alt="changtianml.com" style="width: 30%;">
            <h1>ERNIEST</h1>
        </div>
    """
    st_object.markdown(html_string, unsafe_allow_html=True)
    st_object.markdown('<div style="text-align:center"><strong>基于百度ERNIE和Streamlit的开源大模型交流平台</strong></div>', unsafe_allow_html=True)
    # 用户名和密码输入
    login_u1, login_u2, _ = st_object.columns([2, 2, 1])
    login_u1.markdown(
        '<div style="text-align:right; padding-right: 30px; padding-top: 30px;"><strong>用户名称：</strong></div>',
        unsafe_allow_html=True)
    login_user_name = login_u2.text_input('', 'admin', placeholder='建议填写，以此区分不同用户', key='login_u2')
    login_p1, login_p2, _ = st_object.columns([2, 2, 1])
    login_p1.markdown(
        '<div style="text-align:right; padding-right: 30px; padding-top: 30px;"><strong>用户密码：</strong></div>',
        unsafe_allow_html=True)
    login_user_pwd = login_p2.text_input('', placeholder='无需填写，可用于二次开发', key='login_p2')
    # 登录和注册按钮
    _, login_b1, login_b2, _ = st_object.columns([3, 2, 2, 3])
    login_click = login_b1.button('确认登录', key='login', type='primary')
    login_b2.link_button('使用说明', 'https://github.com/AFAN-LIFE/ERNIEST')
    if login_click:
        st_object.session_state.prepare_login = True
    if st_object.session_state.prepare_login:
        st_object.session_state.prepare_login = False
        from auth import login
        login(st_object, login_user_name, login_user_pwd)
        if st_object.session_state.login_success:
            st_object.markdown(
                f'<div style="color: green; font-weight: bold; text-align: center;">登录成功!</div>',
                unsafe_allow_html=True)
        else:
            st_object.markdown(
                '<div style="color: red; font-weight: bold; text-align: center;">账号或密码输入错误，登录失败请重试</div>',
                unsafe_allow_html=True)