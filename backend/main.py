from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent

app.mount("/css", StaticFiles(directory=BASE_DIR / "css"), name="css")
app.mount("/images", StaticFiles(directory=BASE_DIR / "images"), name="images")

class AnalyzeRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return FileResponse(BASE_DIR / "index.html")

@app.get("/script.js")
def javascript():
    return FileResponse(BASE_DIR / "script.js", media_type="application/javascript")

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    return {"text": request.text}
