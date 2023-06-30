from fastapi import FastAPI
app = FastAPI()
@app.get("/")
async  def Update():
    return ("this is frint")
