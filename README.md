# E-commerce AI Agents
A modular multi-agent backend for ecommerce orchestration with FastAPI, SQLAlchemy persistence, and n8n workflow integration.

## What is implemented
- Modular FastAPI backend under `app/` (no monolithic single-file logic).
- Four agent services with chained orchestration:
  - Analytics → Operations → Marketing → Strategy.
- Persistent run history and report snapshots in SQL database (`DATABASE_URL`, SQLite by default).
- API key protection for non-health routes (`X-API-Key`, configurable in `.env`).
- Updated n8n workflow template for JSON payload chaining.
- Automated test coverage for health, auth, status, pipeline execution, and report generation.

## Architecture
```
Trigger (Cron/Webhook)
  -> /agents/analytics
  -> /agents/operations
  -> /agents/marketing
  -> /agents/strategy
  -> /reports/comprehensive
```

## Project structure
```
ecommerce-ai-agents/
├── app/
│   ├── api/
│   │   ├── deps.py
│   │   └── routers/
│   │       ├── agents.py
│   │       ├── health.py
│   │       └── reports.py
│   ├── core/
│   │   ├── logging.py
│   │   └── settings.py
│   ├── db/
│   │   ├── crud.py
│   │   ├── models.py
│   │   └── session.py
│   ├── schemas/
│   │   ├── agent.py
│   │   └── report.py
│   ├── services/
│   │   ├── analytics.py
│   │   ├── operations.py
│   │   ├── marketing.py
│   │   ├── strategy.py
│   │   └── utils.py
│   └── main.py
├── api_server.py
├── n8n_workflows/ecommerce-agents-workflow-template.json
├── tests/
├── start_api.sh
└── start_n8n.sh
```

## Quick start
1) Install dependencies:
```bash
pip install -r requirements.txt
```

2) Configure environment:
```bash
cp .env.example .env
```

3) Start API server:
```bash
./start_api.sh
```
API docs: `http://localhost:8000/docs`

4) Start n8n in another terminal:
```bash
./start_n8n.sh
```
n8n UI: `http://localhost:5678`

5) In n8n, import:
- `n8n_workflows/ecommerce-agents-workflow-template.json`

## API authentication
- Health routes are public:
  - `GET /`
  - `GET /health`
- Other routes can require an API key:
  - Set `REQUIRE_API_KEY=true`
  - Set `API_KEY=<your_key>`
  - Send header: `X-API-Key: <your_key>`

## API endpoints
- `POST /agents/analytics`
- `POST /agents/operations`
- `POST /agents/marketing`
- `POST /agents/strategy`
- `GET /agents/status`
- `GET /reports/comprehensive`

## Example requests
Analytics:
```bash
curl -X POST "http://localhost:8000/agents/analytics" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "daily_analysis",
    "data": {
      "previous_revenue": 10000,
      "orders": [
        {"product": "Product A", "amount": 180.5},
        {"product": "Product B", "amount": 99.9}
      ],
      "inventory": [
        {"name": "Product A", "quantity": 8, "reorder_point": 10},
        {"name": "Product C", "quantity": 220, "overstock_threshold": 150}
      ]
    }
  }'
```

Comprehensive report:
```bash
curl "http://localhost:8000/reports/comprehensive"
```

## Tests
Run:
```bash
pytest
```

## Notes
- The backend currently implements deterministic, data-driven agent logic with persistence and orchestration hooks.
- External platform integrations (Shopify, GA, ads) are prepared via config placeholders and can be extended in service modules.
