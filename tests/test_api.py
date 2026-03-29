"""Pytest tests for AutoSME API."""
import pytest
from datetime import datetime
from starlette.testclient import TestClient
from auto_sme.main import create_app
from auto_sme.store import products, orders, tasks, optout_phones

@pytest.fixture(autouse=True)
def clear_store():
    """Reset in-memory store before each test."""
    products.clear()
    orders.clear()
    tasks.clear()
    optout_phones.clear()

client = TestClient(create_app())

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_create_product():
    resp = client.post(
        "/api/v1/inventory",
        json={"name": "Rice", "price": 1.5, "unit": "kg"},
        headers={"X-API-Key": "dev-key"}
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Rice"
    assert data["stock"] == 0
    assert "id" in data
    assert len(products) == 1

def test_list_products():
    resp = client.get("/api/v1/inventory", headers={"X-API-Key": "dev-key"})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_adjust_stock():
    # create product
    create = client.post(
        "/api/v1/inventory",
        json={"name": "Beans", "price": 2.0, "unit": "kg"},
        headers={"X-API-Key": "dev-key"}
    )
    prod_id = create.json()["id"]
    # adjust +50
    resp = client.patch(
        f"/api/v1/inventory/{prod_id}?delta=50",
        headers={"X-API-Key": "dev-key"}
    )
    assert resp.status_code == 200
    assert resp.json()["stock"] == 50
    # negative adjustment -20
    resp = client.patch(
        f"/api/v1/inventory/{prod_id}?delta=-20",
        headers={"X-API-Key": "dev-key"}
    )
    assert resp.json()["stock"] == 30
    # clamp at 0
    resp = client.patch(
        f"/api/v1/inventory/{prod_id}?delta=-100",
        headers={"X-API-Key": "dev-key"}
    )
    assert resp.json()["stock"] == 0

def test_create_order_and_stock_deduction():
    # create product with stock
    client.post(
        "/api/v1/inventory",
        json={"name": "Sugar", "price": 0.8, "unit": "kg", "stock": 100},
        headers={"X-API-Key": "dev-key"}
    )
    assert len(products) == 1
    prod = products[0]
    order = {
        "customer_phone": "+234801234567",
        "items": [
            {"product_id": prod["id"], "product_name": prod["name"], "quantity": 2, "unit_price": prod["price"]}
        ]
    }
    resp = client.post("/api/v1/orders", json=order)
    assert resp.status_code == 201
    data = resp.json()
    assert data["total_amount"] == 1.6
    assert data["status"] == "pending"
    # Check stock deducted via store
    assert products[0]["stock"] == 98

def test_whatsapp_webhook_parsing():
    # create product with stock 50
    client.post(
        "/api/v1/inventory",
        json={"name": "Maize", "price": 0.5, "unit": "kg", "stock": 50},
        headers={"X-API-Key": "dev-key"}
    )
    prod = products[0]
    # Simulate Twilio form POST
    from urllib.parse import urlencode
    form = urlencode({
        "From": "whatsapp:+234801111111",
        "Body": "maize 10"
    })
    resp = client.post(
        "/webhook/whatsapp",
        data=form,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "text/xml; charset=utf-8"
    xml = resp.text
    assert "Order #" in xml
    assert "Total" in xml
    # Verify stock deducted (50 - 10 = 40)
    assert products[0]["stock"] == 40

def test_whatsapp_insufficient_stock():
    client.post(
        "/api/v1/inventory",
        json={"name": "Beans", "price": 2.0, "unit": "kg", "stock": 5},
        headers={"X-API-Key": "dev-key"}
    )
    prod = products[0]
    from urllib.parse import urlencode
    form = urlencode({
        "From": "whatsapp:+234801111111",
        "Body": "beans 10"
    })
    resp = client.post("/webhook/whatsapp", data=form, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert resp.status_code == 200
    assert "Insufficient stock" in resp.text
    # stock unchanged
    assert products[0]["stock"] == 5

def test_whatsapp_optout():
    # opt-out
    from urllib.parse import urlencode
    form = urlencode({
        "From": "whatsapp:+234801111111",
        "Body": "STOP"
    })
    resp = client.post("/webhook/whatsapp", data=form, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert "opted out" in resp.text.lower()
    assert "+234801111111" in optout_phones
    # subsequent message should respect opt-out
    form2 = urlencode({
        "From": "whatsapp:+234801111111",
        "Body": "maize 2"
    })
    resp2 = client.post("/webhook/whatsapp", data=form2, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert "opted out" in resp2.text.lower()
    # stock should not change
    # even if product exists, but order not created
    initial_orders = len(orders)
    assert len(orders) == initial_orders

def test_sales_report():
    # create product
    client.post("/api/v1/inventory", json={"name": "Milk", "price": 1.2, "unit": "L"}, headers={"X-API-Key": "dev-key"})
    prod = products[0]
    # create orders
    client.post("/api/v1/orders", json={"customer_phone": "+123", "items": [{"product_id": prod["id"], "product_name": "Milk", "quantity": 3, "unit_price": 1.2}]})
    client.post("/api/v1/orders", json={"customer_phone": "+456", "items": [{"product_id": prod["id"], "product_name": "Milk", "quantity": 2, "unit_price": 1.2}]})
    # report for today
    today = datetime.utcnow().strftime("%Y-%m-%d")
    resp = client.get(f"/api/v1/reports/sales?start_date={today}&end_date={today}", headers={"X-API-Key": "dev-key"})
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert len(resp.content) > 0