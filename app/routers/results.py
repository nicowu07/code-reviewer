from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from app.config import templates
from app.database.connection import get_db
from app.database.models import Scan

router = APIRouter()

@router.get("/results/{scan_id}", response_class=HTMLResponse)
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
        for i, issue in enumerate(scan.issues):
            item = dict(issue)
            if scan.ai_analysis:
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