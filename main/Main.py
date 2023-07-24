from fastapi import FastAPI
from database import database


app = FastAPI()
@app.get("/")
async def addfileUI():
    return {"hello this is UI with this app"}
