from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from app.config import templates

# prevent information disclosure
async def global_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse(
        request=request,
        name='error.html'
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return templates.TemplateResponse(
        request=request,
        name='error.html'
    )