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
            self.index = faiss.IndexIDMap(faiss.IndexFlatL2(dimension))
            self.file_paths = []

    def add_vector(self, vector, file_path):
        """添加一个向量及其关联的文件路径到数据库，或者更新现有的向量"""
        if self.file_path_exists(file_path):
            idx = self.file_paths.index(file_path)
            self.index.remove_ids(np.array([idx]))
            self.index.add_with_ids(np.array([vector], dtype=np.float32), np.array([idx]))
        else:
            idx = len(self.file_paths)
            self.index.add_with_ids(np.array([vector], dtype=np.float32), np.array([idx]))
            self.file_paths.append(file_path)

    def search_vector(self, vector, k=1):
        """在数据库中查询最近的k个向量"""
        distances, indices = self.index.search(np.array([vector], dtype=np.float32), k)
        return [(self.file_paths[i], distances[0][j]) for j, i in enumerate(indices[0])]

    def save_to_file(self):
        with open(self.db_file, 'wb') as f:
            pickle.dump({'index': self.index, 'file_paths': self.file_paths}, f)

    def load_from_file(self):
        with open(self.db_file, 'rb') as f:
            data = pickle.load(f)
            self.index = data['index']
            self.file_paths = data['file_paths']

    def file_path_exists(self, file_path):
        """检查给定的文件路径是否已经存在于数据库中"""
        return file_path in self.file_paths
