import re
import pandas as pd
import os

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

def clean_student_data(input_csv="students.csv", output_csv="students_clean.csv"):
    if not os.path.exists(input_csv):
        print(f"[ERROR] Input file '{input_csv}' not found.")
        return False

    print(f"Reading '{input_csv}'...")
    df = pd.read_csv(input_csv)
    initial_count = len(df)

    # Check for required columns
    required_cols = ['name', 'email']
    missing_req = [col for col in required_cols if col not in df.columns]
    if missing_req:
        print(f"[ERROR] Missing required columns in CSV: {missing_req}")
        return False

    # Strip whitespace for string columns
    for col in df.select_dtypes(include=['object', 'string']).columns:
        df[col] = df[col].astype(str).str.strip()

    dropped_records = []
    valid_rows = []

    for idx, row in df.iterrows():
        name = row['name']
        email = row['email']

        # Check for missing/empty values (pd.isna or string 'nan' or empty)
        if pd.isna(name) or name.lower() == 'nan' or not name:
            dropped_records.append({'index': idx + 2, 'name': name, 'email': email, 'reason': 'Missing name'})
            continue

        if pd.isna(email) or email.lower() == 'nan' or not email:
            dropped_records.append({'index': idx + 2, 'name': name, 'email': email, 'reason': 'Missing email'})
            continue

        # Validate email regex
        if not re.match(EMAIL_REGEX, email):
            dropped_records.append({'index': idx + 2, 'name': name, 'email': email, 'reason': f"Invalid email format ('{email}')"})
            continue

        valid_rows.append(row)

    if valid_rows:
        clean_df = pd.DataFrame(valid_rows)
    else:
        clean_df = pd.DataFrame(columns=df.columns)

    clean_df.to_csv(output_csv, index=False)

    print("\n--- Data Cleaning Summary ---")
    print(f"Total Rows Processed: {initial_count}")
    print(f"Valid Rows Retained : {len(clean_df)}")
    print(f"Rows Dropped        : {len(dropped_records)}")
    
    if dropped_records:
        print("\nDropped Records Log:")
        for record in dropped_records:
            print(f" - CSV Line {record['index']}: Reason: {record['reason']} (Name: '{record['name']}', Email: '{record['email']}')")
    
    print(f"Cleaned dataset saved to '{output_csv}'.\n")
    return True

if __name__ == "__main__":
    clean_student_data()
