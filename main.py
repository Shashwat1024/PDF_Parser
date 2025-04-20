from PyPDF2 import PdfReader
import re
import pandas as pd


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


pdf_text = extract_text_from_pdf("data/Statement_1745166559020.pdf")

# cleaning up the text by joining broken lines
cleaned_text = re.sub(r'(\n)(?=\d{2}-\d{2}-\d{4})', ' ', pdf_text)  # Join date lines
cleaned_text = re.sub(r'(\n)(?=UPI/)', ' ', cleaned_text)  # Join UPI lines
cleaned_text = re.sub(r'(\n)(?=[A-Z]{2,})', ' ', cleaned_text)  # Join BANK lines
cleaned_text = re.sub(r'(\n)(?=\d)', ' ', cleaned_text)  # Join amount lines

pattern = r'(\d{2}-\d{2}-\d{4})\s+(UPI/.+?)\s+(\d+\.\d{2})(DR|CR)'
transactions = re.findall(pattern, cleaned_text)

if not transactions:
    print("No transactions found. Check the text format:")
    print(cleaned_text[:1000])
else:
    df = pd.DataFrame(transactions, columns=["Date", "Description", "Amount", "Type"])

    # Clean description further
    df['Description'] = df['Description'].str.replace(r'\s+', ' ', regex=True).str.strip()

    # Convert date format
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')

    # Save to CSV
    df.to_csv('bank_statement.csv', index=False)
    print(f"Success! Saved {len(df)} transactions to 'bank_statement.csv'")