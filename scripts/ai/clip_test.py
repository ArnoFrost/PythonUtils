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


def translate_to_english(text):
    translation = translator.translate(text, src='zh-CN', dest='en')
    return translation.text


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


def save_image_vectors(directory_path: str):
    first_vector = True
    db = None

    for filename in os.listdir(directory_path):
        if filename.endswith((".jpg", ".png", ".jpeg", ".webp")):
            file_path = os.path.join(directory_path, filename)
            vector = get_image_vector(file_path)

            if first_vector:
                dimension = len(vector)
                db = VectorDatabase(dimension=dimension)
                first_vector = False

            db.add_vector(vector, file_path)

    return db


def search_images_by_text(text_description, db):
    text_vector = get_text_vector(text_description)
    return db.search_vector(text_vector, k=len(db.file_paths))


if __name__ == '__main__':
    directory_path = "/Users/xuxin14/Documents/Backup/头像/训练"
    db = save_image_vectors(directory_path)

    text_description = ["a photo of a road"]
    results = search_images_by_text(text_description, db)

    for path, score in results[:5]:
        print(f"Image: {path}, Similarity: {score:.4f}")


def demo1():
    image_path = "/Users/xuxin14/Documents/Backup/头像/训练/girl.jpeg"
    # image_path = "/Users/xuxin14/Documents/Backup/头像/训练/cat.jpeg"
    image = Image.open(image_path)

    descriptions = ["一只猫", "多只猫", "a photo of a boy", "a photo of a girl", "a photo of a dog",
                    "a photo of a person", "一个人的照片"]

    translated_descriptions = [translate_to_english(desc) if '一' in desc else desc for desc in
                               descriptions]  # 简单检查是否为中文

    inputs = processor(text=translated_descriptions, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)

    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)
    probabilities = probs.detach().numpy()[0]

    # 使用原始描述
    description_probs = list(zip(descriptions, probabilities))

    sorted_description_probs = sorted(description_probs, key=lambda x: x[1], reverse=True)

    for desc, prob in sorted_description_probs:
        print(f"{desc}: {prob:.4f}")
