import os
import qianfan
from config import default_token
# https://cloud.baidu.com/doc/WENXINWORKSHOP/s/hlmokk9qn#%E5%8F%82%E6%95%B0%E8%AF%B4%E6%98%8E

config = qianfan.get_config()
config.ACCESS_TOKEN = ''  # 每次都获取当前最新的token
emb = qianfan.Embedding()

model = 'bge-large-zh'  # Embedding-V1"
resp = emb.do(model=model, texts=[  # 非默认模型，需填写 model参数
    "推荐一些美食", "给我讲个故事"
])

body = resp["body"]
len(body['data'][0]['embedding'])