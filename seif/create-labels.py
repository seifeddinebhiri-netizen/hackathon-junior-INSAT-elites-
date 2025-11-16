import os
import pandas as pd

# All class names must match the folder names exactly
label_map = {
    "angry": 0,
    "drunk": 1,
    "sad": 2,
    "neutral": 3,
    "drunk":   4,
    "sleepy": 5
}

def make_csv(img_root="fer_images", output_csv="labels.csv"):
    rows = []

    for class_name, label in label_map.items():
        folder = os.path.join(img_root, class_name)
        if not os.path.exists(folder):
            print(f"WARNING: folder '{folder}' not found, skipping")
            continue

        for fname in os.listdir(folder):
            if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                rows.append({
                    "filename": f"{class_name}/{fname}",
                    "label": label
                })

    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False)
    print(f"Saved CSV with {len(df)} rows to {output_csv}")

if __name__ == "__main__":
    make_csv()
