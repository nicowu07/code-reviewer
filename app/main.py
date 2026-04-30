from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import UploadFile, File
from app.exceptions import global_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError
from app.config import templates
from app.analyzers.bandit import bandit_analyzer
from app.database.connection import Base, data_engine, get_db
from app.database.models import Scan
from app.logger import logger
from app.config import CODE_LIMIT
from app.analyzers.ai import ai_analyzer

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
async def review(request: Request, code: str = Form(""), file: UploadFile = File(None), db = Depends(get_db)):
    logger.info("Code review requested by %s", request.client.host)
    if file and file.filename:
        if not (file.filename.endswith('.py') or file.filename.endswith('.ipynb')):
            result = "Please upload a python file!"
            logger.warning(f"Unsupported file type uploaded: {file.filename}")
            return templates.TemplateResponse(
                request=request,
                name='index.html',
                context={"result":result, "code": ""}
            )
        contents = await file.read()
        try:
            code = contents.decode("utf-8")
        except UnicodeDecodeError:
            result = "File decoding failed! Please ensure the file is a valid UTF-8 encoded text file."
            logger.warning(f"Failed to decode file: {file.filename}")
            return templates.TemplateResponse(
                request=request,
                name='index.html',
                context={"result": result, "code": ""}
            )
    line_count = len(code.splitlines())
    char_count = len(code)
    # code limit check
    if char_count > CODE_LIMIT:
        result = "Code limit reached, Please split in several submits!"
        logger.warning(f"Code submission exceeded character limit: {char_count} characters")
        return templates.TemplateResponse(
            request=request,
            name='index.html',
            context={"result": result, "code": ""}
        )
    # empty code check
    elif char_count == 0:
        result = "No code or file submitted."
        logger.warning("No code or file submitted.")
        return templates.TemplateResponse(
            request=request,
            name='index.html',
            context={"result":result, "code": ""}
        )
    # normal response
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name
    issue_num, issues, returnCode = bandit_analyzer(temp_file_path)
    if returnCode == 2:
        result = "Analysis failed!"
        logger.error("Bandit analysis failed for the submitted code.")
        return templates.TemplateResponse(
            request=request,
            name='index.html',
            context={"result":result, "code": ""}
        )
    elif returnCode == 1:
        result = "Result parsing failed!"
        logger.error("Failed to parse Bandit output for the submitted code.")
        return templates.TemplateResponse(
            request=request,
            name='index.html',
            context={"result":result, "code": ""}
        )
    ai_result = ai_analyzer(issues)
    if "error" in ai_result:
        logger.error(f"AI analysis failed: {ai_result['error']}")
        ai_result = None
    scan = Scan(
        lines_of_code=line_count,
        severity_high=issue_num.get("SEVERITY.HIGH", 0),
        severity_medium=issue_num.get("SEVERITY.MEDIUM", 0),
        severity_low=issue_num.get("SEVERITY.LOW", 0),
        issues=issues,
        ai_analysis=ai_result
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    logger.info(f"Scan completed and stored with ID: {scan.id}")
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
        combined = []
        if scan.ai_analysis:
            for i, issue in enumerate(scan.issues):
                item = dict(issue)
                for analysis in scan.ai_analysis:
                    if i == analysis["issue_index"]:
                        item["ai_analysis"] = analysis
                        break
                combined.append(item)
        return templates.TemplateResponse(
            request=request,
            name='results.html',
            context={"scan": scan, "combined": combined}
        )