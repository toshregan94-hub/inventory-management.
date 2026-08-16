import argparse
import sys
from typing import Any, Dict, Optional

import requests

BASE_URL = "http://127.0.0.1:5000"


def print_error(message: str) -> None:
    print(f"Error: {message}")


def list_inventory() -> None:
    response = requests.get(f"{BASE_URL}/inventory")
    if response.status_code != 200:
        print_error("Failed to fetch inventory.")
        return
    inventory = response.json().get("inventory", [])
    if not inventory:
        print("Inventory is empty.")
        return
    for item in inventory:
        print(f"[{item['id']}] {item['name']} ({item['brand']}) - qty: {item['quantity']} - $ {item['price']}")


def view_item(item_id: int) -> None:
    response = requests.get(f"{BASE_URL}/inventory/{item_id}")
    if response.status_code != 200:
        print_error(response.json().get("error", "Item not found."))
        return
    item = response.json()
    print("Inventory Item Details:")
    for key, value in item.items():
        print(f"{key}: {value}")


def add_item(args: argparse.Namespace) -> None:
    payload: Dict[str, Any] = {
        "name": args.name,
        "brand": args.brand,
        "quantity": args.quantity,
        "price": args.price,
    }
    if args.barcode:
        payload["barcode"] = args.barcode

    response = requests.post(f"{BASE_URL}/inventory", json=payload)
    if response.status_code != 201:
        print_error(response.json().get("error", "Unable to add item."))
        return
    print("Created inventory item:")
    print(response.json())


def update_item(args: argparse.Namespace) -> None:
    payload: Dict[str, Any] = {}
    if args.name:
        payload["name"] = args.name
    if args.brand:
        payload["brand"] = args.brand
    if args.quantity is not None:
        payload["quantity"] = args.quantity
    if args.price is not None:
        payload["price"] = args.price
    if args.barcode:
        payload["barcode"] = args.barcode

    if not payload:
        print_error("Provide at least one field to update.")
        return

    response = requests.patch(f"{BASE_URL}/inventory/{args.id}", json=payload)
    if response.status_code != 200:
        print_error(response.json().get("error", "Update failed."))
        return
    print("Updated inventory item:")
    print(response.json())


def delete_item(item_id: int) -> None:
    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    if response.status_code != 200:
        print_error(response.json().get("error", "Delete failed."))
        return
    print(response.json().get("message"))


def search_external(args: argparse.Namespace) -> None:
    params: Dict[str, str] = {}
    if args.barcode:
        params["barcode"] = args.barcode
    if args.name:
        params["name"] = args.name
    if not params:
        print_error("Provide barcode or name to search.")
        return

    response = requests.get(f"{BASE_URL}/inventory/search", params=params)
    if response.status_code != 200:
        print_error(response.json().get("error", "Search failed."))
        return
    print("External product search result:")
    print(response.json().get("product"))


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inventory management CLI for the Flask API.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="List all inventory items.")

    view_parser = subparsers.add_parser("view", help="View details for a single item.")
    view_parser.add_argument("id", type=int, help="Inventory item ID")

    add_parser = subparsers.add_parser("add", help="Add a new inventory item.")
    add_parser.add_argument("--name", required=True, help="Product name")
    add_parser.add_argument("--brand", default="Unknown", help="Product brand")
    add_parser.add_argument("--quantity", required=True, type=int, help="Quantity in stock")
    add_parser.add_argument("--price", required=True, type=float, help="Item price")
    add_parser.add_argument("--barcode", help="Product barcode for external lookup")

    update_parser = subparsers.add_parser("update", help="Update an existing inventory item.")
    update_parser.add_argument("id", type=int, help="Inventory item ID")
    update_parser.add_argument("--name", help="New product name")
    update_parser.add_argument("--brand", help="New brand")
    update_parser.add_argument("--quantity", type=int, help="New stock quantity")
    update_parser.add_argument("--price", type=float, help="New price")
    update_parser.add_argument("--barcode", help="New barcode to refresh product details")

    delete_parser = subparsers.add_parser("delete", help="Delete an inventory item.")
    delete_parser.add_argument("id", type=int, help="Inventory item ID")

    search_parser = subparsers.add_parser("search", help="Search OpenFoodFacts for product details.")
    search_parser.add_argument("--barcode", help="Barcode to search")
    search_parser.add_argument("--name", help="Product name to search")

    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = create_parser()
    args = parser.parse_args(argv)

    if args.command == "list":
        list_inventory()
    elif args.command == "view":
        view_item(args.id)
    elif args.command == "add":
        add_item(args)
    elif args.command == "update":
        update_item(args)
    elif args.command == "delete":
        delete_item(args.id)
    elif args.command == "search":
        search_external(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except requests.RequestException as exc:
        print_error(f"Unable to reach the API: {exc}")
        sys.exit(1)