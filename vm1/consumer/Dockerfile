FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
COPY consumer.py consumer.py
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "consumer:app", "--host", "0.0.0.0", "--port", "8000"]
