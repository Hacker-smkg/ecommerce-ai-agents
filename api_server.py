"""
FastAPI Backend for E-commerce AI Agents
This server provides REST API endpoints for n8n to call each agent
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="E-commerce AI Agents API",
    description="Backend API for multi-agent e-commerce scaling system",
    version="1.0.0"
)

# Request/Response Models
class AgentRequest(BaseModel):
    action: str
    data: Optional[Dict[Any, Any]] = None
    analytics_data: Optional[Dict[Any, Any]] = None
    operations_data: Optional[Dict[Any, Any]] = None
    marketing_data: Optional[Dict[Any, Any]] = None

class AgentResponse(BaseModel):
    agent: str
    action: str
    timestamp: str
    status: str
    data: Dict[Any, Any]
    recommendations: list
    next_action: Optional[str] = None

# In-memory storage for demo (replace with real database)
analytics_store = {}
operations_store = {}
marketing_store = {}
strategy_store = {}

@app.get("/")
def read_root():
    return {"message": "E-commerce AI Agents API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Analytics Agent Endpoint
@app.post("/agents/analytics", response_model=AgentResponse)
def analytics_agent(request: AgentRequest):
    """
    Analytics Agent - Processes sales data and customer insights
    """
    logger.info(f"Analytics Agent called with action: {request.action}")
    
    try:
        if request.action == "daily_analysis":
            # Simulate analytics processing
            analysis_results = {
                "sales_trends": {
                    "total_revenue": 15420.50,
                    "orders_count": 127,
                    "avg_order_value": 121.42,
                    "growth_rate": 12.5,
                    "top_products": ["Product A", "Product B", "Product C"]
                },
                "customer_insights": {
                    "new_customers": 23,
                    "returning_customers": 104,
                    "customer_lifetime_value": 342.15,
                    "churn_risk_customers": 15
                },
                "inventory_alerts": {
                    "low_stock_items": ["Product X", "Product Y"],
                    "out_of_stock": ["Product Z"],
                    "overstock_items": ["Product W"]
                }
            }
            
            # Store results for other agents
            analytics_store['latest_analysis'] = analysis_results
            
            recommendations = [
                "Focus marketing on top-performing products",
                "Implement retention campaign for churn-risk customers", 
                "Restock low inventory items immediately",
                "Consider promotional pricing for overstocked items"
            ]
            
            return AgentResponse(
                agent="analytics",
                action=request.action,
                timestamp=datetime.now().isoformat(),
                status="completed",
                data=analysis_results,
                recommendations=recommendations,
                next_action="operations_optimization"
            )
        
        elif request.action == "customer_behavior":
            # Process new order data
            customer_analysis = {
                "customer_segment": "Premium",
                "purchase_frequency": "High",
                "recommended_products": ["Product D", "Product E"],
                "upsell_opportunity": True,
                "cross_sell_items": ["Accessory A", "Accessory B"]
            }
            
            return AgentResponse(
                agent="analytics",
                action=request.action,
                timestamp=datetime.now().isoformat(),
                status="completed",
                data=customer_analysis,
                recommendations=["Send personalized upsell email", "Add cross-sell items to cart"],
                next_action="marketing_personalization"
            )
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown action: {request.action}")
            
    except Exception as e:
        logger.error(f"Analytics Agent error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Operations Agent Endpoint
@app.post("/agents/operations", response_model=AgentResponse)
def operations_agent(request: AgentRequest):
    """
    Operations Agent - Handles inventory and pricing optimization
    """
    logger.info(f"Operations Agent called with action: {request.action}")
    
    try:
        if request.action == "inventory_optimization":
            # Get analytics data
            analytics_data = analytics_store.get('latest_analysis', {})
            
            operations_results = {
                "inventory_actions": {
                    "reorder_needed": ["Product X", "Product Y"],
                    "reorder_quantities": {"Product X": 100, "Product Y": 50},
                    "supplier_contacts": ["Supplier A", "Supplier B"]
                },
                "pricing_optimization": {
                    "price_increases": {"Product A": {"old": 99.99, "new": 104.99}},
                    "price_decreases": {"Product W": {"old": 79.99, "new": 69.99}},
                    "promotional_pricing": {"Product Z": {"discount": 20}}
                },
                "operational_efficiency": {
                    "fulfillment_optimization": "Enable fast shipping for top products",
                    "warehouse_suggestions": "Reorganize layout for high-demand items"
                }
            }
            
            operations_store['latest_operations'] = operations_results
            
            recommendations = [
                "Place urgent reorders for low-stock items",
                "Implement dynamic pricing for optimal margins",
                "Optimize warehouse layout for efficiency",
                "Enable expedited shipping for premium customers"
            ]
            
            return AgentResponse(
                agent="operations",
                action=request.action,
                timestamp=datetime.now().isoformat(),
                status="completed",
                data=operations_results,
                recommendations=recommendations,
                next_action="marketing_campaigns"
            )
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown action: {request.action}")
            
    except Exception as e:
        logger.error(f"Operations Agent error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Marketing Agent Endpoint  
@app.post("/agents/marketing", response_model=AgentResponse)
def marketing_agent(request: AgentRequest):
    """
    Marketing Agent - Creates campaigns and content strategies
    """
    logger.info(f"Marketing Agent called with action: {request.action}")
    
    try:
        if request.action == "campaign_optimization":
            # Get operations data
            operations_data = operations_store.get('latest_operations', {})
            
            marketing_results = {
                "email_campaigns": {
                    "retention_campaign": {
                        "target": "churn_risk_customers",
                        "subject": "We miss you! Here's 15% off your next order",
                        "content": "Personalized retention email with product recommendations"
                    },
                    "upsell_campaign": {
                        "target": "premium_customers", 
                        "subject": "Exclusive products just for you",
                        "content": "Premium product showcase with VIP pricing"
                    }
                },
                "social_media": {
                    "facebook_ads": "Target lookalike audiences with top-selling products",
                    "instagram_content": "Product showcase posts with user-generated content",
                    "tiktok_strategy": "Trending hashtag campaigns with product demos"
                },
                "content_marketing": {
                    "blog_posts": ["How to style Product A", "Top 10 uses for Product B"],
                    "video_content": "Product demonstration videos",
                    "seo_keywords": ["best products 2024", "product reviews", "buying guide"]
                }
            }
            
            marketing_store['latest_marketing'] = marketing_results
            
            recommendations = [
                "Launch retention campaign for at-risk customers",
                "Increase Facebook ad spend on top-performing products", 
                "Create viral TikTok content for younger demographics",
                "Optimize SEO content for high-intent keywords"
            ]
            
            return AgentResponse(
                agent="marketing",
                action=request.action,
                timestamp=datetime.now().isoformat(),
                status="completed",
                data=marketing_results,
                recommendations=recommendations,
                next_action="strategy_planning"
            )
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown action: {request.action}")
            
    except Exception as e:
        logger.error(f"Marketing Agent error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Strategy Agent Endpoint
@app.post("/agents/strategy", response_model=AgentResponse) 
def strategy_agent(request: AgentRequest):
    """
    Strategy Agent - High-level business growth strategies
    """
    logger.info(f"Strategy Agent called with action: {request.action}")
    
    try:
        if request.action == "growth_strategy":
            # Get marketing data
            marketing_data = marketing_store.get('latest_marketing', {})
            
            strategy_results = {
                "growth_opportunities": {
                    "market_expansion": {
                        "new_regions": ["Europe", "Asia-Pacific"],
                        "target_demographics": "25-45 year olds",
                        "estimated_revenue_increase": "35%"
                    },
                    "product_diversification": {
                        "recommended_categories": ["Accessories", "Premium line"],
                        "investment_required": "$50000",
                        "projected_roi": "250%"
                    }
                },
                "competitive_analysis": {
                    "market_position": "Strong in premium segment",
                    "competitive_advantages": ["Product quality", "Customer service"],
                    "threats": ["Price competition", "New entrants"],
                    "opportunities": ["Subscription model", "B2B expansion"]
                },
                "strategic_initiatives": {
                    "q1_priorities": ["International expansion", "Premium line launch"],
                    "q2_priorities": ["Subscription model", "B2B channel development"], 
                    "long_term_vision": "Market leader in premium e-commerce segment"
                }
            }
            
            strategy_store['latest_strategy'] = strategy_results
            
            # Generate comprehensive report
            comprehensive_report = {
                "executive_summary": "Strong growth trajectory with 35% revenue increase opportunity",
                "key_metrics": analytics_store.get('latest_analysis', {}),
                "operational_changes": operations_store.get('latest_operations', {}),
                "marketing_initiatives": marketing_store.get('latest_marketing', {}),
                "strategic_roadmap": strategy_results,
                "action_items": [
                    "Begin international market research",
                    "Develop premium product line business case", 
                    "Test subscription model with core customers",
                    "Explore B2B partnership opportunities"
                ]
            }
            
            recommendations = [
                "Begin market research for international expansion",
                "Develop business case for premium product line",
                "Test subscription model with loyal customers", 
                "Explore strategic B2B partnerships",
                "Invest in competitive intelligence tools"
            ]
            
            return AgentResponse(
                agent="strategy",
                action=request.action,
                timestamp=datetime.now().isoformat(),
                status="completed",
                data={**strategy_results, "comprehensive_report": comprehensive_report},
                recommendations=recommendations,
                next_action="generate_report"
            )
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown action: {request.action}")
            
    except Exception as e:
        logger.error(f"Strategy Agent error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Utility endpoints for n8n
@app.get("/agents/status")
def get_agents_status():
    """Get status of all agents and latest data"""
    return {
        "agents": {
            "analytics": {"status": "active", "last_run": datetime.now().isoformat()},
            "operations": {"status": "active", "last_run": datetime.now().isoformat()},
            "marketing": {"status": "active", "last_run": datetime.now().isoformat()},
            "strategy": {"status": "active", "last_run": datetime.now().isoformat()}
        },
        "data_available": {
            "analytics": bool(analytics_store),
            "operations": bool(operations_store),
            "marketing": bool(marketing_store), 
            "strategy": bool(strategy_store)
        }
    }

@app.get("/reports/comprehensive")
def get_comprehensive_report():
    """Generate comprehensive business report"""
    return {
        "report_date": datetime.now().isoformat(),
        "analytics": analytics_store.get('latest_analysis', {}),
        "operations": operations_store.get('latest_operations', {}),
        "marketing": marketing_store.get('latest_marketing', {}),
        "strategy": strategy_store.get('latest_strategy', {})
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
