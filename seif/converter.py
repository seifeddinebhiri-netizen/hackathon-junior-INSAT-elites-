import os
import pandas as pd
import numpy as np
from PIL import Image

df = pd.read_csv("fer2013.csv")

# Create folders
root = "fer_images"
os.makedirs(root, exist_ok=True)

emotion_map = {
    0: "angry",
    1: "disgust",
    2: "fear",
    3: "happy",
    4: "sad",
    5: "surprise",
    6: "neutral"
}

for emotion in emotion_map.values():
    os.makedirs(os.path.join(root, emotion), exist_ok=True)

# Convert each row into an image
for i, row in df.iterrows():
    pixels = np.array(row["pixels"].split(), dtype="uint8")
    img = pixels.reshape(48,48)  # grayscale
    
    # convert to PIL Image
    img = Image.fromarray(img)

    label = emotion_map[row["emotion"]]
    img.save(os.path.join(root, label, f"{i}.png"))

print("Conversion complete!")
