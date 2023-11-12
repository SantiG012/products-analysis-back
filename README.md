# products-analysis-back

## Project setup

    1. Create a virtual environment with python

        - `python -m venv venv`
        - `venv\Scripts\activate.bat`
    
    2. Install dependencies

        - `pip install -r requirements.txt`
    
    3. Create a .env file with the following variables

        - CONNECTION_STRING="Your mongo connection string"

    4. Run the project

        - `uvicorn main:app --reload`