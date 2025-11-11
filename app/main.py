import crud
import database
from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from dependencies import auth_user, register_user
from app.schemas import UserCreate

app = FastAPI()
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(user_router, prefix="/api")
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/login")
def login():
    return {"message": "Login required"}


@app.post("/login")
def login(response: UserCreate, db: Session = Depends(database.get_db)):
    if auth_user(db, str(response.email), response.password):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.get("/register")
def register():
    return {"message": "Register required"}


@app.post("/register")
def register(response: UserCreate, db: Session = Depends(database.get_db)):
    if register_user(db, str(response.email), response.password):
        return {"message": "Registration successful"}
    else:
        return {"message": "Registration failed"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
