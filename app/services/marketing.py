from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.db import crud
from app.schemas.agent import AgentRequest, AgentResponse
from app.services.utils import ensure_dict, now_iso

_SUPPORTED_ACTIONS = {"campaign_optimization"}


def _build_marketing_payload(operations_data: dict[str, Any]) -> dict[str, Any]:
    inventory_actions = ensure_dict(operations_data.get("inventory_actions"))
    pricing_optimization = ensure_dict(operations_data.get("pricing_optimization"))

    reorder_needed = [item for item in inventory_actions.get("reorder_needed", []) if isinstance(item, str)]
    price_increases = ensure_dict(pricing_optimization.get("price_increases"))
    price_decreases = ensure_dict(pricing_optimization.get("price_decreases"))

    focus_products = sorted(set(reorder_needed + list(price_increases.keys()) + list(price_decreases.keys())))
    if not focus_products:
        focus_products = ["Product A", "Product B"]

    return {
        "email_campaigns": {
            "retention_campaign": {
                "target": "high-ltv-and-at-risk-customers",
                "subject": "Exclusive comeback offer for your favorite picks",
                "content": "Personalized recommendations with limited-time incentives.",
            },
            "upsell_campaign": {
                "target": "premium-customers",
                "subject": "Upgrade your cart with curated premium bundles",
                "content": "Product bundles optimized for margin and customer lifetime value.",
            },
        },
        "social_media": {
            "facebook_ads": f"Promote inventory-backed products: {', '.join(focus_products)}",
            "instagram_content": "Use customer stories and short-form product explainers.",
            "tiktok_strategy": "Run creator-led demos focused on high-converting products.",
        },
        "content_marketing": {
            "focus_products": focus_products,
            "blog_posts": [
                "How to choose the best product combination for your goals",
                "What makes premium ecommerce experiences convert better",
            ],
            "seo_keywords": ["ecommerce growth strategy", "inventory optimization", "high-converting product bundles"],
        },
    }


def execute(request: AgentRequest, db: Session) -> AgentResponse:
    action = request.action.strip().lower()
    if action not in _SUPPORTED_ACTIONS:
        raise ValueError(f"Unknown action: {request.action}")

    operations_data = request.operations_data or crud.get_latest_agent_data(db, "operations")
    if not isinstance(operations_data, dict):
        operations_data = {}

    data = _build_marketing_payload(operations_data)
    recommendations = [
        "Deploy retention and upsell campaigns in parallel cohorts.",
        "Shift paid budget toward inventory-backed focus products.",
        "Measure campaign lift against margin and repeat-purchase KPIs.",
    ]

    response = AgentResponse(
        agent="marketing",
        action=request.action,
        timestamp=now_iso(),
        status="completed",
        data=data,
        recommendations=recommendations,
        next_action="growth_strategy",
    )

    crud.create_agent_run(
        db,
        agent="marketing",
        action=request.action,
        status="completed",
        request_payload=request.model_dump(),
        response_payload=response.model_dump(),
    )
    return response
