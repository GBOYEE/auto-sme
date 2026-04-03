"""CRUD and model validation tests."""
import pytest
from auto_sme.database import Base, get_db
from auto_sme.models import Product, Order, Task, OptOut
from auto_sme.crud import (
    create_product,
    get_products,
    adjust_stock,
    create_order,
    get_orders,
    update_order_status,
    create_task,
    get_tasks,
    opt_out,
    is_opted_out,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

SQLITE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db():
    engine = create_engine(
        SQLITE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool if "sqlite" in SQLITE_URL else None,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
        session.rollback()
    finally:
        session.close()
    engine.dispose()


class TestProductCRUD:
    def test_create_product(self, db):
        prod = create_product(
            db=db,
            name="Test",
            price=9.99,
            unit="lb",
            stock=50,
            low_stock_threshold=5,
        )
        assert prod.id is not None
        assert prod.name == "Test"
        assert prod.stock == 50

    def test_get_products(self, db):
        create_product(db=db, name="P1", price=1.0, unit="unit")
        create_product(db=db, name="P2", price=2.0, unit="unit")
        products = get_products(db)
        assert len(products) >= 2

    def test_adjust_stock(self, db):
        prod = create_product(db=db, name="AdjustTest", price=5.0, unit="unit", stock=10)
        adjusted = adjust_stock(db=db, product_id=prod.id, delta=5)
        assert adjusted.stock == 15
        reduced = adjust_stock(db=db, product_id=prod.id, delta=-3)
        assert reduced.stock == 12

    def test_adjust_stock_not_found(self, db):
        result = adjust_stock(db=db, product_id="nonexistent", delta=5)
        assert result is None


class TestOrderCRUD:
    def test_create_order(self, db):
        # Create product first
        prod = create_product(db=db, name="OrderProduct", price=10.0, unit="unit")
        items = [{"product_id": prod.id, "quantity": 2, "unit_price": 10.0}]
        order = create_order(db=db, customer_phone="+1234567890", items=items)
        assert order.id is not None
        assert order.total_amount == 20.0
        assert order.status == "pending"

    def test_get_orders(self, db):
        create_order(db=db, customer_phone="+1111111111", items=[])
        orders = get_orders(db)
        assert len(orders) >= 1

    def test_update_order_status(self, db):
        order = create_order(db=db, customer_phone="+2222222222", items=[])
        updated = update_order_status(db=db, order_id=order.id, status="completed")
        assert updated.status == "completed"
        assert updated.id == order.id


class TaskCRUD:
    def test_create_task(self, db):
        task = create_task(
            db=db,
            name="Check Inventory",
            cron="0 9 * * *",
            action="inventory_check",
            payload={"low_stock": True},
        )
        assert task.id is not None
        assert task.action == "inventory_check"

    def test_get_tasks(self, db):
        create_task(db=db, name="Task1", cron="0 0 * * *", action="report")
        create_task(db=db, name="Task2", cron="0 1 * * *", action="cleanup")
        tasks = get_tasks(db)
        assert len(tasks) >= 2


class TestOptOut:
    def test_opt_out(self, db):
        opt = opt_out(db=db, phone="+1234567890")
        assert opt.phone == "+1234567890"
        assert opt.opted_out_at is not None

    def test_is_opted_out(self, db):
        opt_out(db=db, phone="+9999999999")
        assert is_opted_out(db=db, phone="+9999999999") is True
        assert is_opted_out(db=db, phone="+0000000000") is False
