from __future__ import annotations

from app.core.settings import get_settings


def test_root_and_health(client):
    root_response = client.get("/")
    assert root_response.status_code == 200
    assert root_response.json()["message"] == "E-commerce AI Agents API is running"

    health_response = client.get("/health")
    assert health_response.status_code == 200
    payload = health_response.json()
    assert payload["status"] == "healthy"
    assert "timestamp" in payload


def test_full_agent_pipeline_and_report(client):
    analytics_payload = {
        "action": "daily_analysis",
        "data": {
            "previous_revenue": 1000,
            "orders": [
                {"product": "Product A", "amount": 120.5},
                {"product": "Product A", "amount": 98.0},
                {"product": "Product B", "amount": 60.0},
            ],
            "inventory": [
                {"name": "Product A", "quantity": 5, "reorder_point": 10},
                {"name": "Product B", "quantity": 0, "reorder_point": 8},
                {"name": "Product C", "quantity": 220, "overstock_threshold": 150},
            ],
            "customers": [
                {"status": "new"},
                {"status": "returning", "churn_risk": "high"},
                {"status": "returning"},
            ],
        },
    }

    analytics_response = client.post("/agents/analytics", json=analytics_payload)
    assert analytics_response.status_code == 200
    analytics_data = analytics_response.json()
    assert analytics_data["agent"] == "analytics"
    assert analytics_data["next_action"] == "inventory_optimization"

    operations_response = client.post(
        "/agents/operations",
        json={
            "action": "inventory_optimization",
            "analytics_data": analytics_data["data"],
        },
    )
    assert operations_response.status_code == 200
    operations_data = operations_response.json()
    assert operations_data["agent"] == "operations"
    assert operations_data["next_action"] == "campaign_optimization"

    marketing_response = client.post(
        "/agents/marketing",
        json={
            "action": "campaign_optimization",
            "operations_data": operations_data["data"],
        },
    )
    assert marketing_response.status_code == 200
    marketing_data = marketing_response.json()
    assert marketing_data["agent"] == "marketing"
    assert marketing_data["next_action"] == "growth_strategy"

    strategy_response = client.post(
        "/agents/strategy",
        json={
            "action": "growth_strategy",
            "marketing_data": marketing_data["data"],
        },
    )
    assert strategy_response.status_code == 200
    strategy_payload = strategy_response.json()
    assert strategy_payload["agent"] == "strategy"
    assert "comprehensive_report" in strategy_payload["data"]

    report_response = client.get("/reports/comprehensive")
    assert report_response.status_code == 200
    report_payload = report_response.json()
    assert "analytics" in report_payload
    assert "operations" in report_payload
    assert "marketing" in report_payload
    assert "strategy" in report_payload

    status_response = client.get("/agents/status")
    assert status_response.status_code == 200
    status_payload = status_response.json()
    assert status_payload["data_available"]["analytics"] is True
    assert status_payload["data_available"]["operations"] is True
    assert status_payload["data_available"]["marketing"] is True
    assert status_payload["data_available"]["strategy"] is True


def test_api_key_enforcement(client):
    settings = get_settings()
    settings.api_key = "test-key"
    settings.require_api_key = True

    unauthenticated = client.get("/agents/status")
    assert unauthenticated.status_code == 401

    authenticated = client.get("/agents/status", headers={"X-API-Key": "test-key"})
    assert authenticated.status_code == 200
