FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install mlflow if not in requirements.txt
RUN pip install mlflow

COPY . .

EXPOSE 8888
EXPOSE 8008

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]