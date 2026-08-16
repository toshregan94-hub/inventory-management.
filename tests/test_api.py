import copy

import pytest

from app import app
import inventory_data


@pytest.fixture(autouse=True)
def preserve_inventory_state():
    original = copy.deepcopy(inventory_data.INVENTORY_ITEMS)
    yield
    inventory_data.INVENTORY_ITEMS[:] = original


@pytest.fixture
def client():
    app.testing = True
    return app.test_client()


def test_get_all_inventory_items(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert "inventory" in response.json
    assert isinstance(response.json["inventory"], list)


def test_get_single_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.json["id"] == 1


def test_get_missing_item(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404
    assert response.json["error"] == "Item not found."


def test_add_inventory_item(client):
    payload = {"name": "Test Product", "brand": "TestBrand", "quantity": 10, "price": 5.5}
    response = client.post("/inventory", json=payload)
    assert response.status_code == 201
    assert response.json["name"] == "Test Product"
    assert response.json["quantity"] == 10


def test_update_inventory_item(client):
    payload = {"price": 4.99, "quantity": 30}
    response = client.patch("/inventory/1", json=payload)
    assert response.status_code == 200
    assert response.json["price"] == 4.99
    assert response.json["quantity"] == 30


def test_delete_inventory_item(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200
    assert response.json["message"] == "Item deleted."
    assert client.get("/inventory/1").status_code == 404