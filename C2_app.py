from fastapi import FastAPI, HTTPException
import csv
import os

app = FastAPI()

# Persistent storage path in GKE
PERSISTENT_STORAGE_PATH = "/het_PV_dir"

@app.post("/compute")
def compute(data: dict):
    """Computes the sum of a product's amount in the given file."""
    if "file" not in data or "product" not in data:
        return {"file": None, "error": "Invalid JSON input."}

    file_path = os.path.join(PERSISTENT_STORAGE_PATH, data["file"])

    # Check if file exists in persistent volume
    if not os.path.exists(file_path):
        return {"file": data["file"], "error": "File not found."}

    # Read and process the CSV file
    total = 0
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            if not {"product", "amount"}.issubset(reader.fieldnames):
                raise ValueError("Invalid CSV format")

            total = sum(int(row["amount"]) for row in reader if row["product"] == data["product"])
        
        return {"file": data["file"], "sum": total}

    except (csv.Error, ValueError):
        return {"file": data["file"], "error": "Input file not in CSV format."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
