from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from agent import run_agent

app = FastAPI(title="Medical Agent")
templates = Jinja2Templates(directory="templates")

class Query(BaseModel):
    symptoms: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/recommend")
async def recommend(query: Query):
    result = run_agent(query.symptoms)
    return result