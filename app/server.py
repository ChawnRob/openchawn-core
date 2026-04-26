from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AskRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"message": "OpenChawn is alive"}

@app.post("/ask")
def ask(request: AskRequest):
    return {
        "response": f"OpenChawn received: {request.prompt}",
        "status": "ok"
    }
