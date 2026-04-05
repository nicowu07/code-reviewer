from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from app.exceptions import global_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError
from app.config import templates


app = FastAPI()

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

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
