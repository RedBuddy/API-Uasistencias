# FastAPI Application Setup

## Step 1: Set Up a Virtual Environment

First, create a virtual environment to manage your project's dependencies. Run the following command:

```bash
python -m venv env
```

Activate the virtual environment:

- On Windows:
    ```bash
    .\env\Scripts\activate
    ```
- On macOS/Linux:
    ```bash
    source env/bin/activate
    ```

## Step 2: Install Dependencies

With the virtual environment activated, install the required libraries from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```
## Create database on localhost called UML

## Step 3: Start the FastAPI Application

To start your FastAPI application, run the following command:

```bash
uvicorn main:app --reload
```

Replace `main` with the name of your Python file (without the `.py` extension) and `app` with the name of your FastAPI instance.

Your FastAPI application should now be running and accessible at `http://127.0.0.1:8000`.

# About the libraries

SQLAlchemy: https://www.sqlalchemy.org 
FastAPI: https://fastapi.tiangolo.com
