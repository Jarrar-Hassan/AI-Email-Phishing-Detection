**AI Email Phishing Detector**



An AI-powered desktop application built using Python, Tkinter, and Machine Learning to automatically detect phishing emails from a Gmail inbox. The application connects to your Gmail account via IMAP, fetches new emails, analyzes their content, and classifies them as Safe or Phishing in real time.



**Features**



* Connects to Gmail using IMAP securely with an App Password.
* Fetches emails in real time and updates every 15 seconds.
* Analyzes both subject line and body text for phishing indicators.
* Machine Learning model (trained with TF-IDF and a classifier) for accurate predictions.
* Simple, clean, and responsive Tkinter-based GUI.
* Color-coded results:
* Green = Safe Email
* Red = Phishing Email
* Orange = Error or Connection Issue



**Requirements**



* Python: 3.8 or later
* Gmail account with IMAP enabled
* Google App Password (instead of main password for security)
* Pre-trained model files:
* models/phishing\_model.pkl
* models/tfidf\_vectorizer.pkl



**Installation**



1. Clone the Repository

   git clone https://github.com/Jarrar-Hassan/AI-Email-Phishing-Detector.git
   cd AI-Email-Phishing-Detector
   
2. Create a Virtual Environment


   python -m venv phishing-env



**Activate the environment:**



On Windows:

* phishing-env\\Scripts\\activate
* 



On Linux/Mac:

* source phishing-env/bin/activate

* Install Dependencies
  pip install -r requirements.txt



**Gmail Setup (IMAP \& App Password)**



* Log in to your Google Account.
* Enable IMAP:
* Go to Gmail Settings > Forwarding and POP/IMAP > Enable IMAP.
* Generate an App Password:
* Go to Google Account > Security > App Passwords.
* Select Mail as the app and your device type.
* Copy the generated 16-character password.



**Configuration**



* Open main.py and update these lines with your Gmail credentials:
* EMAIL\_ACCOUNT = "your-email@gmail.com"
  EMAIL\_PASSWORD = "your-app-password"
* Run the Application
* Start the app by running:
* python main.py



The GUI will open and begin fetching your emails in real time. The list updates automatically every 15 seconds.



**Working:**



* The app connects to Gmail using IMAP.
* Fetches emails received after the application started.
* Cleans and preprocesses the subject and body text.
* Converts the text into TF-IDF features.
* Uses the Machine Learning model to predict if the email is Phishing or Safe.
* Displays the results in a color-coded Treeview table.





**Project Structure**


AI-Email-Phishing-Detector/
│
├── main.py                 # Main application script
├── models/
│   ├── phishing\_model.pkl  # Trained ML model
│   └── tfidf\_vectorizer.pkl # TF-IDF vectorizer
├── requirements.txt         # Project dependencies
└── README.md                # Documentation



**Common Issues \& Fixes**



Invalid Credentials:

* Ensure you are using the App Password, not your main Gmail password.

IMAP Disabled:

* Enable IMAP in Gmail settings.

App Not Responding:

* The first fetch may take time depending on your inbox size. Wait a few seconds.





**Developed by Muhammad Jarrar Hassan**

