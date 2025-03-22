from fastapi import FastAPI
import csv
import os

app = FastAPI()
PERSISTENT_STORAGE_PATH = "/het_PV_dir"

@app.post("/compute")
def compute(data: dict):
    filename = data.get("file")
    product = data.get("product")

    if not filename or not product:
        return {"file": None, "error": "Invalid JSON input."}

    file_path = os.path.join(PERSISTENT_STORAGE_PATH, filename)

    if not os.path.exists(file_path):
        return {"file": filename, "error": "File not found."}

    try:
        with open(file_path, "r") as f:
            reader = csv.DictReader(f)
            headers = [h.strip().lower() for h in reader.fieldnames or []]

            if "product" not in headers or "amount" not in headers:
                return {"file": filename, "error": "Input file not in CSV format."}

            total = 0
            for row in reader:
                prod = row.get("product", "").strip()
                amt = row.get("amount", "").strip()
                if prod == product and amt.isdigit():
                    total += int(amt)

        return {"file": filename, "sum": total}

    except csv.Error:
        return {"file": filename, "error": "Input file not in CSV format."}
    except:
        return {"file": filename, "error": "Input file not in CSV format."}
