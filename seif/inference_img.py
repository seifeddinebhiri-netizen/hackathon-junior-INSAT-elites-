# inference_image.py
import torch, numpy as np
from torchvision import transforms, models
from PIL import Image
import torch.nn as nn

def get_image_model(num_classes=9, pretrained=False, dropout=0.3):
    model = models.resnet50(pretrained=pretrained)
    in_feat = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(dropout),
        nn.Linear(in_feat, 512),
        nn.ReLU(),
        nn.Dropout(0.2),
        nn.Linear(512, num_classes)
    )
    return model

val_tfms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225]),
])

device = 'cuda' if torch.cuda.is_available() else 'cpu'
num_classes = 9
model = get_image_model(num_classes=num_classes, pretrained=False)
state = torch.load("best_image_model.pth", map_location=device)
model.load_state_dict(state)
model.to(device)
model.eval()

label_map = {0:"angry", 1:"disgust", 2:"fear", 3:"happy", 4:"sad", 5:"surprise", 6:"neutral", 7:"drunk", 8:"sleepy" }

def predict_image(image_path):
    img = Image.open(image_path).convert('RGB')
    x = val_tfms(img).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(x)
        probs = torch.softmax(logits, dim=1).cpu().numpy()[0]
    return probs

if __name__ == "__main__":
    test_image = "fer_images/sleepy2.png"  # <- change to your image filename
    probs = predict_image(test_image)
    for i,p in enumerate(probs):
        print(f"{label_map[i]}: {p:.4f}")
    pred = int(np.argmax(probs))
    print("Predicted:", label_map[pred], "confidence:", float(probs[pred]))
