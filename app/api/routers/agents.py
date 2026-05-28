from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import verify_api_key
from app.db import crud
from app.db.session import get_db
from app.schemas.agent import AgentRequest, AgentResponse
from app.schemas.report import AgentRuntimeStatus, AgentStatusResponse
from app.services import analytics, marketing, operations, strategy

router = APIRouter(prefix="/agents", tags=["agents"], dependencies=[Depends(verify_api_key)])


@router.post("/analytics", response_model=AgentResponse)
def analytics_agent(request: AgentRequest, db: Session = Depends(get_db)) -> AgentResponse:
    try:
        return analytics.execute(request, db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/operations", response_model=AgentResponse)
def operations_agent(request: AgentRequest, db: Session = Depends(get_db)) -> AgentResponse:
    try:
        return operations.execute(request, db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/marketing", response_model=AgentResponse)
def marketing_agent(request: AgentRequest, db: Session = Depends(get_db)) -> AgentResponse:
    try:
        return marketing.execute(request, db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/strategy", response_model=AgentResponse)
def strategy_agent(request: AgentRequest, db: Session = Depends(get_db)) -> AgentResponse:
    try:
        return strategy.execute(request, db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/status", response_model=AgentStatusResponse)
def get_agents_status(db: Session = Depends(get_db)) -> AgentStatusResponse:
    agents_payload, data_available = crud.get_agents_status(db)
    return AgentStatusResponse(
        agents={name: AgentRuntimeStatus(**details) for name, details in agents_payload.items()},
        data_available=data_available,
    )
