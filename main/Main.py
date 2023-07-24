from fastapi import FastAPI



app = FastAPI()
@app.get("/")
async def addfileUI():
    return {"hello this is UI with this app"}
