"""
download_dataset.py
Downloads the Kaggle chest X-ray pneumonia dataset via kagglehub
and prints the local path for use by the training script.

Usage:
    python download_dataset.py

Output:
    Writes the dataset path to  dataset_path.txt  so the training script
    can pick it up without re-downloading.

Prerequisites:
    - kagglehub installed  (pip install kagglehub)
    - Kaggle API credentials configured:
        ~/.kaggle/kaggle.json   OR   env vars KAGGLE_USERNAME / KAGGLE_KEY
"""

import os
import sys

print("=" * 50)
print("Dataset downloader — chest-xray-pneumonia")
print("=" * 50)

try:
    import kagglehub
except ImportError:
    print("[FAIL] kagglehub is not installed. Run: pip install kagglehub")
    sys.exit(1)

DATASET = "paultimothymooney/chest-xray-pneumonia"
PATH_FILE = "dataset_path.txt"

print(f"Downloading dataset: {DATASET}")
print("This may take a few minutes on first run (cached afterwards)...")

try:
    path = kagglehub.dataset_download(DATASET)
except Exception as e:
    print(f"[FAIL] Download failed: {e}")
    sys.exit(1)

data_dir = os.path.join(path, "chest_xray")

# Sanity-check expected splits
for split in ("train", "val", "test"):
    split_path = os.path.join(data_dir, split)
    if os.path.isdir(split_path):
        classes = [d for d in os.listdir(split_path) if os.path.isdir(os.path.join(split_path, d))]
        print(f"  [{split:5s}] {split_path}  —  classes: {classes}")
    else:
        print(f"  [WARN] Expected split not found: {split_path}")

# Persist path for the training script
with open(PATH_FILE, "w") as f:
    f.write(path)

print(f"\nDataset root  : {path}")
print(f"Data dir      : {data_dir}")
print(f"Path written to: {PATH_FILE}")
print("=" * 50)
print("Download complete.")
