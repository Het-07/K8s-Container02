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
        return {"file": data["file"], "error": "File not found"}

    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            if not {"product", "amount"}.issubset(reader.fieldnames):
                raise ValueError("CSV format invalid")
            total = sum(int(row["amount"]) for row in reader if row["product"] == data["product"])
        return {"file": data["file"], "sum": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
