# 参考：json-schema：https://json-schema.org/understanding-json-schema/reference
get_project_info_desc = {
    'name': 'get_project_info',
    'description': "在用户询问：ERNIEST是什么项目/这是什么/这是什么项目/你是谁/你的作者是谁/你是什么大模型/你用什么编写的，等情况的时候触发",
    'parameters': {
        'type': 'object',
        'required': [
            'properties',
        ],
    },
    'responses': {
        'type': 'object',
        'properties': {
            'response': {
                'type': 'string',
                'description': "项目的作者、使用的大模型的名称和框架名称",
                'properties': {
                    'author_name': {'type': 'string', 'description': "作者名称"},
                    'llm': {'type': 'string', 'description': "大模型名称"},
                    'framework': {'type': 'string', 'description': "框架名称"},
                },
            }
        },
    },
}

functions = [get_project_info_desc]