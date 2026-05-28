from __future__ import annotations
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.settings import get_settings
from app.db.session import reset_db
from app.main import create_app


@pytest.fixture(autouse=True)
def clean_state():
    settings = get_settings()
    previous_api_key = settings.api_key
    previous_require_api_key = settings.require_api_key

    settings.api_key = None
    settings.require_api_key = False
    reset_db()
    yield

    settings.api_key = previous_api_key
    settings.require_api_key = previous_require_api_key


@pytest.fixture
def client():
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client
