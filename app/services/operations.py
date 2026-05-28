from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.db import crud
from app.schemas.agent import AgentRequest, AgentResponse
from app.services.utils import ensure_dict, now_iso, to_float

_SUPPORTED_ACTIONS = {"inventory_optimization"}


def _build_operations_payload(analytics_data: dict[str, Any]) -> dict[str, Any]:
    inventory_alerts = ensure_dict(analytics_data.get("inventory_alerts"))
    sales_trends = ensure_dict(analytics_data.get("sales_trends"))

    low_stock = [item for item in inventory_alerts.get("low_stock_items", []) if isinstance(item, str)]
    out_of_stock = [item for item in inventory_alerts.get("out_of_stock", []) if isinstance(item, str)]
    overstock = [item for item in inventory_alerts.get("overstock_items", []) if isinstance(item, str)]
    top_products = [item for item in sales_trends.get("top_products", []) if isinstance(item, str)]
    growth_rate = to_float(sales_trends.get("growth_rate"), default=0.0)

    reorder_needed = sorted(set(low_stock + out_of_stock))
    reorder_quantities = {item: 150 if item in out_of_stock else 75 for item in reorder_needed}

    price_increases = {}
    if growth_rate >= 10 and top_products:
        product = top_products[0]
        price_increases[product] = {"direction": "increase", "percentage": 5}

    price_decreases = {item: {"direction": "decrease", "percentage": 10} for item in overstock}
    promotional_pricing = {item: {"discount": 15} for item in out_of_stock}

    return {
        "inventory_actions": {
            "reorder_needed": reorder_needed,
            "reorder_quantities": reorder_quantities,
            "supplier_contacts": ["primary-supplier@company.com", "backup-supplier@company.com"],
        },
        "pricing_optimization": {
            "price_increases": price_increases,
            "price_decreases": price_decreases,
            "promotional_pricing": promotional_pricing,
        },
        "operational_efficiency": {
            "fulfillment_optimization": "Prioritize high-margin products for same-day dispatch.",
            "warehouse_suggestions": "Relocate fast-moving SKUs closer to packing stations.",
        },
    }


def execute(request: AgentRequest, db: Session) -> AgentResponse:
    action = request.action.strip().lower()
    if action not in _SUPPORTED_ACTIONS:
        raise ValueError(f"Unknown action: {request.action}")

    analytics_data = request.analytics_data or crud.get_latest_agent_data(db, "analytics")
    if not isinstance(analytics_data, dict):
        analytics_data = {}

    data = _build_operations_payload(analytics_data)
    recommendations = [
        "Issue purchase orders for stockout and low-stock SKUs.",
        "Apply dynamic pricing updates before the next campaign cycle.",
        "Review warehouse routing changes with fulfillment leads.",
    ]

    response = AgentResponse(
        agent="operations",
        action=request.action,
        timestamp=now_iso(),
        status="completed",
        data=data,
        recommendations=recommendations,
        next_action="campaign_optimization",
    )

    crud.create_agent_run(
        db,
        agent="operations",
        action=request.action,
        status="completed",
        request_payload=request.model_dump(),
        response_payload=response.model_dump(),
    )
    return response
