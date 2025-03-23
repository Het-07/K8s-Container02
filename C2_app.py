# Container - 02

from fastapi import FastAPI
import csv
import os

app = FastAPI()
PERSISTENT_STORAGE_PATH = "/het_PV_dir"

# ----------------------------------------------------------
# Endpoint to compute sum of product amounts from CSV file.
# ----------------------------------------------------------
@app.post("/compute")
def compute(data: dict):
    filename = data.get("file")
    product = data.get("product")

    if not filename or not product:
        return {"file": None, "error": "Invalid JSON input."}

    file_path = os.path.join(PERSISTENT_STORAGE_PATH, filename)
    if not os.path.exists(file_path):
        return {"file": filename, "error": "File not found."}

    results = []
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            
            if not reader.fieldnames:
                return {"file": filename, "error": "Input file not in CSV format."}

            headers = [h.strip().lower() for h in reader.fieldnames]
            if "product" not in headers or "amount" not in headers:
                return {"file": filename, "error": "Input file not in CSV format."}

            for row in reader:
                cleaned_row = {k.strip().lower(): v.strip() for k, v in row.items()}
                if cleaned_row.get("product") == product:
                    try:
                        amount = int(cleaned_row.get("amount", ""))
                        results.append(amount)
                    except ValueError:
                        continue

        total = sum(results)
        return {"file": filename, "sum": total}

    except Exception:
        return {"file": filename, "error": "Input file not in CSV format."}
