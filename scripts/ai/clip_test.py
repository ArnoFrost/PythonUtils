from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from googletrans import Translator

model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
translator = Translator()


def translate_to_english(text):
    translation = translator.translate(text, src='zh-CN', dest='en')
    return translation.text


if __name__ == '__main__':
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
