FROM python:3.9-slim
WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /het_PV_dir

CMD ["uvicorn", "C2_app:app", "--host", "0.0.0.0", "--port", "8000"]
