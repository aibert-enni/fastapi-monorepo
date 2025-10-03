FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY api ./api
COPY certs ./certs
COPY proto ./proto

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]