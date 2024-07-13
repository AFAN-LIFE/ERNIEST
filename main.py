import streamlit as st
from database.initialize import initialize_database

# 初始化sqlite数据库
initialize_database()

# 登录模块
login_area = st.empty()
if 'login_success' not in st.session_state:
    st.session_state.login_success = False
if not st.session_state.login_success:
    from view.login import login_view

    with st.container(height=600):
        login_view(st)

# 侧边栏和对话模块
if st.session_state.login_success:
    from view.sidebar import sidebar_view
    from view.chat import chat_view
    sidebar_view(st)
    chat_view(st)
