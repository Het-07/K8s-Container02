# Container - 02
from fastapi import FastAPI, HTTPException
import csv, os

app = FastAPI()
PERSISTENT_STORAGE_PATH = "/het_PV_dir"

@app.post("/compute")
def compute(data: dict):
    if "file" not in data or "product" not in data:
        return {"file": None, "error": "Invalid input"}

    file_path = os.path.join(PERSISTENT_STORAGE_PATH, data["file"])
    if not os.path.exists(file_path):
        return {"file": data["file"], "error": "File not found."}

    try:
        with open(file_path, "r") as f:
            reader = csv.DictReader(f)
            headers = [header.strip() for header in reader.fieldnames]

            if "product" not in headers or "amount" not in headers:
                return {"file": data["file"], "error": "Input file not in CSV format."}

            total = 0
            for row in reader:
                clean_row = {k.strip(): v.strip() for k, v in row.items()}
                if clean_row.get("product") == data["product"]:
                    try:
                        total += int(clean_row.get("amount", 0))
                    except ValueError:
                        continue

        return {"file": data["file"], "sum": total}

    except Exception as e:
        return {"file": data["file"], "error": "Input file not in CSV format."}

