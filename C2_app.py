# Container - 02
from fastapi import FastAPI, HTTPException
import csv, os

app = FastAPI()
PERSISTENT_STORAGE_PATH = "/het_PV_dir"

@app.post("/compute")
def compute(data: dict):
    if "file" not in data or "product" not in data:
        return {"file": None, "error": "Invalid JSON input."}

    file_path = os.path.join(PERSISTENT_STORAGE_PATH, data["file"])
    if not os.path.exists(file_path):
        return {"file": data["file"], "error": "File not found."}

    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            if not {"product", "amount"}.issubset(reader.fieldnames):
                return {"file": data["file"], "error": "Input file not in CSV format."}

            total = sum(int(row["amount"]) for row in reader if row["product"] == data["product"])
            return {"file": data["file"], "sum": total} 
    except:
        return {"file": data["file"], "error": "Input file not in CSV format."}

