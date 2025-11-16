# image_pipeline.py
import os, random
import pandas as pd
from PIL import Image
import torch
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from torchvision.models import resnet50, ResNet50_Weights
from sklearn.model_selection import train_test_split
from tqdm import tqdm
# ----- 1) Example DataFrame format -----
# csv columns: filename,label
# label mapping: neutral=0,happy=1,sad=2,angry=3,sleepy=4,drunk=5
# df = pd.read_csv("labels.csv")

# ----- 2) Dataset -----
class DriverImageDataset(Dataset):
    def __init__(self, df, img_dir, transform=None):
        self.df = df.reset_index(drop=True)
        self.img_dir = img_dir
        self.transform = transform

    def __len__(self): return len(self.df)
    def __getitem__(self, idx):
        row = self.df.loc[idx]
        img_path = os.path.join(self.img_dir, row['filename'])
        try:
            img = Image.open(img_path).convert('RGB')
        except Exception as e:
            print(f"CORRUPTED IMAGE: {img_path}")
            # return a black image instead of crashing/freezing
            img = Image.new("RGB", (224,224))
        img = Image.open(img_path).convert('RGB')
        if self.transform: img = self.transform(img)
        label = int(row['label'])
        return img, label

# ----- 3) Transforms -----
train_tfms = transforms.Compose([
    transforms.Resize(256),
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(0.15,0.15,0.15,0.05),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225]),
])
val_tfms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225]),
])

# ----- 4) Build DataFrames & DataLoaders -----
def make_dataloaders(df, img_dir, batch_size=32, val_size=0.2, seed=42):
    print("DEBUG: building dataloaders...")
    train_df, val_df = train_test_split(df, test_size=val_size, stratify=df['label'], random_state=seed)
    train_ds = DriverImageDataset(train_df, img_dir, transform=train_tfms)
    val_ds = DriverImageDataset(val_df, img_dir, transform=val_tfms)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=0)
    print("DEBUG: train_loader size =", len(train_loader))
    print("DEBUG: val_loader size =", len(val_loader))
    return train_loader, val_loader





# ----- 5) Model (ResNet50 finetune) -----

def get_image_model(num_classes=5, pretrained=True, dropout=0.3):
    weights = ResNet50_Weights.IMAGENET1K_V1 if pretrained else None
    model = resnet50(weights=weights)

    in_feat = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(dropout),
        nn.Linear(in_feat, 512),
        nn.ReLU(),
        nn.Dropout(0.2),
        nn.Linear(512, num_classes)
    )
    return model

# ----- 6) Training & evaluation helpers -----
def train_one_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0
    total_correct = 0
    total_samples = 0

    print(" train_one_epoch started")   # DEBUG

    for batch_idx, (images, labels) in enumerate(loader):
        if batch_idx == 0:
            print(" First batch loaded")  # DEBUG
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * images.size(0)
        total_correct += (outputs.argmax(1) == labels).sum().item()
        total_samples += labels.size(0)

        if batch_idx % 10 == 0:
            print("Batch", batch_idx)  # DEBUG

    print(" train_one_epoch finished")   # DEBUG
    return total_loss / total_samples, total_correct / total_samples

def eval_model(model, loader, criterion, device):
    model.eval(); running_loss = 0.0; correct=0; total=0
    with torch.no_grad():
        for x,y in loader:
            x,y = x.to(device), y.to(device)
            logits = model(x); loss = criterion(logits,y)
            running_loss += loss.item()*x.size(0)
            preds = logits.argmax(dim=1)
            correct += (preds==y).sum().item(); total += x.size(0)
    return running_loss/total, correct/total

# ----- 7) Full train function -----
def train_image(df, img_dir, num_classes=5, batch_size=32, epochs=8, lr=1e-4, device=None):
    print("DEBUG: train_image() STARTED, device =", device)
    if device is None: device = 'cuda' if torch.cuda.is_available() else 'cpu'
    train_loader, val_loader = make_dataloaders(df, img_dir, batch_size=batch_size)
    model = get_image_model(num_classes=num_classes).to(device)
    optimizer = optim.AdamW(model.parameters(), lr=lr)
    # optional: compute class weights if imbalanced
    # weights = torch.tensor([...], device=device)
    criterion = nn.CrossEntropyLoss()  # or nn.CrossEntropyLoss(weight=weights)
    scaler = torch.cuda.amp.GradScaler() if device.startswith('cuda') else None

    best_val_acc = 0.0
    print("Starting training...")
    for epoch in range(1, epochs+1):
        train_loss, train_acc = train_one_epoch(model, train_loader, optimizer, criterion, device)
        val_loss, val_acc = eval_model(model, val_loader, criterion, device)
        print(f"Epoch {epoch}: train_loss={train_loss:.4f} train_acc={train_acc:.4f} val_acc={val_acc:.4f}")
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), "best_image_model.pth")
    print("Best val acc:", best_val_acc)
    return model

