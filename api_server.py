"""
Compatibility entrypoint for running the E-commerce AI Agents API.
"""
from app.main import app


if __name__ == "__main__":
    import uvicorn

    from app.core.settings import get_settings

    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
