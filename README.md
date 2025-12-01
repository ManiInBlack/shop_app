# 🛒 Shop API -- My First Python Project

Welcome to my first Python project --- a **Shop API** built with
**FastAPI**, designed to manage users, authentication, products,
categories, and orders.

## ✨ Features

-   Account creation & login\
-   Password change\
-   User management\
-   Listing products & categories\
-   Order handling\
-   SQLite/SQLAlchemy database integration\
-   JWT authentication

## 🚀 Technologies Used

-   Python\
-   FastAPI\
-   SQLAlchemy\
-   Pydantic\
-   JWT\
-   pytest

## 📂 Project Structure

    shop_app/
    │
    ├── app/
    │   ├── main.py                # FastAPI entry point
    │   ├── database.py            # Database config
    │   ├── models.py              # ORM models
    │   ├── schemas.py             # Pydantic schemas
    │   ├── crud.py                # CRUD operations
    │   ├── dependencies.py        # Authorization helpers
    │   ├── routers/
    │   │   ├── users.py
    │   │   ├── products.py
    │   │   ├── orders.py
    │   │   └── auth.py
    │   └── utils/
    │       ├── hashing.py         # Password hashing
    │       ├── jwt_handler.py     # JWT creation
    │       └── validators.py      # Additional validators
    │
    ├── tests/
    │   ├── test_users.py
    │   ├── test_products.py
    │   └── test_orders.py
    │
    ├── requirements.txt
    ├── README.md
    └── .env

## ▶️ Running the Project

1.  Install dependencies:

    ``` bash
    pip install -r requirements.txt
    ```

2.  Run the API server:

    ``` bash
    uvicorn app.main:app --reload
    ```

## 📬 Contact

Feel free to reach out or contribute!
