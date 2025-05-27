#!/bin/bash

# Start MLflow server in the background
mlflow server --host 0.0.0.0 --port 8008 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns &

# Start Jupyter Notebook in the foreground
exec jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser