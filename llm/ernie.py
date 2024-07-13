import json
import erniebot
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
def get_ernie_response(messages, st_object):
    erniebot.api_type = 'aistudio'
    erniebot.access_token = st_object.session_state.token
    # 支持的模型列表：https://github.com/PaddlePaddle/ERNIE-SDK/blob/develop/docs/sdk/models.md
    # 高级的模型调用付费，但支持function call
    if st_object.session_state.model=='ernie-4.0':
        response = erniebot.ChatCompletion.create(
            model=st_object.session_state.model,
            messages=messages,
            functions=functions,
            stream=False
        )
        if response.is_function_response:
            function_call = response.get_result()
            func_result = dispatch_function(function_call, st_object)
            new_messages = messages.copy()
            new_messages.append(response.to_message())
            new_messages.append({'role': 'function', 'name': function_call['name'],
                                 'content': json.dumps(func_result, ensure_ascii=False)})
            # 将结果返回进行润色
            final_response = erniebot.ChatCompletion.create(model=st_object.session_state.model, messages=new_messages,
                                                            functions=functions, stream=False)
            final_result = final_response.get_result()
            return final_result
        else:
            result = response.get_result()
            return result
    # 简单的模型调用免费，但不支持function call
    elif st_object.session_state.model=='ernie-speed':
        response = erniebot.ChatCompletion.create(
            model=st_object.session_state.model,
            messages=messages,
            stream=False
        )
        result = response.get_result()
        return result
    else:
        raise Exception('当前仅支持ernie-4.0和ernie-speed两种模型')


if __name__ == '__main__':
    # 填充API Key与Secret Key
    import requests
    import json
    API_KEY = 'iA3YHBwOQtOAeSwXkQzS5upp'
    Secret_Key = '4Cxe4IZquPIUdiJk4Ubl2Xsbp9SJrbsH'
    def main():
        url = f"https://aip.baidubce.com/oauth/2.0/token?client_id={API_KEY}&client_secret={Secret_Key}&grant_type=client_credentials"
        payload = json.dumps("")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()
    response = main()
    access_token = response.get("access_token")
    print(response)
    print(access_token)
