from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import csv
import os

app = FastAPI()
PERSISTENT_STORAGE_PATH = "/het_PV_dir"

@app.post("/compute")
async def compute(request: Request):
    try:
        data = await request.json()
        filename = data.get("file")
        product = data.get("product")

        if not filename or not product:
            return JSONResponse(status_code=400, content={"file": None, "error": "Invalid JSON input."})

        file_path = os.path.join(PERSISTENT_STORAGE_PATH, filename)
        if not os.path.exists(file_path):
            return {"file": filename, "error": "File not found."}

        try:
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                headers = [h.strip() for h in reader.fieldnames]

                # Check header validity
                if "product" not in headers or "amount" not in headers:
                    return {"file": filename, "error": "Input file not in CSV format."}

                total = 0
                for row in reader:
                    row_product = row.get("product", "").strip()
                    row_amount = row.get("amount", "").strip()

                    if row_product == product:
                        try:
                            total += int(row_amount)
                        except:
                            return {"file": filename, "error": "Input file not in CSV format."}

            return {"file": filename, "sum": total}

        except:
            return {"file": filename, "error": "Input file not in CSV format."}

    except:
        return JSONResponse(status_code=400, content={"file": None, "error": "Invalid JSON input."})
