def get_project_info():
    author_name = 'AFAN是金融科技行业的资深从业者，B站账号是AFAN的金融科技，欢迎联系他的微信:afan-life，他的邮箱是fcncassandra@gmail.com'
    llm = '文心一言（英文名：ERNIE Bot）是百度全新一代知识增强大语言模型，文心大模型家族的新成员，能够与人对话互动、回答问题、协助创作，高效便捷地帮助人们获取信息、知识和灵感。'
    framework = 'Streamlit是一个面向机器学习和数据科学团队的开源应用程序框架，通过它可以用python代码方便快捷的构建交互式前端页面'
    res_dict = {'author_name': author_name, 'llm': llm, 'framework': framework,
                'message': '更多有关项目的使用介绍，可以联系作者，或访问https://github.com/AFAN-LIFE/ERNIEST'}
    return res_dict