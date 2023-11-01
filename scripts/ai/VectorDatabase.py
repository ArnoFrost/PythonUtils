import os
import pickle

import faiss
import numpy as np


class VectorDatabase:
    db_file = None

    def __init__(self, db_file: str = "vector_database.pkl", dimension=768):
        self.dimension = dimension
        self.db_file = db_file
        if os.path.exists(self.db_file):
            self.load_from_file()
        else:
            self.index = None if self.dimension is None else faiss.IndexFlatL2(self.dimension)
            self.file_paths = []

    def add_vector(self, vector, file_path):
        """添加一个向量及其关联的文件路径到数据库"""
        self.index.add(np.array([vector]))
        self.file_paths.append(file_path)
        self.save_to_file()

    def search_vector(self, vector, k=1):
        """在数据库中查询最近的k个向量"""
        distances, indices = self.index.search(np.array([vector]), k)
        return [(self.file_paths[i], distances[0][j]) for j, i in enumerate(indices[0])]

    def save_to_file(self):
        with open(self.db_file, 'wb') as f:
            pickle.dump({'index': self.index, 'file_paths': self.file_paths}, f)

    def load_from_file(self):
        with open(self.db_file, 'rb') as f:
            data = pickle.load(f)
            self.index = data['index']
            self.file_paths = data['file_paths']

# # 示例用法
# db = VectorDatabase()
#
# # 假设v1, v2, v3是从三个文件中提取的向量
# v1 = np.random.rand(512).astype('float32')
# v2 = np.random.rand(512).astype('float32')
# v3 = np.random.rand(512).astype('float32')
#
# # 向数据库中添加向量和相关文件路径
# db.add_vector(v1, "file_path_1.jpg")
# db.add_vector(v2, "file_path_2.jpg")
# db.add_vector(v3, "file_path_3.jpg")
#
# # 查询与v1最相似的2个向量
# results = db.search_vector(v1, k=2)
# print(results)  # 输出与v1最相似的文件路径及其距离
