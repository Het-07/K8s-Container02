from fastapi import FastAPI, HTTPException
import csv
import os

app = FastAPI()
PERSISTENT_STORAGE_PATH = "/het_PV_dir"

@app.post("/compute")
def compute(data: dict):
    """Computes the sum of a product's amount in the given file."""
    if "file" not in data or "product" not in data:
        return {"file": None, "error": "Invalid JSON input."}

    file_path = os.path.join(PERSISTENT_STORAGE_PATH, data["file"])

    if not os.path.exists(file_path):
        return {"file": data["file"], "error": "File not found."}

    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            expected_headers = {"product", "amount"}
            if not expected_headers.issubset(set(reader.fieldnames or [])):
                return {"file": data["file"], "error": "Invalid CSV format"}

            total = sum(int(row["amount"]) for row in reader if row["product"] == data["product"])

        return {"file": data["file"], "sum": total}

    except (csv.Error, ValueError):
        return {"file": data["file"], "error": "Invalid CSV data"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
