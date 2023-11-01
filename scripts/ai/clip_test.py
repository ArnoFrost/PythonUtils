import os
import pickle

from PIL import Image
from googletrans import Translator
from sklearn.metrics.pairwise import cosine_similarity
from transformers import CLIPProcessor, CLIPModel

# 初始化模型处理器
model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
translator = Translator()


def translate_to_english(text):
    translation = translator.translate(text, src='zh-CN', dest='en')
    return translation.text


def get_image_vector(image_path):
    image = Image.open(image_path)
    inputs = processor(text=[], images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    return outputs.image_embeds.squeeze().cpu().detach().numpy()


def get_text_vector(text_description):
    inputs = processor(text=text_description, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    return outputs.text_embeds.squeeze().cpu().detach().numpy()


def save_image_vectors(directory_path, save_path):
    image_vectors = {}

    # 遍历指定目录下的所有图片
    for filename in os.listdir(directory_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):  # 可以根据需要添加更多图片格式
            file_path = os.path.join(directory_path, filename)
            vector = get_image_vector(file_path)
            image_vectors[file_path] = vector.cpu().detach().numpy()

    # 保存为pickle文件
    with open(save_path, 'wb') as handle:
        pickle.dump(image_vectors, handle, protocol=pickle.HIGHEST_PROTOCOL)


def search_images_by_text(text_description: list, vectors_path: str):
    # 加载保存的向量数据
    with open(vectors_path, 'rb') as handle:
        saved_vectors = pickle.load(handle)

    # 计算给定文本描述的向量
    text_vector = get_text_vector(text_description)

    # 计算相似度
    similarities = {}
    for image_path, image_vector in saved_vectors.items():
        similarity = cosine_similarity([text_vector], [image_vector])[0][0]
        similarities[image_path] = similarity

    # 根据相似度排序
    sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

    return sorted_similarities


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


if __name__ == '__main__':
    # 定义目录:
    directory_path = "/Users/xuxin14/Documents/Backup/头像/训练"
    vectors_path = "/Users/xuxin14/Documents/Backup/头像/训练/vectors.pkl"
    # 保存向量
    save_image_vectors(directory_path, vectors_path)

    # 搜索图片：
    text_description = ["a photo of a cat"]
    results = search_images_by_text(text_description, vectors_path)

    # 打印最相似的5个图片
    for path, score in results[:5]:
        print(f"Image: {path}, Similarity: {score:.4f}")
