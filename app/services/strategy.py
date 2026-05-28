from __future__ import annotations
import copy

from typing import Any

from sqlalchemy.orm import Session

from app.db import crud
from app.schemas.agent import AgentRequest, AgentResponse
from app.services.utils import ensure_dict, now_iso, to_float

_SUPPORTED_ACTIONS = {"growth_strategy"}


def _build_strategy_payload(
    analytics_data: dict[str, Any],
    operations_data: dict[str, Any],
    marketing_data: dict[str, Any],
) -> dict[str, Any]:
    sales_trends = ensure_dict(analytics_data.get("sales_trends"))
    operational_efficiency = ensure_dict(operations_data.get("operational_efficiency"))
    content_marketing = ensure_dict(marketing_data.get("content_marketing"))

    growth_rate = to_float(sales_trends.get("growth_rate"), default=0.0)
    top_products = [item for item in sales_trends.get("top_products", []) if isinstance(item, str)]
    focus_products = [item for item in content_marketing.get("focus_products", []) if isinstance(item, str)]
    market_targets = top_products or focus_products or ["Product A", "Product B"]

    estimated_revenue_increase = "35%" if growth_rate >= 10 else "18%"

    return {
        "growth_opportunities": {
            "market_expansion": {
                "new_regions": ["Europe", "Asia-Pacific"],
                "target_product_lines": market_targets,
                "estimated_revenue_increase": estimated_revenue_increase,
            },
            "product_diversification": {
                "recommended_categories": ["Accessories", "Premium line"],
                "investment_required": "$50,000",
                "projected_roi": "220%",
            },
        },
        "competitive_analysis": {
            "market_position": "Improving in premium segment",
            "competitive_advantages": [
                "Data-driven pricing",
                "Campaign-to-operations feedback loop",
            ],
            "threats": ["Price competition", "Seasonal demand swings"],
            "opportunities": ["Subscription bundles", "B2B distribution partnerships"],
        },
        "strategic_initiatives": {
            "q1_priorities": [
                "Expand into one new international market",
                "Launch high-margin premium bundle tests",
            ],
            "q2_priorities": [
                "Pilot subscription add-on offering",
                "Integrate partner distribution analytics",
            ],
            "long_term_vision": "Become a data-native, multi-region ecommerce growth engine",
            "operations_alignment": operational_efficiency,
        },
    }


def execute(request: AgentRequest, db: Session) -> AgentResponse:
    action = request.action.strip().lower()
    if action not in _SUPPORTED_ACTIONS:
        raise ValueError(f"Unknown action: {request.action}")

    analytics_data = crud.get_latest_agent_data(db, "analytics")
    operations_data = crud.get_latest_agent_data(db, "operations")
    marketing_data = request.marketing_data or crud.get_latest_agent_data(db, "marketing")

    if not isinstance(marketing_data, dict):
        marketing_data = {}

    strategy_core = _build_strategy_payload(
        analytics_data=analytics_data,
        operations_data=operations_data,
        marketing_data=marketing_data,
    )
    strategy_for_report = copy.deepcopy(strategy_core)

    comprehensive_report = {
        "report_date": now_iso(),
        "analytics": analytics_data,
        "operations": operations_data,
        "marketing": marketing_data,
        "strategy": strategy_for_report,
    }
    response_data = copy.deepcopy(strategy_core)
    response_data["comprehensive_report"] = comprehensive_report

    recommendations = [
        "Prioritize one expansion region with the strongest unit economics.",
        "Align premium bundle roadmap with campaign performance benchmarks.",
        "Review subscription pilot outcomes before broader rollout.",
    ]

    response = AgentResponse(
        agent="strategy",
        action=request.action,
        timestamp=now_iso(),
        status="completed",
        data=response_data,
        recommendations=recommendations,
        next_action="generate_report",
    )

    crud.create_agent_run(
        db,
        agent="strategy",
        action=request.action,
        status="completed",
        request_payload=request.model_dump(),
        response_payload=response.model_dump(),
    )
    crud.create_comprehensive_report(db, comprehensive_report)
    return response
