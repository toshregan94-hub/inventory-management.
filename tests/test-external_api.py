from unittest.mock import patch

import inventory_data


@patch("inventory_data.requests.get")
def test_fetch_external_product_by_barcode(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {
            "code": "0001",
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds",
            "quantity": "1 L",
            "labels": "Organic, Vegan",
        },
    }

    product = inventory_data.fetch_external_product(barcode="0001")
    assert product is not None
    assert product["product_name"] == "Organic Almond Milk"
    assert product["brands"] == "Silk"


@patch("inventory_data.requests.get")
def test_fetch_external_product_by_name(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "products": [
            {
                "code": "0003",
                "product_name": "Greek Yogurt, Low Fat",
                "brands": "Chobani",
                "ingredients_text": "Cultured pasteurized milk",
                "quantity": "500 g",
                "labels": "Low Fat, Protein",
            }
        ]
    }

    product = inventory_data.fetch_external_product(name="Greek Yogurt")
    assert product is not None
    assert product["product_name"] == "Greek Yogurt, Low Fat"
    assert product["brands"] == "Chobani"