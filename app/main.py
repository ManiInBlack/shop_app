from fastapi import FastAPI
from routers import auth

app = FastAPI()
app.include_router(auth.router, prefix="/api")


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
