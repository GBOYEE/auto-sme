"""API endpoint tests for AutoSME."""
import pytest
from auto_sme.models import Product, Order, Task, OptOut


class TestHealth:
    def test_health(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "version" in data
        assert "timestamp" in data


class TestMetrics:
    def test_metrics(self, client):
        resp = client.get("/metrics")
        assert resp.status_code == 200
        data = resp.json()
        assert "requests_total" in data
        assert "requests_failed" in data


class TestInventory:
    def test_create_product(self, client, sample_product_data):
        resp = client.post("/api/v1/inventory", json=sample_product_data)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == sample_product_data["name"]
        assert data["price"] == sample_product_data["price"]
        assert "id" in data
        assert "created_at" in data

    def test_list_products(self, client, sample_product_data):
        # Create a product first
        client.post("/api/v1/inventory", json=sample_product_data)
        resp = client.get("/api/v1/inventory")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_adjust_stock(self, client, sample_product_data):
        create_resp = client.post("/api/v1/inventory", json=sample_product_data)
        product_id = create_resp.json()["id"]
        resp = client.patch(f"/api/v1/inventory/{product_id}", params={"delta": 5})
        assert resp.status_code == 200
        data = resp.json()
        assert data["stock"] == sample_product_data["stock"] + 5

    def test_adjust_stock_not_found(self, client):
        resp = client.patch("/api/v1/inventory/nonexistent", params={"delta": 5})
        assert resp.status_code == 404


class TestOrders:
    def test_create_order(self, client, sample_order_data):
        # First create a product to reference
        prod_resp = client.post(
            "/api/v1/inventory",
            json={
                "name": "Order Test Product",
                "price": 10.0,
                "unit": "unit",
                "stock": 100,
            },
        )
        product = prod_resp.json()
        sample_order_data["items"][0]["product_id"] = product["id"]

        resp = client.post("/api/v1/orders", json=sample_order_data)
        assert resp.status_code == 201
        data = resp.json()
        assert data["customer_phone"] == sample_order_data["customer_phone"]
        assert data["status"] == "pending"
        assert "id" in data

    def test_list_orders(self, client, sample_order_data):
        # Create an order first
        client.post("/api/v1/orders", json=sample_order_data)
        resp = client.get("/api/v1/orders")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_update_order_status(self, client, sample_order_data):
        create_resp = client.post("/api/v1/orders", json=sample_order_data)
        order_id = create_resp.json()["id"]
        resp = client.patch(f"/api/v1/orders/{order_id}/status", params={"status": "confirmed"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "confirmed"


class TestTasks:
    def test_create_task(self, client):
        task_data = {
            "name": "Test Task",
            "cron": "0 * * * *",
            "action": "inventory_check",
            "payload": {"threshold": 10},
        }
        resp = client.post("/api/v1/tasks", json=task_data)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == task_data["name"]
        assert data["cron"] == task_data["cron"]
        assert "id" in data

    def test_list_tasks(self, client):
        resp = client.get("/api/v1/tasks")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


class TestReports:
    def test_sales_report_requires_dates(self, client):
        resp = client.get("/api/v1/reports/sales")
        assert resp.status_code == 422  # missing required date params

    def test_sales_report_empty(self, client):
        resp = client.get("/api/v1/reports/sales", params={
            "start_date": "2026-01-01",
            "end_date": "2026-01-31",
        })
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "application/pdf"
