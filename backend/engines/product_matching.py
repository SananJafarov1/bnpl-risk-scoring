"""
Product Matching Engine
Matches agricultural products to farmer profiles based on crop type,
farm size, budget, and seasonal timing.
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_products() -> list:
    with open(os.path.join(DATA_DIR, "products.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def match_products(farmer_data: dict, bnpl_limit: float) -> dict:
    """
    Match products to a farmer profile based on:
    - Crop type compatibility
    - Farm size requirements
    - Budget constraints (BNPL limit)
    - Requested product categories
    """
    products = load_products()
    crop_type = farmer_data["crop_type"]
    farm_size = farmer_data["farm_size_hectares"]
    budget = min(farmer_data.get("requested_amount", bnpl_limit), bnpl_limit)
    requested_categories = farmer_data.get("requested_products", [])

    recommendations = []

    for product in products:
        compatible = product["compatible_crops"]
        if crop_type not in compatible and "all" not in compatible:
            continue

        category = product["category"]
        # Map requested product names to categories
        category_match = False
        for req in requested_categories:
            if req in category or category in req:
                category_match = True
                break
            # Handle special mappings
            if req == "organic_seeds" and category == "seeds":
                category_match = True
            elif req == "organic_fertilizer" and category == "fertilizer":
                category_match = True

        if not category_match:
            continue

        # Calculate quantity and price
        qty_per_ha = product.get("quantity_per_hectare", 0)
        if qty_per_ha > 0:
            estimated_qty = round(qty_per_ha * farm_size, 1)
            estimated_price = round(product["unit_price"] * estimated_qty)
        else:
            # Fixed items (equipment, vet supplies, etc.)
            estimated_qty = 1
            estimated_price = round(product["unit_price"])

        # Calculate match score
        match_score = _calculate_match_score(product, farmer_data)

        # Determine priority
        if category in ["seeds", "animal_feed"]:
            priority = "high"
        elif category in ["fertilizer", "veterinary_supplies"]:
            priority = "high"
        elif category in ["pesticide", "irrigation"]:
            priority = "medium"
        else:
            priority = "low"

        recommendations.append({
            "product_id": product["product_id"],
            "category": category,
            "name": product["name"],
            "name_az": product.get("name_az", ""),
            "estimated_quantity": f"{estimated_qty} {product['unit']}",
            "estimated_price": estimated_price,
            "priority": priority,
            "match_score": match_score,
            "seasonal_timing": product.get("seasonal_timing", ""),
        })

    # Sort by priority then match score
    priority_order = {"high": 0, "medium": 1, "low": 2}
    recommendations.sort(
        key=lambda x: (priority_order.get(x["priority"], 3), -x["match_score"])
    )

    # Trim to budget - fit products within budget, reducing quantities if needed
    total_cost = 0
    budget_recommendations = []
    for rec in recommendations:
        remaining = budget - total_cost
        if remaining <= 0:
            break
        if rec["estimated_price"] <= remaining:
            total_cost += rec["estimated_price"]
            budget_recommendations.append(rec)
        elif remaining >= 100:
            # Include at reduced quantity to fit budget
            ratio = remaining / rec["estimated_price"]
            rec["estimated_price"] = round(remaining)
            rec["estimated_quantity"] = f"~{round(ratio * 100)}% of full quantity"
            total_cost += rec["estimated_price"]
            budget_recommendations.append(rec)

    return {
        "farmer_id": farmer_data["farmer_id"],
        "recommendations": budget_recommendations,
        "total_estimated_cost": total_cost,
    }


def _calculate_match_score(product: dict, farmer_data: dict) -> int:
    """Calculate how well a product matches the farmer profile (0-100)."""
    score = 70  # Base score for compatible product

    crop_type = farmer_data["crop_type"]
    compatible = product["compatible_crops"]

    # Direct crop match bonus
    if crop_type in compatible:
        score += 15

    # Farm size appropriateness
    farm_size = farmer_data["farm_size_hectares"]
    qty_per_ha = product.get("quantity_per_hectare", 0)
    if qty_per_ha > 0:
        total_qty = qty_per_ha * farm_size
        total_cost = product["unit_price"] * total_qty
        if total_cost <= farmer_data.get("requested_amount", 5000):
            score += 10

    # Experience bonus - experienced farmers get better match scores
    if farmer_data.get("years_experience", 0) >= 5:
        score += 5

    return min(score, 100)
