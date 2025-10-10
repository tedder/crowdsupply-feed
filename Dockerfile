FROM python:3-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scrape-browse.py .

CMD ["python3", "scrape-browse.py"]
