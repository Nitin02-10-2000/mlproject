FROM python:3.9-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir awscli
COPY . .
CMD ["python", "app.py"]