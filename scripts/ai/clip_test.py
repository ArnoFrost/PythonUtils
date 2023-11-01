from PIL import Image

from transformers import CLIPProcessor, CLIPModel

model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

if __name__ == '__main__':
    # url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    # image = Image.open(requests.get(url, stream=True).raw)
    # image_path = "/Users/xuxin14/Documents/Backup/头像/训练/girl.jpeg"
    image_path = "/Users/xuxin14/Documents/Backup/头像/训练/cat.jpeg"
    image = Image.open(image_path)

    descriptions = ["a photo of a boy", "a photo of a girl", "a photo of a person",
                    "a photo of a dog", "a photo of a cat", "a photo of a animal"]
    inputs = processor(text=descriptions, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)

    logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1)  # we can take the softmax to get the label probabilities
    probabilities = probs.detach().numpy()[0]  # 将tensor转换为numpy数组

    # 将文本描述和它们的概率值结合
    description_probs = list(zip(descriptions, probabilities))

    # 按概率值从高到低排序
    sorted_description_probs = sorted(description_probs, key=lambda x: x[1], reverse=True)

    for desc, prob in sorted_description_probs:
        print(f"{desc}: {prob:.4f}")
