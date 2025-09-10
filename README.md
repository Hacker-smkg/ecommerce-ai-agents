# 🤖 E-commerce AI Agents - Multi-Agent System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)
![AI](https://img.shields.io/badge/AI-Powered-FF6B6B?style=for-the-badge&logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/Hacker-smkg/ecommerce-ai-agents?style=for-the-badge&logo=github)
![Forks](https://img.shields.io/github/forks/Hacker-smkg/ecommerce-ai-agents?style=for-the-badge&logo=github)

**🚀 A comprehensive multi-agent AI system designed to help scale e-commerce businesses through intelligent automation and insights.**

[🎯 Live Demo](https://github.com/Hacker-smkg/ecommerce-ai-agents) • [📚 Documentation](#-quick-start) • [🤝 Contributing](#-development)

</div>

---

## 🏗️ Architecture

This system uses a **multi-agent architecture** with 4 specialized agents orchestrated through **n8n workflows**:

```
📊 Analytics Agent → ⚙️ Operations Agent → 📢 Marketing Agent → 🎯 Strategy Agent
```

### Agent Responsibilities

1. **📊 Analytics Agent**
   - Sales trend analysis
   - Customer behavior insights  
   - Inventory alerts
   - Performance metrics

2. **⚙️ Operations Agent**
   - Inventory optimization
   - Pricing strategies
   - Supplier management
   - Operational efficiency

3. **📢 Marketing Agent**
   - Campaign creation & optimization
   - Content generation
   - Social media strategies
   - SEO optimization

4. **🎯 Strategy Agent**
   - Growth opportunities analysis
   - Market expansion strategies
   - Competitive intelligence
   - Long-term planning

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install n8n globally (already done if you followed setup)
npm install -g n8n
```

### 2. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys
nano .env
```

### 3. Start the System

#### Terminal 1: Start n8n (Visual Workflow Engine)
```bash
./start_n8n.sh
```
- Open browser to: `http://localhost:5678`
- Import workflow from: `n8n_workflows/ecommerce-agents-workflow-template.json`

#### Terminal 2: Start API Server (Agent Backend)
```bash
./start_api.sh
```
- API available at: `http://localhost:8000`
- API docs at: `http://localhost:8000/docs`

## 🔄 Workflow Examples

### Daily Business Analysis Workflow
```
🕒 Cron Trigger (9 AM Daily)
↓
📊 Analytics Agent (Sales Analysis)
↓  
⚙️ Operations Agent (Inventory Check)
↓
📢 Marketing Agent (Campaign Performance)
↓
🎯 Strategy Agent (Growth Recommendations)
↓
📧 Email Report
```

### Real-time Order Processing
```
🌐 Shopify Webhook (New Order)
↓
📊 Analytics Agent (Customer Analysis)
↓
📢 Marketing Agent (Upsell Recommendations)  
↓
⚙️ Operations Agent (Inventory Update)
```

## 🔌 API Endpoints

### Agent Endpoints
- `POST /agents/analytics` - Analytics processing
- `POST /agents/operations` - Operations optimization
- `POST /agents/marketing` - Marketing campaigns
- `POST /agents/strategy` - Strategy planning

### Utility Endpoints
- `GET /agents/status` - Check agent status
- `GET /reports/comprehensive` - Full business report
- `GET /health` - Health check

### Example API Call
```bash
curl -X POST "http://localhost:8000/agents/analytics" \
  -H "Content-Type: application/json" \
  -d '{"action": "daily_analysis", "data": {}}'
```

## 📁 Project Structure

```
ecommerce-ai-agents/
├── agents/                 # Individual agent implementations
├── config/                 # Configuration files
│   └── settings.py        # App settings
├── tools/                  # Shared tools and utilities
├── workflows/              # Workflow definitions
├── n8n_workflows/          # n8n workflow templates
├── data/                   # Data storage
├── tests/                  # Test files
├── api_server.py          # FastAPI backend server
├── start_n8n.sh          # n8n startup script
├── start_api.sh          # API server startup script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

## 🎮 Using n8n Visual Workflows

1. **Access n8n**: Open `http://localhost:5678` in your browser
2. **Import Workflow**: 
   - Click "+" → Import from File
   - Select `n8n_workflows/ecommerce-agents-workflow-template.json`
3. **Customize Workflow**:
   - Add triggers (webhooks, cron jobs)
   - Modify agent parameters
   - Add integrations (Slack, email, databases)
4. **Execute Workflow**: 
   - Test with manual triggers
   - Enable for production use

### n8n Workflow Features

**Triggers Available:**
- ⏰ Cron Scheduler - Daily/weekly analysis
- 🌐 Webhooks - Real-time data from Shopify, etc.
- 📧 Email Triggers - Process email requests
- 📊 HTTP Requests - External system integration

**Actions Available:**  
- 📧 Send Emails - Reports and notifications
- 💬 Slack Messages - Team updates
- 📊 Google Sheets - Data logging
- 🗄️ Database Updates - Store insights

## 🔗 Integration Options

### E-commerce Platforms
- **Shopify**: Product data, orders, customers
- **WooCommerce**: WordPress integration
- **Amazon**: Marketplace data
- **BigCommerce**: Enterprise features

### Marketing Platforms  
- **Facebook Ads**: Campaign optimization
- **Google Ads**: Keyword and bid management
- **Mailchimp**: Email marketing
- **HubSpot**: CRM integration

### Analytics Platforms
- **Google Analytics**: Website traffic
- **Mixpanel**: User behavior
- **Amplitude**: Product analytics

## 💡 Customization

### Adding New Agents
1. Create new endpoint in `api_server.py`
2. Add agent to n8n workflow  
3. Define agent logic and integrations
4. Update workflow connections

### Custom Workflows
1. Design workflow in n8n visual editor
2. Connect to agent endpoints
3. Add custom triggers and actions
4. Test and deploy

## 📊 Monitoring & Reporting

### Built-in Reports
- Daily business summary
- Agent performance metrics
- Workflow execution logs
- Integration status

### Custom Dashboards
- Connect to BI tools (Tableau, PowerBI)
- Export data to Google Sheets
- Real-time Slack notifications

## 🔧 Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black .
flake8 .
```

### Adding Dependencies
```bash
pip install new-package
pip freeze > requirements.txt
```

## 🚀 Production Deployment

### Environment Setup
- Set production environment variables
- Configure database connections
- Set up monitoring and logging

### Scaling Options
- Deploy API server with Docker
- Use managed n8n hosting
- Implement load balancing
- Add Redis for caching

## 📝 Next Steps

1. **Test the System**: Run both servers and test the workflow
2. **Add Real Integrations**: Connect to your Shopify store, analytics
3. **Customize Agents**: Modify agent logic for your business needs
4. **Expand Workflows**: Create specialized workflows for different scenarios
5. **Add Monitoring**: Implement logging and alerting
6. **Scale Up**: Move to production infrastructure

## 🆘 Support

- Check API documentation at `http://localhost:8000/docs`
- Review n8n workflow execution logs
- Monitor agent responses and errors
- Test individual endpoints before full workflow

---

**Happy Scaling! 🚀**

Your multi-agent e-commerce system is ready to help grow your business through intelligent automation and insights.
