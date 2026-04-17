from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from app.exceptions import global_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError
from app.config import templates
from app.analyzers.bandit import bandit_analyzer
from app.database.connection import Base, data_engine, get_db
from app.database.models import Scan

import tempfile


app = FastAPI()
Base.metadata.create_all(bind=data_engine)

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
async def review(request: Request, code: str = Form(""), db = Depends(get_db)):
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
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name
    issue_num, issues, returnCode = bandit_analyzer(temp_file_path)
    '''
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"result": result, "code": code}
    )
    '''
    scan = Scan(
        lines_of_code=line_count,
        severity_high=issue_num.get("SEVERITY.HIGH", 0),
        severity_medium=issue_num.get("SEVERITY.MEDIUM", 0),
        severity_low=issue_num.get("SEVERITY.LOW", 0),
        issues=issues
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return RedirectResponse(url=f"/results/{scan.id}", status_code=303)

@app.get("/results/{scan_id}", response_class=HTMLResponse)
async def results(request: Request, scan_id: str, db = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        return templates.TemplateResponse(
            request=request,
            name='results.html',
            context={"error":"The scan id not found."}
        )
    else:
        return templates.TemplateResponse(
            request=request,
            name='results.html',
            context={"scan": scan}
        )