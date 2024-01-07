import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routes import contacts, auth

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix="/api")

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")


@app.get("/")
def read_root():
    return {"message": "This is API for contacts"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
