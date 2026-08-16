import copy
from typing import Any, Dict, List, Optional

import requests

INVENTORY_ITEMS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "quantity": 25,
        "price": 3.99,
        "barcode": "0001",
        "details": {
            "ingredients_text": "Filtered water, almonds, cane sugar, sea salt, vitamins",
            "labels": "Organic, Vegan",
        },
    },
    {
        "id": 2,
        "name": "Whole Wheat Bread",
        "brand": "Nature's Own",
        "quantity": 40,
        "price": 2.49,
        "barcode": "0002",
        "details": {
            "ingredients_text": "Whole wheat flour, water, yeast, salt, sugar",
            "labels": "Whole Grain",
        },
    },
]

MOCK_OPENFOODFACTS: List[Dict[str, Any]] = [
    {
        "status": 1,
        "product": {
            "code": "0001",
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds, cane sugar, sea salt, vitamins",
            "quantity": "1 L",
            "labels": "Organic, Vegan",
        },
    },
    {
        "status": 1,
        "product": {
            "code": "0002",
            "product_name": "Whole Wheat Bread",
            "brands": "Nature's Own",
            "ingredients_text": "Whole wheat flour, water, yeast, salt, sugar",
            "quantity": "650 g",
            "labels": "Whole Grain",
        },
    },
    {
        "status": 1,
        "product": {
            "code": "0003",
            "product_name": "Greek Yogurt, Low Fat",
            "brands": "Chobani",
            "ingredients_text": "Cultured pasteurized milk, milk protein concentrate, natural flavors",
            "quantity": "500 g",
            "labels": "Low Fat, Protein",
        },
    },
]

def _get_next_id() -> int:
    if not INVENTORY_ITEMS:
        return 1
    return max(item["id"] for item in INVENTORY_ITEMS) + 1


def get_all_items() -> List[Dict[str, Any]]:
    return copy.deepcopy(INVENTORY_ITEMS)


def get_item_by_id(item_id: int) -> Optional[Dict[str, Any]]:
    for item in INVENTORY_ITEMS:
        if item["id"] == item_id:
            return copy.deepcopy(item)
    return None


def add_inventory_item(payload: Dict[str, Any]) -> Dict[str, Any]:
    item_id = _get_next_id()
    barcode = payload.get("barcode")
    name = payload.get("name")
    details = fetch_external_product(barcode=barcode, name=name)
    item = {
        "id": item_id,
        "name": name,
        "brand": payload.get("brand", "Unknown"),
        "quantity": int(payload.get("quantity", 0)),
        "price": float(payload.get("price", 0.0)),
        "barcode": barcode,
        "details": details or {},
    }
    INVENTORY_ITEMS.append(item)
    return copy.deepcopy(item)


def update_inventory_item(item_id: int, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    for item in INVENTORY_ITEMS:
        if item["id"] != item_id:
            continue
        if "name" in payload:
            item["name"] = payload["name"]
        if "brand" in payload:
            item["brand"] = payload["brand"]
        if "quantity" in payload:
            item["quantity"] = int(payload["quantity"])
        if "price" in payload:
            item["price"] = float(payload["price"])
        if "barcode" in payload:
            item["barcode"] = payload["barcode"]
            item["details"] = fetch_external_product(barcode=payload["barcode"], name=item["name"]) or item.get("details", {})
        return copy.deepcopy(item)
    return None


def delete_inventory_item(item_id: int) -> bool:
    for index, item in enumerate(INVENTORY_ITEMS):
        if item["id"] == item_id:
            INVENTORY_ITEMS.pop(index)
            return True
    return False


def _simplify_product(product: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "code": product.get("code"),
        "product_name": product.get("product_name"),
        "brands": product.get("brands"),
        "ingredients_text": product.get("ingredients_text"),
        "quantity": product.get("quantity"),
        "labels": product.get("labels"),
    }


def _mock_search(barcode: Optional[str] = None, name: Optional[str] = None) -> Optional[Dict[str, Any]]:
    if barcode:
        for item in MOCK_OPENFOODFACTS:
            if item["product"]["code"] == barcode:
                return _simplify_product(item["product"])
    if name:
        normalized = name.strip().lower()
        for item in MOCK_OPENFOODFACTS:
            if normalized in item["product"]["product_name"].lower():
                return _simplify_product(item["product"])
    return None


def fetch_external_product(barcode: Optional[str] = None, name: Optional[str] = None) -> Optional[Dict[str, Any]]:
    if barcode:
        url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            payload = response.json()
            if payload.get("status") == 1:
                return _simplify_product(payload.get("product", {}))
        except requests.RequestException:
            pass

    if name:
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        try:
            params = {
                "search_terms": name,
                "search_simple": 1,
                "action": "process",
                "json": 1,
                "page_size": 1,
            }
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            payload = response.json()
            products = payload.get("products", [])
            if products:
                return _simplify_product(products[0])
        except requests.RequestException:
            pass

    return _mock_search(barcode=barcode, name=name)