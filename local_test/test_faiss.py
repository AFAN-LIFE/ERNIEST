# 参考：https://github.com/facebookresearch/faiss/wiki/Getting-started

# 1 查询
## Getting some data
import numpy as np

d = 64  # dimension
nb = 100000  # database size
nq = 10000  # nb of queries
np.random.seed(1234)  # make reproducible
xb = np.random.random((nb, d)).astype('float32')
# 给各自64个维度中的第一个维度逐步从0加到100或者10，目的是看到一个索引变化
xb[:, 0] += np.arange(nb) / 1000.  #
xq = np.random.random((nq, d)).astype('float32')
xq[:, 0] += np.arange(nq) / 1000.

## Building an index and adding the vectors to it
import faiss  # make faiss available

index = faiss.IndexFlatL2(d)  # build the index
print(index.is_trained)
index.add(xb)  # add vectors to the index
print(index.ntotal)

## Searching
k = 4  # we want to see 4 nearest neighbors
D, I = index.search(xb[:5], k)  # sanity check
print(I)  # 可以看到索引矩阵的第一列都是自己，证明匹配逻辑正确
print(D)  # 索引对应向量的距离大小，可以看到距离从左到右也在不断增加
D, I = index.search(xq, k)  # actual search
print(I[:5])  # neighbors of the 5 first queries
print(I[-5:])  # neighbors of the 5 last queries

# 2 存储