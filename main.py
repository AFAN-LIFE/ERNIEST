import streamlit as st
from database.initialize import initialize_database

# 初始化sqlite数据库
if 'initialize_database' not in st.session_state:
    st.session_state.initialize_database = False
if not st.session_state.initialize_database:
    initialize_database()
    st.session_state.initialize_database = True

# 登录模块
login_area = st.empty()
if 'login_success' not in st.session_state:
    st.session_state.login_success = False
if not st.session_state.login_success:
    from view.login import login_view
    with login_area:
        with st.container(height=600):
            login_view(st)
    if st.session_state.login_success:
        login_area.empty()

# 侧边栏和对话模块
if st.session_state.login_success:
    from view.sidebar import sidebar_view
    from view.chat import chat_view
    sidebar_view(st)
    chat_view(st)
