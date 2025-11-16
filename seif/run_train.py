import pandas as pd
from image_pipeline import train_image

if __name__ == "__main__":
    df = pd.read_csv("labels.csv")
    model = train_image(
        df,
        img_dir="fer_images",
        num_classes=5,
        batch_size=16,
        epochs=8,
        lr=1e-4
    )

