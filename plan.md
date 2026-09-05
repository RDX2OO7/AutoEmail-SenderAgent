# Certificate Automation - Plan

## Goal
Read student names/emails from a CSV (exported from Google Sheets), generate a
personalized certificate PDF for each student from a fixed template, and email
each certificate to the corresponding student.

## Tech stack
- Python 3.11+
- pandas (data cleaning)
- PyMuPDF (fitz) (PDF text overlay)
- smtplib + email.mime (sending, via Gmail App Password / SMTP)
- python-dotenv (store email credentials outside source code)

## Inputs
- `template.pdf` — certificate template with a placeholder name area
- `students.csv` — columns: name, email (may contain extra/dirty columns to ignore)
- `.env` — GMAIL_ADDRESS, GMAIL_APP_PASSWORD

## Steps
1. `clean_data.py` — load students.csv with pandas, drop rows missing name or
   email, strip whitespace, validate email format with regex, save cleaned
   data to students_clean.csv. Print a summary of how many rows were dropped
   and why.
2. `generate_certificates.py` — for each row in students_clean.csv, open
   template.pdf with PyMuPDF, insert the student's name at fixed coordinates
   (X, Y — to be tuned by visually checking one output), matching the
   template's script font as closely as possible, save to
   output/<name>.pdf. Skip and log any row that fails instead of crashing
   the whole batch.
3. `send_emails.py` — for each generated PDF, send via Gmail SMTP (smtplib,
   using .env credentials) with a short subject/body, attaching the
   matching PDF. Add a 2-3 second delay between sends. Log every send
   (success/fail + timestamp) to send_log.csv so it's resumable — a
   re-run should skip names already marked as sent.
4. `main.py` — runs the three steps in order with a single command.

## Constraints
- Do not hardcode credentials — always read from .env
- Do not overwrite template.pdf — always work on a copy in memory/output
- Must be resumable: if the script stops midway, re-running should not
  re-send emails already logged as successful
- No external paid APIs