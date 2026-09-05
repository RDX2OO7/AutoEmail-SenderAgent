import os
import sys

from create_sample_template import generate_sample_template
from clean_data import clean_student_data
from generate_certificates import generate_certificates
from send_emails import send_emails

def run_pipeline():
    print("=" * 60)
    print("       CERTIFICATE AUTOMATION PIPELINE RUNNER       ")
    print("=" * 60)

    # 0. Ensure template.pdf exists
    if not os.path.exists("template.pdf"):
        print("[INFO] template.pdf not found. Generating sample template...")
        generate_sample_template("template.pdf")

    # Step 1: Clean Data
    print("\n---> STEP 1: Data Cleaning (clean_data.py)")
    clean_success = clean_student_data("students.csv", "students_clean.csv")
    if not clean_success:
        print("[ABORT] Pipeline stopped due to data cleaning error.")
        sys.exit(1)

    # Step 2: Generate Certificates
    print("\n---> STEP 2: Certificate Generation (generate_certificates.py)")
    gen_success = generate_certificates("students_clean.csv", "template.pdf", "output")
    if not gen_success:
        print("[ABORT] Pipeline stopped due to certificate generation error.")
        sys.exit(1)

    # Step 3: Send Emails
    print("\n---> STEP 3: Email Dispatch (send_emails.py)")
    send_emails("students_clean.csv", "output")

    print("\n" + "=" * 60)
    print(" Pipeline execution completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()
