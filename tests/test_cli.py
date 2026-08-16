import argparse
from unittest.mock import patch

import cli


def test_cli_list_calls_inventory(monkeypatch):
    class DummyResponse:
        status_code = 200

        def json(self):
            return {"inventory": [{"id": 1, "name": "Test", "brand": "Brand", "quantity": 5, "price": 1.0}]}

    monkeypatch.setattr(cli.requests, "get", lambda url: DummyResponse())
    cli.list_inventory()


def test_cli_view_calls_inventory(monkeypatch):
    class DummyResponse:
        status_code = 200

        def json(self):
            return {"id": 1, "name": "Test", "brand": "Brand", "quantity": 5, "price": 1.0}

    monkeypatch.setattr(cli.requests, "get", lambda url: DummyResponse())
    cli.view_item(1)


def test_cli_add_item_posts_data(monkeypatch):
    class DummyResponse:
        status_code = 201

        def json(self):
            return {"id": 3, "name": "New Product"}

    class DummyArgs:
        name = "New Product"
        brand = "Brand"
        quantity = 10
        price = 2.5
        barcode = None

    monkeypatch.setattr(cli.requests, "post", lambda url, json: DummyResponse())
    cli.add_item(DummyArgs())


def test_cli_update_item_patches_data(monkeypatch):
    class DummyResponse:
        status_code = 200

        def json(self):
            return {"id": 1, "quantity": 15}

    class DummyArgs:
        id = 1
        name = None
        brand = None
        quantity = 15
        price = None
        barcode = None

    monkeypatch.setattr(cli.requests, "patch", lambda url, json: DummyResponse())
    cli.update_item(DummyArgs())


def test_cli_delete_item(monkeypatch):
    class DummyResponse:
        status_code = 200

        def json(self):
            return {"message": "Item deleted."}

    monkeypatch.setattr(cli.requests, "delete", lambda url: DummyResponse())
    cli.delete_item(1)