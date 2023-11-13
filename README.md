# products-analysis-back

## Project setup

1. Create a virtual environment with python

    - `python -m venv venv`

2. Activate the virtual environment

    - `venv\Scripts\activate.bat`

**NOTES:** You might need to activate the virtual environment every time you open the project with VSCode
    
2. Install dependencies

    - ```pip install -r requirements.txt```
    
3. Create a .env file with the following variables

    - CONNECTION_STRING="Your mongo connection string"

4. Run the project

    - ```uvicorn main:app --reload```

## Endpoints

### /

- **GET**: Fetches all the products. This is the endpoint that you need to call every time you start the app.

### /correlation/{column1}/{column2}

- **GET**: Fetches the correlation between two columns. The columns must contain numerical values.

### /productsByStars

- **GET**: Fetches the products grouped by stars.

### /topProductsByCategoryName/{category_name}

- **GET**: Fetches the top products by category name.

### /categories

- **GET**: Fetches all the categories.