from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.db import crud
from app.schemas.agent import AgentRequest, AgentResponse
from app.services.utils import ensure_dict, now_iso, to_float, top_products_from_orders

_SUPPORTED_ACTIONS = {"daily_analysis", "customer_behavior"}


def _default_daily_analysis() -> dict[str, Any]:
    return {
        "sales_trends": {
            "total_revenue": 15420.50,
            "orders_count": 127,
            "avg_order_value": 121.42,
            "growth_rate": 12.5,
            "top_products": ["Product A", "Product B", "Product C"],
        },
        "customer_insights": {
            "new_customers": 23,
            "returning_customers": 104,
            "customer_lifetime_value": 342.15,
            "churn_risk_customers": 15,
        },
        "inventory_alerts": {
            "low_stock_items": ["Product X", "Product Y"],
            "out_of_stock": ["Product Z"],
            "overstock_items": ["Product W"],
        },
    }


def _customer_behavior(payload: dict[str, Any]) -> dict[str, Any]:
    order_value = to_float(payload.get("order_value"), default=0.0)
    customer_tier = "Premium" if order_value >= 150 else "Standard"
    frequency = "High" if to_float(payload.get("orders_last_90_days"), default=0) >= 5 else "Medium"
    return {
        "customer_segment": customer_tier,
        "purchase_frequency": frequency,
        "recommended_products": payload.get("recommended_products", ["Product D", "Product E"]),
        "upsell_opportunity": customer_tier == "Premium",
        "cross_sell_items": payload.get("cross_sell_items", ["Accessory A", "Accessory B"]),
    }


def _daily_analysis(payload: dict[str, Any]) -> dict[str, Any]:
    orders = payload.get("orders")
    inventory = payload.get("inventory")
    customers = payload.get("customers")

    if not isinstance(orders, list):
        orders = []
    if not isinstance(inventory, list):
        inventory = []
    if not isinstance(customers, list):
        customers = []

    if not orders and not inventory and not customers:
        return _default_daily_analysis()

    valid_orders = [order for order in orders if isinstance(order, dict)]
    total_revenue = round(sum(to_float(order.get("amount")) for order in valid_orders), 2)
    orders_count = len(valid_orders)
    avg_order_value = round(total_revenue / orders_count, 2) if orders_count else 0.0
    previous_revenue = to_float(payload.get("previous_revenue"))
    growth_rate = round(((total_revenue - previous_revenue) / previous_revenue) * 100, 2) if previous_revenue > 0 else 0.0

    top_products = top_products_from_orders(valid_orders)
    if not top_products:
        top_products = payload.get("top_products", ["Product A", "Product B", "Product C"])

    low_stock_items: list[str] = []
    out_of_stock_items: list[str] = []
    overstock_items: list[str] = []
    for item in inventory:
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        quantity = to_float(item.get("quantity"))
        reorder_point = to_float(item.get("reorder_point"), default=10)
        overstock_threshold = to_float(item.get("overstock_threshold"), default=150)
        if not isinstance(name, str):
            continue
        if quantity <= 0:
            out_of_stock_items.append(name)
        elif quantity <= reorder_point:
            low_stock_items.append(name)
        elif quantity >= overstock_threshold:
            overstock_items.append(name)

    new_customers = 0
    returning_customers = 0
    churn_risk_customers = 0
    for customer in customers:
        if not isinstance(customer, dict):
            continue
        status = str(customer.get("status", "")).lower()
        if status == "new":
            new_customers += 1
        elif status in {"returning", "repeat"}:
            returning_customers += 1
        churn_risk = customer.get("churn_risk")
        if churn_risk is True or str(churn_risk).lower() == "high":
            churn_risk_customers += 1

    total_known_customers = max(new_customers + returning_customers, 1)
    customer_lifetime_value = round(total_revenue / total_known_customers, 2)

    return {
        "sales_trends": {
            "total_revenue": total_revenue,
            "orders_count": orders_count,
            "avg_order_value": avg_order_value,
            "growth_rate": growth_rate,
            "top_products": top_products,
        },
        "customer_insights": {
            "new_customers": new_customers,
            "returning_customers": returning_customers,
            "customer_lifetime_value": customer_lifetime_value,
            "churn_risk_customers": churn_risk_customers,
        },
        "inventory_alerts": {
            "low_stock_items": low_stock_items,
            "out_of_stock": out_of_stock_items,
            "overstock_items": overstock_items,
        },
    }


def execute(request: AgentRequest, db: Session) -> AgentResponse:
    action = request.action.strip().lower()
    if action not in _SUPPORTED_ACTIONS:
        raise ValueError(f"Unknown action: {request.action}")

    payload = ensure_dict(request.data)
    if action == "daily_analysis":
        data = _daily_analysis(payload)
        recommendations = [
            "Prioritize campaigns for top-performing products.",
            "Launch retention outreach for churn-risk customers.",
            "Rebalance low-stock and overstock inventory positions.",
        ]
        next_action = "inventory_optimization"
    else:
        data = _customer_behavior(payload)
        recommendations = [
            "Send a personalized upsell email sequence.",
            "Highlight cross-sell products during checkout.",
        ]
        next_action = "campaign_optimization"

    response = AgentResponse(
        agent="analytics",
        action=request.action,
        timestamp=now_iso(),
        status="completed",
        data=data,
        recommendations=recommendations,
        next_action=next_action,
    )

    crud.create_agent_run(
        db,
        agent="analytics",
        action=request.action,
        status="completed",
        request_payload=request.model_dump(),
        response_payload=response.model_dump(),
    )
    return response
