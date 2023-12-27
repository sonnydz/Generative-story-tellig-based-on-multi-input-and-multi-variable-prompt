import gradio as gr
import torch
from torchvision import models, transforms
from PIL import Image
from transformers import pipeline
import traceback
import requests

# Load the pre-trained MobileNetV2 model
model = models.mobilenet_v2(pretrained=True)
model.eval()

# Define a transform to preprocess the image
preprocess = transforms.Compose([
    transforms.Resize(128),  # Reduced size
    transforms.CenterCrop(128),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def imgToClassification(image):
    try:
        input_image = Image.fromarray(image.astype('uint8'), 'RGB')
        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0)
        with torch.no_grad():
            output = model(input_batch)
        labels_url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
        labels = requests.get(labels_url).json()
        _, predicted_idx = torch.max(output, 1)
        label = labels[predicted_idx.item()]
        return label
    except Exception as e:
        print(f"Error in imgToClassification: {e}")
        traceback.print_exc()
        return "No label detected"

def generate_story_with_gpt_neo(label):
    try:
        generator = pipeline("text-generation", model="gpt2")  # Switched to GPT-2
        prompt = f"In a scene with a {label}, "
        story = generator(prompt, max_length=50, clean_up_tokenization_spaces=True)[0]['generated_text']
        return story
    except Exception as e:
        print(f"Error in generate_story_with_gpt_neo: {e}")
        return "Error in generating story"

def auto_caption_and_story(uploaded_image):
    label = imgToClassification(uploaded_image)
    auto_story = generate_story_with_gpt_neo(label)
    return label, auto_story

def user_caption_and_story(user_caption):
    user_story = generate_story_with_gpt_neo(user_caption)
    return user_caption, user_story
def chatgpt_story(image):
    # Manually crafted story (as if from a paid model, ChatGPT-4)
    caption = "A genocide , children crying ,war crime ."
    story = ("Once upon a time, in a world gripped by the shadows of despair,a little child cried out amidst the ruins of a once-thriving city. The air was heavy with the aftermath of destruction, and the echoes of genocide and war crimes stained the landscape. The child, innocent and unaware of the grim reality surrounding them, stood alone in the midst of chaos. Tears rolled down their cheeks, reflecting the pain and loss that had befallen the world. The once-vibrant city, now reduced to rubble, bore the scars of a conflict that had torn apart the very fabric of society. The reasons behind such devastation were complex and rooted in the darker aspects of human nature.")
    return caption, story



