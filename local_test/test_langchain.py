# https://python.langchain.com/v0.2/docs/how_to/
# https://api.python.langchain.com/en/latest/langchain_api_reference.html
# https://api.python.langchain.com/en/latest/community_api_reference.html#
# https://blog.csdn.net/oHeHui1/article/details/136323004
# https://blog.csdn.net/u013066244/article/details/132014791

import os
import getpass
from langchain_community.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# 1 本地分词
loader = TextLoader(r"", encoding='utf-8')
documents = loader.load()
# separator默认是\n\n需要两个空行，chunk_overlap是保留重叠部分
text_splitter = CharacterTextSplitter(separator="\n", chunk_size=500, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
print(sum([len(i.page_content) for i in docs]))

# 2 在线embedding并检索
from langchain.embeddings.baidu_qianfan_endpoint import QianfanEmbeddingsEndpoint
qianfan_ak = ""
qianfan_sk = ""
# 注意这里是embedding对象，后面在获取文档向量后会有embeddings真正的结果
embedding = QianfanEmbeddingsEndpoint(qianfan_ak=qianfan_ak, qianfan_sk =qianfan_sk)
db = FAISS.from_documents(docs, embedding)
query = "KNN的算法原理是什么？"
result_docs = db.similarity_search(query)
print(result_docs[0].page_content)
db_path = 'local_test/qianfan.db'
# faiss是索引，pkl是文档
db.save_local(db_path)  # 存到本地

'''
# 形成embeddings过程中，内部把文档比如有128个，又除以16形成批请求去获取embeddings了
chunk_size = embedding.chunk_size
texts = docs.copy()
text_in_chunks = [
    texts[i: i + chunk_size]
    for i in range(0, len(texts), chunk_size)
]
len(text_in_chunks)
len(text_in_chunks[0])
'''

# 3 从本地加载
# 此时这个embedding的目的是将Question转成向量检索用，而不是再和知识库相关
from langchain_community.vectorstores import FAISS
from langchain.embeddings.baidu_qianfan_endpoint import QianfanEmbeddingsEndpoint
qianfan_ak = ""
qianfan_sk = ""
db_path = 'local_test/qianfan.db'
embedding = QianfanEmbeddingsEndpoint(qianfan_ak=qianfan_ak, qianfan_sk =qianfan_sk)
db = FAISS.load_local(db_path, embedding, allow_dangerous_deserialization=True)
# retriever = vectorstore.as_retriever()
query = "KNN的算法原理是什么？"
result_docs = db.similarity_search(query)
print(result_docs[0].page_content)