import os
import torch
from PIL import Image
from googletrans import Translator
from transformers import CLIPProcessor, CLIPModel
from scripts.ai.VectorDatabase import VectorDatabase

# 常量定义
DIRECTORY_PATH = "/Users/xuxin14/Documents/Backup/头像/训练"
DB_PATH = os.path.join(DIRECTORY_PATH, "vector_db.pkl")

# 初始化模型处理器
model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
translator = Translator()


def initialize_or_load_db(db_path):
    """初始化或加载数据库"""
    db = VectorDatabase(db_file=db_path, dimension=768)
    if not os.path.exists(db_path):
        db.save_to_file()
    return db


def translate_to_english(text):
    """将中文文本翻译为英文"""
    translation = translator.translate(text, src='zh-CN', dest='en')
    return translation[0].text


def get_image_vector(image_path):
    """获取图片的向量表示"""
    image = Image.open(image_path)
    inputs = processor(text=["dummy"], images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    return outputs.image_embeds.squeeze().cpu().detach().numpy()


def get_text_vector(text_description: list[str]):
    """获取文本描述的向量表示"""
    dummy_image = torch.zeros(1, 3, 224, 224)
    inputs = processor(text=text_description, images=dummy_image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    return outputs.text_embeds.squeeze().cpu().detach().numpy()


def save_image_vectors(db: VectorDatabase, directory_path: str):
    """保存图片目录中的所有图片向量到数据库"""
    for filename in os.listdir(directory_path):
        if filename.endswith((".jpg", ".png", ".jpeg", ".webp")):
            file_path = os.path.join(directory_path, filename)
            vector = get_image_vector(file_path)
            db.add_vector(vector, file_path)


def search_images_by_text(text_description: list[str], db):
    """根据文本描述检索数据库中的图片"""
    text_vector = get_text_vector(text_description)
    return db.search_vector(text_vector, k=len(db.file_paths))


if __name__ == '__main__':
    db = initialize_or_load_db(DB_PATH)
    save_image_vectors(db, DIRECTORY_PATH)

    topK = 2
    text_description = ["车辆"]
    translated_descriptions = translate_to_english(text_description)
    print(translated_descriptions)

    results = search_images_by_text(translated_descriptions, db)
    for path, score in results[:topK]:
        print(f"Image: {path}, Similarity: {score:.4f}")
