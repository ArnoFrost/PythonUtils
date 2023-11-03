import os

import torch
from PIL import Image
from googletrans import Translator
from transformers import CLIPProcessor, CLIPModel

from scripts.ai.VectorDatabase import VectorDatabase

# 常量定义
DIRECTORY_PATH = "/Users/xuxin14/Documents/Backup/头像/训练"
DB_PATH = os.path.join(DIRECTORY_PATH, "vector_db.pkl")


class ClipSearchEngine:
    def __init__(self, model_name="openai/clip-vit-large-patch14", translate_from='zh-CN', translate_to='en'):
        self.model = CLIPModel.from_pretrained(model_name)
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.translator = Translator()
        self.translate_from = translate_from
        self.translate_to = translate_to

    def translate_to_english(self, text):
        translation = self.translator.translate(text, src='zh-CN', dest='en')
        return translation[0].text

    def get_image_vector(self, image_path):
        image = Image.open(image_path)
        inputs = self.processor(text=["dummy"], images=image, return_tensors="pt", padding=True)
        outputs = self.model(**inputs)
        return outputs.image_embeds.squeeze().cpu().detach().numpy()

    def get_text_vector(self, text_description: list[str]):
        dummy_image = torch.zeros(1, 3, 224, 224)
        inputs = self.processor(text=text_description, images=dummy_image, return_tensors="pt", padding=True)
        outputs = self.model(**inputs)
        return outputs.text_embeds.squeeze().cpu().detach().numpy()


def initialize_or_load_db(db_path):
    db = VectorDatabase(db_file=db_path, dimension=768)
    if not os.path.exists(db_path):
        db.save_to_file()
    return db


def save_image_vectors(engine: ClipSearchEngine, db: VectorDatabase, directory_path: str, file_types: tuple):
    for filename in os.listdir(directory_path):
        if filename.endswith(file_types):
            file_path = os.path.join(directory_path, filename)
            vector = engine.get_image_vector(file_path)
            db.add_vector(vector, file_path)


def search_images_by_text(engine: ClipSearchEngine, text_description: list[str], db: VectorDatabase,
                          min_similarity_score=0):
    text_vector = engine.get_text_vector(text_description)
    results = db.search_vector(text_vector, k=len(db.file_paths))
    # 过滤同时满足分数条件的选项
    filtered_results = [result for result in results if result[1] <= min_similarity_score]
    return filtered_results


if __name__ == '__main__':
    FILE_TYPES = (".jpg", ".png", ".jpeg", ".webp")

    search_engine = ClipSearchEngine()
    db = initialize_or_load_db(DB_PATH)
    save_image_vectors(search_engine, db, DIRECTORY_PATH, FILE_TYPES)

    topK = 10
    min_similarity_score = 1.7
    text_description = ["车辆"]
    translated_descriptions = search_engine.translate_to_english(text_description)
    print(translated_descriptions)

    results = search_images_by_text(search_engine, translated_descriptions, db, min_similarity_score)
    for path, score in results[:topK]:
        print(f"Image: {path}, Similarity: {score:.4f}")
