from flask import Flask, jsonify, request

from inventory_data import (
    add_inventory_item,
    delete_inventory_item,
    fetch_external_product,
    get_all_items,
    get_item_by_id,
    update_inventory_item,
)

app = Flask(__name__)

@app.route("/inventory", methods=["GET"])
def list_inventory():
    """Fetch all inventory items."""
    return jsonify({"inventory": get_all_items()}), 200

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    """Fetch a single inventory item by ID."""
    item = get_item_by_id(item_id)
    if item is None:
        return jsonify({"error": "Item not found."}), 404
    return jsonify(item), 200

@app.route("/inventory", methods=["POST"])
def create_inventory_item():
    """Add a new inventory item."""
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "JSON payload required."}), 400

    if "name" not in payload or "quantity" not in payload or "price" not in payload:
        return jsonify({"error": "name, quantity, and price are required."}), 400

    item = add_inventory_item(payload)
    return jsonify(item), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def patch_inventory_item(item_id):
    """Update fields for an existing inventory item."""
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "JSON payload required."}), 400

    updated = update_inventory_item(item_id, payload)
    if updated is None:
        return jsonify({"error": "Item not found."}), 404
    return jsonify(updated), 200

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def remove_inventory_item(item_id):
    """Delete an inventory item by ID."""
    deleted = delete_inventory_item(item_id)
    if not deleted:
        return jsonify({"error": "Item not found."}), 404
    return jsonify({"message": "Item deleted."}), 200

@app.route("/inventory/search", methods=["GET"])
def search_external_product():
    """Search the OpenFoodFacts API by barcode or product name."""
    barcode = request.args.get("barcode")
    name = request.args.get("name")

    if not barcode and not name:
        return jsonify({"error": "Provide barcode or name query parameter."}), 400

    product = fetch_external_product(barcode=barcode, name=name)
    if product is None:
        return jsonify({"error": "Product not found or external API unavailable."}), 404

    return jsonify({"status": 1, "product": product}), 200

if __name__ == "__main__":
    app.run(debug=True