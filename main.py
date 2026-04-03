from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# prevent information disclosure
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse(
        request=request,
        name='error.html'
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return templates.TemplateResponse(
        request=Request,
        name='error.html'
    )

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"result": None, "code": ""}
    )

@app.post("/review", response_class=HTMLResponse)
async def review(request: Request, code: str = Form("")):
    line_count = len(code.splitlines())
    char_count = len(code)
    # code limit check
    if char_count > 50000:
        result = "Code limit reached, Please split in several submits!"
        return templates.TemplateResponse(
            request=request,
            name='index.html',
            context={"result": result, "code": ""}
        )
    # empty code check
    elif char_count == 0:
        result = "No code submitted."
        return templates.TemplateResponse(
            request=request,
            name='index.html',
            context={"result":result, "code": ""}
        )
    # normal response
    result = f"Received {line_count} lines of code. Analysis coming soon!"
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"result": result, "code": code}
    )
