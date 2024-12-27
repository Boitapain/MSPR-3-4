# Project Overview

## Notebook (ToDo)
The notebook is designed to perform various data analysis tasks. It includes functionalities such as data cleaning, visualization, and model training. Detailed instructions on how to use the notebook will be provided here.

## App
The app is a web-based application built using Streamlit. It allows users to log in, create accounts, and navigate through different sections such as Home, Profile, and Settings. The app is designed to be responsive and user-friendly.

### Features
- **Login:** Users can log in using their email and password.
- **Create Account:** New users can create an account.
- **Dashboard:** After logging in, users can navigate through different sections using the sidebar.
  - **Home:** Displays a welcome message.
  - **ToDo**

## Setup Instructions

### Cloning the Repository
To clone the repository, run the following command:
```bash
git clone https://github.com/Boitapain/MSPR1.git
cd MSPR1
```

### Setting Up the Python Environment

#### MacOS/Linux
1. **Install Python 3.9+**:
   ```bash
   sudo apt-get update
   sudo apt-get install python3.9 python3.9-venv python3.9-dev
   ```

2. **Create a virtual environment**:
   ```bash
   python3.9 -m venv venv
   ```

3. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

#### Windows
1. **Install Python 3.9+**:
   Download and install Python from [python.org](https://www.python.org/downloads/).

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   ```bash
   .\venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

1. Start the Flask API:
    ```bash
    python app/api/api.py
    ```

2. In a new terminal, start the Streamlit app:
    ```bash
    streamlit run app/app.py
    ```

This will start the Flask API server and the Streamlit server. The Streamlit app will open in your default web browser.

### Using Swagger UI

To test the API endpoints using Swagger UI, open your web browser and navigate to: http://127.0.0.1:5000/swagger

You will see the Swagger UI interface where you can test the API endpoints defined in the `openapi.yaml` file.