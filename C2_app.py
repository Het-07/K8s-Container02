from fastapi import FastAPI
import csv
import os

app = FastAPI()
PERSISTENT_STORAGE_PATH = "/het_PV_dir"

@app.post("/compute")
def compute(data: dict):
    if "file" not in data or not data["file"] or "product" not in data or not data["product"]:
        return {"file": None, "error": "Invalid JSON input."}

    file_path = os.path.join(PERSISTENT_STORAGE_PATH, data["file"])
    if not os.path.exists(file_path):
        return {"file": data["file"], "error": "File not found."}

    try:
        with open(file_path, "r") as f:
            reader = csv.DictReader(f)
            headers = [h.strip().lower() for h in reader.fieldnames]
            if "product" not in headers or "amount" not in headers:
                return {"file": data["file"], "error": "Input file not in CSV format."}

            total = 0
            for row in reader:
                product = row.get("product") or row.get(" product") or ""
                amount = row.get("amount") or row.get(" amount") or ""
                product = product.strip()
                amount = amount.strip()
                if product == data["product"] and amount.isdigit():
                    total += int(amount)


            return {"file": data["file"], "sum": total}

    except Exception:
        return {"file": data["file"], "error": "Input file not in CSV format."}
