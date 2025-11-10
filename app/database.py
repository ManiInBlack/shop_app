from sqlalchemy import create_engine, text

# Create engine (the connection to SQLite)
engine = create_engine(f"sqlite:///D:/databases/shop_app.db", echo=True)

# Create a test connection
with engine.connect() as conn:
    result = conn.execute(text("SELECT sqlite_version();"))
    print("SQLite version:", result.scalar())


