from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import verify_api_key
from app.db import crud
from app.db.session import get_db
from app.schemas.report import ComprehensiveReportResponse
from app.services.utils import now_iso

router = APIRouter(tags=["reports"], dependencies=[Depends(verify_api_key)])


@router.get("/reports/comprehensive", response_model=ComprehensiveReportResponse)
def get_comprehensive_report(db: Session = Depends(get_db)) -> ComprehensiveReportResponse:
    latest_report = crud.get_latest_comprehensive_report(db)
    if latest_report:
        return ComprehensiveReportResponse(**latest_report)

    return ComprehensiveReportResponse(
        report_date=now_iso(),
        analytics=crud.get_latest_agent_data(db, "analytics"),
        operations=crud.get_latest_agent_data(db, "operations"),
        marketing=crud.get_latest_agent_data(db, "marketing"),
        strategy=crud.get_latest_agent_data(db, "strategy"),
    )
