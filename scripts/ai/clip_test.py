import os

import torch
from PIL import Image
from googletrans import Translator
from transformers import CLIPProcessor, CLIPModel

from scripts.ai.VectorDatabase import VectorDatabase

# 初始化模型处理器
model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
translator = Translator()
directory_path = "/Users/xuxin14/Documents/Backup/头像/训练"
DB_PATH = os.path.join(directory_path, "vector_db.pkl")

# 初始化数据库
db = VectorDatabase(db_file=DB_PATH, dimension=768)
# 保存数据库
if not os.path.exists(DB_PATH):
    db.save_to_file()


def translate_to_english(text):
    translation = translator.translate(text, src='zh-CN', dest='en')
    return translation[0].text


def get_image_vector(image_path):
    image = Image.open(image_path)
    inputs = processor(text=["dummy"], images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    return outputs.image_embeds.squeeze().cpu().detach().numpy()


def get_text_vector(text_description: list[str]):
    dummy_image = torch.zeros(1, 3, 224, 224)
    inputs = processor(text=text_description, images=dummy_image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    return outputs.text_embeds.squeeze().cpu().detach().numpy()


def save_image_vectors(db: VectorDatabase, directory_path: str):
    for filename in os.listdir(directory_path):
        if filename.endswith((".jpg", ".png", ".jpeg", ".webp")):
            file_path = os.path.join(directory_path, filename)
            vector = get_image_vector(file_path)

            db.add_vector(vector, file_path)


def search_images_by_text(text_description: list[str], db):
    text_vector = get_text_vector(text_description)
    return db.search_vector(text_vector, k=len(db.file_paths))


if __name__ == '__main__':
    save_image_vectors(db, directory_path)

    topK = 2
    text_description = ["车辆"]
    # 进行翻译
    translated_descriptions = translate_to_english(text_description)
    print(translated_descriptions)

    # 检索结果
    results = search_images_by_text(translated_descriptions, db)

    for path, score in results[:topK]:
        print(f"Image: {path}, Similarity: {score:.4f}")
