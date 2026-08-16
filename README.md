# Inventory Management System

A Flask-based inventory management API with CLI integration and OpenFoodFacts external lookup support.

## Project Overview

This project provides:
- RESTful routes for inventory CRUD operations
- In-memory inventory storage using a Python list
- External product detail lookup via OpenFoodFacts API with a mock fallback
- CLI commands to interact with the API
- Pytest test coverage for endpoints, CLI commands, and external API integration

## API Routes

### GET /inventory
- Input: none
- Output: `{"inventory": [ ... ]}`
- Changes: none
- Triggered when the CLI lists all items.

### GET /inventory/<id>
- Input: item ID in URL path
- Output: single inventory item or 404 error
- Changes: none
- Triggered when the CLI views a specific item.

### POST /inventory
- Input: JSON body with `name`, `quantity`, `price`, optional `brand`, optional `barcode`
- Output: newly created inventory item
- Changes: adds a new item to the in-memory array
- Triggered when the CLI adds a new product.

### PATCH /inventory/<id>
- Input: JSON body with fields to change (`name`, `brand`, `quantity`, `price`, `barcode`)
- Output: updated inventory item or 404 error
- Changes: edits the stored item in the in-memory array
- Triggered when the CLI updates price, stock, or barcode information.

### DELETE /inventory/<id>
- Input: item ID in URL path
- Output: delete confirmation or 404 error
- Changes: removes the item from the in-memory array
- Triggered when the CLI deletes a product.

### GET /inventory/search
- Input: query parameters `barcode` or `name`
- Output: external product details from OpenFoodFacts or mock fallback
- Changes: none
- Triggered when the CLI searches for a product on the external API.

## Setup Instructions

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

Start the Flask application:

```bash
python app.py
```

The API will run at `http://127.0.0.1:5000`.

## CLI Usage

The CLI talks to the running Flask API.

### List all inventory items

```bash
python cli.py list
```

### View a single item

```bash
python cli.py view 1
```

### Add a new product

```bash
python cli.py add --name "Organic Almond Milk" --brand Silk --quantity 20 --price 3.99 --barcode 0001
```

### Update product price or stock

```bash
python cli.py update 1 --price 4.49 --quantity 30
```

### Delete a product

```bash
python cli.py delete 1
```

### Search OpenFoodFacts by barcode or name

```bash
python cli.py search --barcode 0001
python cli.py search --name "Greek Yogurt"
```

## Testing

Run the test suite with:

```bash
pytest
```

## Notes

- Inventory is stored in memory. Restarting the service resets data.
- The `inventory_data.fetch_external_product` function attempts a real OpenFoodFacts API call, and falls back to mock product data on failure.
- The CLI triggers each route directly by making HTTP requests to the Flask API.