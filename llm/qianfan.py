import json
import os
from config import default_robot_name
from log import log_function_call
from function.register import functions


@log_function_call
def dispatch_function(function_call, st_object):
    from function.description import get_project_info
    name2function = {'get_project_info': get_project_info}
    func_name = function_call['name']
    arguments = function_call['arguments']
    origin_dict = json.loads(arguments)
    return name2function[func_name](**origin_dict)


@log_function_call
def get_qianfan_response(messages, st_object):
    import qianfan
    config = qianfan.get_config()
    config.ACCESS_TOKEN = st_object.session_state.token  # 每次都获取当前最新的token
    # 调用方法参考：https://cloud.baidu.com/doc/WENXINWORKSHOP/s/jlil56u11和github文档https://github.com/baidubce/bce-qianfan-sdk
    # 高级的模型调用付费，但支持function call
    if st_object.session_state.model == 'ernie-3.5-8k':
        response = qianfan.ChatCompletion().do(
            model=st_object.session_state.model,
            messages=messages,
            functions=functions,
            stream=False
        )
        if response.get("function_call"):
            function_call = response["function_call"]
            func_result = dispatch_function(function_call, st_object)
            new_messages = messages.copy()
            new_messages.append({'role': default_robot_name, 'content': None, 'function_call': response['function_call']})
            new_messages.append({'role': 'function', 'name': function_call['name'],
                                 'content': json.dumps(func_result, ensure_ascii=False)})
            # 将结果返回进行润色
            final_response = qianfan.ChatCompletion().do(model=st_object.session_state.model, messages=new_messages,
                                                         top_p=0.2, functions=functions, stream=False)
            final_result = final_response['body']['result']
            return final_result
        else:
            result = response['body']['result']
            return result
    # 简单的模型调用免费，但不支持function call
    elif st_object.session_state.model == 'ernie-speed-128k':
        response = qianfan.ChatCompletion().do(
            model=st_object.session_state.model,
            messages=messages,
            stream=False
        )
        result = response['body']['result']
        return result
    else:
        raise Exception('当前仅支持ernie-4.0和ernie-speed两种模型')
