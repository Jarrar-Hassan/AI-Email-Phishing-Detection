import imaplib
import email
from email.header import decode_header
import tkinter as tk
from tkinter import ttk, messagebox
import joblib
import re
import threading
from datetime import datetime, timezone
import email.utils

# ----------------------------
# Load Model and Vectorizer
# ----------------------------
# Ensure your model and vectorizer files are in a 'models' subfolder
# or update the path accordingly.
try:
    model = joblib.load("models/phishing_model.pkl")
    vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
except FileNotFoundError:
    # Handle error if model files are not found.
    # This requires creating a simple Tkinter window to show the error,
    # as the main app window might not be initialized yet.
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("Error", "Model or vectorizer file not found.\nPlease make sure 'phishing_model.pkl' and 'tfidf_vectorizer.pkl' are in the 'models' folder.")
    exit()

# ----------------------------
# Email Cleaning Function
# ----------------------------
def clean_text(text):
    """
    Cleans email text by converting to lowercase, removing URLs,
    and stripping non-alphabetic characters.
    """
    if text is None:
        return ""
    text = text.lower()
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"[^a-z\s]", "", text)  # Keep only letters and spaces
    return text

# ----------------------------
# IMAP Configuration
# ----------------------------
# IMPORTANT: Use a Gmail "App Password" for security, not your main password.
IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "123@gmail.com"
EMAIL_PASSWORD = "" # place the app password here

# Global variable to store the time the application started.
# We will only fetch emails that arrived after this time.
app_start_time = datetime.now(timezone.utc)

def fetch_emails():
    """
    Connects to the IMAP server and fetches all emails that have
    arrived since the application was started.
    """
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")

        # Format the date for the IMAP SINCE query (e.g., "01-Jan-2023")
        search_date = app_start_time.strftime("%d-%b-%Y")
        
        # Search for all emails SINCE the app started.
        status, messages = mail.search(None, f'(SINCE "{search_date}")')
        if status != 'OK':
            return [{"from": "Error", "subject": "Failed to search inbox.", "prediction": "Error"}]

        email_ids = messages[0].split()
        emails_data = []

        for e_id in email_ids:
            status, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    # Get email date and ensure it's timezone-aware
                    email_date_str = msg.get("Date")
                    if not email_date_str:
                        continue
                    
                    parsed_date = email.utils.parsedate_to_datetime(email_date_str)
                    if parsed_date.tzinfo is None:
                        parsed_date = parsed_date.replace(tzinfo=timezone.utc)

                    # Final check: only process emails received after the app officially started
                    if parsed_date < app_start_time:
                        continue

                    # Decode subject and sender information
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")

                    from_, encoding = decode_header(msg.get("From", ""))[0]
                    if isinstance(from_, bytes):
                        from_ = from_.decode(encoding if encoding else "utf-8", errors="ignore")

                    # Extract the email body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition")):
                                payload = part.get_payload(decode=True)
                                charset = part.get_content_charset() or 'utf-8'
                                body += payload.decode(charset, errors="ignore")
                    else:
                        payload = msg.get_payload(decode=True)
                        charset = msg.get_content_charset() or 'utf-8'
                        body = payload.decode(charset, errors="ignore")
                    
                    # Predict using the loaded model
                    text_to_analyze = subject + " " + body
                    cleaned_text = clean_text(text_to_analyze)
                    features = vectorizer.transform([cleaned_text])
                    prediction = model.predict(features)[0]

                    emails_data.append({
                        "from": from_,
                        "subject": subject,
                        "prediction": "Phishing" if prediction == 1 else "Safe"
                    })

        mail.logout()
        # Return emails in reverse chronological order (newest first)
        return emails_data[::-1]

    except Exception as e:
        return [{"from": "Error", "subject": str(e), "prediction": "Connection Error"}]


# ----------------------------
# GUI Application
# ----------------------------
class EmailCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Email Phishing Detector")
        self.root.geometry("850x500")
        self.root.config(bg="#f0f0f0")

        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Treeview for displaying emails ---
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#ffffff", foreground="#333333", rowheight=25, fieldbackground="#ffffff", borderwidth=0)
        style.configure("Treeview.Heading", background="#e0e0e0", font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#347083')])

        self.tree = ttk.Treeview(main_frame, columns=("From", "Subject", "Status"), show="headings")
        self.tree.heading("From", text="From")
        self.tree.heading("Subject", text="Email Subject")
        self.tree.heading("Status", text="Prediction")

        self.tree.column("From", width=220, anchor=tk.W)
        self.tree.column("Subject", width=450, anchor=tk.W)
        self.tree.column("Status", width=120, anchor=tk.CENTER)
        
        # --- Scrollbar ---
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Status Bar ---
        self.status_label = tk.Label(root, text="Initializing...", bd=1, relief=tk.SUNKEN, anchor=tk.W, padx=5, pady=2)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Start the automatic refresh loop
        self.auto_refresh()

    def populate_tree(self, emails):
        """Clears and repopulates the treeview with fetched emails."""
        self.tree.delete(*self.tree.get_children())
        for email_data in emails:
            prediction = email_data.get("prediction", "N/A")
            tag = "safe"
            if prediction == "Phishing":
                tag = "phishing"
            elif "Error" in prediction:
                tag = "error"

            values = (
                email_data.get("from", "N/A"),
                email_data.get("subject", "N/A"),
                prediction
            )
            self.tree.insert("", tk.END, values=values, tags=(tag,))
        
        self.tree.tag_configure("phishing", foreground="#d90429", font=('Arial', 9, 'bold'))
        self.tree.tag_configure("safe", foreground="#008000")
        self.tree.tag_configure("error", foreground="#fca311")
        
        now = datetime.now().strftime('%H:%M:%S')
        self.status_label.config(text=f"Update complete. Displaying emails since app start. Last check: {now}")

    def update_emails_in_background(self):
        """Fetches emails in a separate thread to not freeze the GUI."""
        def task():
            self.root.after(0, lambda: self.status_label.config(text="Checking for new emails..."))
            emails = fetch_emails()
            # Schedule the GUI update on the main thread
            self.root.after(0, self.populate_tree, emails)
        
        threading.Thread(target=task, daemon=True).start()

    def auto_refresh(self):
        """Schedules the email check to run periodically."""
        self.update_emails_in_background()
        # Schedule the next refresh in 15 seconds (15000 milliseconds)
        self.root.after(15000, self.auto_refresh)

# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = EmailCheckerApp(root)
    root.mainloop()

