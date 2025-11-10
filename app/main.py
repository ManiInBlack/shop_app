import crud
import database
from fastapi import FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import UserLogin

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/login")
def login():
    return {"message": "Login required"}


@app.post("/login")
def login(response: UserLogin):
    with Session(database.engine) as session:
        user = crud.get_user_by_email(session, response.email)
        is_valid_password = crud.verify_password(session, response.email, response.password)

        if user and is_valid_password:
            return {"message": "Login successful"}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Basic"},
            )


@app.get("/register")
def register():
    return {"message": "Register required"}


@app.post("/register")
def register(response: UserLogin):
    with Session(database.engine) as session:
        result = crud.create_user(session, response.email, response.password)
        return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
