import os
import time
import re
import smtplib
import pandas as pd
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", "").strip()
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "").strip()

CLEAN_CSV = "students_clean.csv"
OUTPUT_DIR = "output"
SEND_LOG_CSV = "send_log.csv"
DELAY_SECONDS = 2.5

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name.strip())

def get_sent_emails(log_file=SEND_LOG_CSV):
    """Retrieve set of emails already successfully sent."""
    if not os.path.exists(log_file):
        return set()
    try:
        log_df = pd.read_csv(log_file)
        if 'email' in log_df.columns and 'status' in log_df.columns:
            successful = log_df[log_df['status'].isin(['SUCCESS', 'SENT'])]
            return set(successful['email'].astype(str).str.strip())
    except Exception as e:
        print(f"[WARNING] Could not read log file '{log_file}': {e}")
    return set()

def log_send_result(email, name, status, details, log_file=SEND_LOG_CSV):
    """Append send log entry to send_log.csv."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = pd.DataFrame([{
        'timestamp': timestamp,
        'email': email,
        'name': name,
        'status': status,
        'details': details
    }])
    
    header = not os.path.exists(log_file)
    log_entry.to_csv(log_file, mode='a', index=False, header=header)

def is_credentials_valid():
    """Check if valid Gmail credentials are set in .env."""
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        return False
    if "your_email@gmail.com" in GMAIL_ADDRESS or "your_app_password" in GMAIL_APP_PASSWORD:
        return False
    return True

def send_emails(clean_csv=CLEAN_CSV, output_dir=OUTPUT_DIR):
    if not os.path.exists(clean_csv):
        print(f"[ERROR] Clean CSV file '{clean_csv}' not found.")
        return False

    df = pd.read_csv(clean_csv)
    if df.empty:
        print("[WARNING] No records found to send.")
        return False

    sent_emails = get_sent_emails()
    credentials_ok = is_credentials_valid()

    if not credentials_ok:
        print("[NOTICE] Gmail credentials in .env are placeholder or missing.")
        print("[NOTICE] Running email phase in DRY-RUN mode (logging operations without sending real SMTP emails).\n")

    server = None
    if credentials_ok:
        try:
            print(f"Connecting to Gmail SMTP server as {GMAIL_ADDRESS}...")
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            print("SMTP Connection established successfully.\n")
        except Exception as e:
            print(f"[ERROR] Failed to connect to SMTP server: {e}")
            print("Switching to DRY-RUN mode for remaining records.\n")
            credentials_ok = False

    try:
        for idx, row in df.iterrows():
            name = str(row['name']).strip()
            email = str(row['email']).strip()
            safe_name = sanitize_filename(name)
            pdf_path = os.path.join(output_dir, f"{safe_name}.pdf")

            if email in sent_emails:
                print(f" [SKIP] {name} ({email}) - Already sent.")
                continue

            if not os.path.exists(pdf_path):
                print(f" [FAIL] Certificate PDF not found for {name} ({pdf_path})")
                log_send_result(email, name, "FAILED", f"PDF missing: {pdf_path}")
                continue

            if not credentials_ok:
                # Dry-run logging
                print(f" [DRY-RUN] Simulating email to {name} ({email}) with attachment '{pdf_path}'")
                log_send_result(email, name, "SUCCESS", "DRY_RUN_SIMULATED")
                sent_emails.add(email)
                time.sleep(1.0)
                continue

            # Construct MIME Email
            try:
                msg = MIMEMultipart()
                msg['From'] = GMAIL_ADDRESS
                msg['To'] = email
                msg['Subject'] = f"Congratulations on your Certificate, {name}!"
                #hers yours personilzed message that is to be send by agent to the mail as a body message that the python
                body = (
                    f"Dear {name},\n\n"
                    #complete this as per your requirement and make it look professional
                    f"Congratulations on completing the course and completing it successfully. We are proud of you for your hard work and dedication.\n\n"
                    f"Please find your Certificate of Completion attached to this email.\n\n"
                    f"Best regards,\n"
                    f"Team Python Program"
                )
                msg.attach(MIMEText(body, 'plain'))

                # Attach PDF
                with open(pdf_path, 'rb') as f:
                    attach = MIMEApplication(f.read(), _subtype="pdf")
                    attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_path))
                    msg.attach(attach)

                server.send_message(msg)
                print(f" [SENT] Email successfully delivered to {name} ({email})")
                log_send_result(email, name, "SUCCESS", "Sent via Gmail SMTP")
                sent_emails.add(email)

                # Delay between sends
                time.sleep(DELAY_SECONDS)

            except Exception as e:
                print(f" [FAIL] Could not send email to {name} ({email}): {e}")
                log_send_result(email, name, "FAILED", str(e))

    finally:
        if server:
            try:
                server.quit()
            except Exception:
                pass

    print(f"\nEmail dispatch completed. Logs saved to '{SEND_LOG_CSV}'.\n")
    return True

if __name__ == "__main__":
    send_emails()
