from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"result": None, "code": ""}
    )

@app.post("/review", response_class=HTMLResponse)
async def review(request: Request, code: str = Form(...)):
    line_count = len(code.splitlines())
    result = f"Received {line_count} lines of code. Analysis coming soon!"
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"result": result, "code": code}
    )
