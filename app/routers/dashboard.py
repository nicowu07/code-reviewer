from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from app.config import templates
from app.database.connection import get_db
from app.database.models import Scan
from sqlalchemy import func,text

router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
async def results(request: Request, db = Depends(get_db)):
    total_scans = db.query(func.count(Scan.id)).scalar()
    total_issues = db.query(func.sum(Scan.severity_high + Scan.severity_medium + Scan.severity_low)).scalar() or 0
    most_common_issue = db.execute(text("""
        SELECT
            issue->>'test_name' as test_name,
            COUNT(*) as count
        FROM scans,
            jsonb_array_elements(issues::jsonb) as issue
        GROUP BY test_name
        ORDER BY count DESC
        LIMIT 5
    """)).fetchall()
    return templates.TemplateResponse(
        request=request,
        name='dashboard.html',
        context={"total_scans": total_scans, "total_issues": total_issues, "most_common_issue": most_common_issue}
    )