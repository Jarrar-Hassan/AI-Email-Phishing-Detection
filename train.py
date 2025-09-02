import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE
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
# LOAD PROCESSED DATASET
# ==============================
print("[INFO] Loading dataset...")
processed_path = "dataset/processed/processed_emails.csv"

if not os.path.exists(processed_path):
    raise FileNotFoundError(f"{processed_path} not found! Run preprocess.py first.")

df = pd.read_csv(processed_path)
print("[INFO] Columns in dataset:", df.columns)

# ==============================
# VALIDATE COLUMNS
# ==============================
expected_columns = ['label', 'text']
if not all(col in df.columns for col in expected_columns):
    raise ValueError(f"Dataset must contain columns: {expected_columns}")

# ==============================
# CLEAN EMAIL TEXTS
# ==============================
print("[INFO] Cleaning email texts...")
df['clean_text'] = df['text'].astype(str).apply(clean_text)
print("[INFO] Dataset size after cleaning:", df.shape)

# ==============================
# CHECK LABEL BALANCE
# ==============================
print("[INFO] Label distribution BEFORE balancing:")
print(df['label'].value_counts())

if df['label'].nunique() < 2:
    raise ValueError("Dataset contains only one class. Please check your dataset or preprocessing steps.")

# ==============================
# SPLIT DATA
# ==============================
print("[INFO] Splitting dataset into train and test...")
X_train, X_test, y_train, y_test = train_test_split(df['clean_text'], df['label'], test_size=0.2, random_state=42, stratify=df['label'])

# ==============================
# TF-IDF VECTORIZATION
# ==============================
print("[INFO] Creating TF-IDF features...")
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ==============================
# HANDLE IMBALANCE WITH SMOTE
# ==============================
print("[INFO] Balancing classes using SMOTE...")
smote = SMOTE(random_state=42)
X_train_bal, y_train_bal = smote.fit_resample(X_train_vec, y_train)
print("[INFO] Class distribution AFTER SMOTE:")
print(pd.Series(y_train_bal).value_counts())

# ==============================
# TRAIN MODEL
# ==============================
print("[INFO] Training Logistic Regression model...")
model = LogisticRegression(max_iter=1000)
model.fit(X_train_bal, y_train_bal)

# ==============================
# EVALUATE MODEL
# ==============================
print("[INFO] Evaluating model...")
y_pred = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)
print(f"[INFO] Accuracy: {accuracy:.4f}")
print("[INFO] Classification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# ==============================
# SAVE MODEL & VECTORIZER
# ==============================
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/phishing_model.pkl")
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")
print("[INFO] Model and TF-IDF vectorizer saved in 'models' folder.")
