# 🚨 AI Email Phishing Detector


An **AI-powered desktop application** built with **Python**, **Tkinter**, and **Machine Learning** to detect phishing emails automatically from your Gmail inbox. The app fetches new emails in real-time, analyzes them, and classifies them as **Safe** or **Phishing**.

---

## ✨ Features

* Securely connects to Gmail using **IMAP** with an **App Password**
* Fetches emails in **real-time** and updates every **15 seconds**
* Analyzes both **subject** and **body text** for phishing indicators
* Uses a **Machine Learning model** (TF-IDF + Classifier) for predictions
* Simple, clean, and **responsive Tkinter GUI**
* **Color-coded results**:

  * 🟢 **Green** = Safe
  * 🔴 **Red** = Phishing
  * 🟠 **Orange** = Error or Connection Issue

---

## 🛠 Requirements

* Python 3.8 or later
* Gmail account with **IMAP enabled**
* Google **App Password**
* Pre-trained model files:

  * `models/phishing_model.pkl`
  * `models/tfidf_vectorizer.pkl`

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Jarrar-Hassan/AI-Email-Phishing-Detector.git
cd AI-Email-Phishing-Detector
```

### 2. Create a Virtual Environment

```bash
python -m venv phishing-env
```

### 3. Activate the Environment

**Windows:**

```bash
phishing-env\Scripts\activate
```

**Linux/Mac:**

```bash
source phishing-env/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📧 Gmail Setup (IMAP & App Password)

1. **Enable IMAP**: Gmail → Settings → Forwarding and POP/IMAP → Enable IMAP
2. **Generate an App Password**: Google Account → Security → App Passwords → Select "Mail" → Copy 16-character password
3. **Update Credentials** in `main.py`:

```python
EMAIL_ACCOUNT = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"
```

---

## ▶️ Run the Application

```bash
python main.py
```

The GUI will open and start fetching emails **received after the app started**, updating every **15 seconds**.

---

## 🧐 How It Works

1. Connects to Gmail via IMAP
2. Fetches **emails received after app startup**
3. Cleans and preprocesses text (subject + body)
4. Converts text into **TF-IDF features**
5. ML model predicts:

   * 🔴 Phishing
   * 🟢 Safe
6. Displays results in a **color-coded table** in the GUI

---

## 📁 Project Structure

```
AI-Email-Phishing-Detector/
│
├── main.py                     # Main application script
├── models/
│   ├── phishing_model.pkl      # Trained ML model
│   └── tfidf_vectorizer.pkl    # TF-IDF vectorizer
├── requirements.txt            # Project dependencies
└── README.md                   # Documentation
```

---

## ⚠️ Common Issues & Fixes

* **Invalid Credentials**: Use App Password, not Gmail password
* **IMAP Disabled**: Enable IMAP in Gmail settings
* **App Freezes / Unresponsive**: First fetch may take time if inbox is large

---

## 👨‍💻 Developed by

**Muhammad Jarrar Hassan**
(https://github.com/Jarrar-Hassan)
