"""Test suite for AutoSME."""
import os
import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- Test database setup ---
TEST_DB = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB.name}"

from auto_sme.database import Base, get_db as original_get_db
from auto_sme.main import create_app
from auto_sme.dependencies import verify_api_key as original_verify

# Create engine and tables
engine = create_engine(f"sqlite:///{TEST_DB.name}", connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    """Test client that bypasses API key check and uses test DB."""
    TestingSessionLocal = sessionmaker(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    def override_verify_api_key():
        return True

    app = create_app()
    app.dependency_overrides[original_get_db] = override_get_db
    app.dependency_overrides[original_verify] = override_verify_api_key
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def sample_product_data():
    return {
        "name": "Test Product",
        "price": 19.99,
        "unit": "kg",
        "stock": 100,
        "low_stock_threshold": 10,
    }


@pytest.fixture
def sample_order_data():
    return {
        "customer_phone": "+1234567890",
        "customer_name": "Test Customer",
        "items": [
            {
                "product_id": "placeholder",
                "product_name": "Test Product",
                "quantity": 2,
                "unit_price": 19.99,
            }
        ],
    }
