from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create engine (the connection to SQLite)
engine = create_engine(f"sqlite:///D:/databases/shop_app.db", echo=True)

# Create a test connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
