import pandas as pd
import os
import re
import string

# ==============================
# CLEANING FUNCTION
# ==============================
def clean_text(text):
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", " ", text)  # remove punctuation
    text = re.sub(r"\d+", "", text)  # remove numbers
    text = re.sub(r"\s+", " ", text).strip()  # remove extra spaces
    return text

# ==============================
# LOAD RAW DATASET
# ==============================
raw_path = "dataset/raw/Phishing_email.csv"  # Change to your actual file
processed_path = "dataset/processed"
os.makedirs(processed_path, exist_ok=True)

print("[INFO] Loading raw dataset...")
df = pd.read_csv(raw_path)

print("[INFO] Original columns:", df.columns)

# ==============================
# VALIDATE & RENAME COLUMNS
# ==============================
if "text" not in df.columns and "email_text" in df.columns:
    df.rename(columns={"email_text": "text"}, inplace=True)

if "label" not in df.columns:
    raise ValueError("Dataset must contain a 'label' column.")

print("[INFO] Dataset shape:", df.shape)

# ==============================
# CLEAN EMAIL TEXT
# ==============================
print("[INFO] Cleaning email text...")
df['text'] = df['text'].astype(str).apply(clean_text)

# ==============================
# SAVE PROCESSED DATA
# ==============================
processed_file = os.path.join(processed_path, "processed_emails.csv")
df.to_csv(processed_file, index=False)

print(f"[INFO] Processed dataset saved at {processed_file}")
print("[INFO] Sample data after cleaning:")
print(df.head())
