"""
BNPL Risk Scoring Engine - FastAPI Application
Digital Umbrella Aqrar Challenge
"""

import json
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from engines.scoring import calculate_risk_score
from engines.product_matching import match_products
from engines.explainability import generate_explanation

app = FastAPI(
    title="BNPL Risk Scoring Engine",
    description="AI-based BNPL Risk Scoring and Product Matching for Agricultural Trade Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load_farmers() -> list:
    with open(os.path.join(DATA_DIR, "farmers.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def get_farmer_by_id(farmer_id: str) -> Optional[dict]:
    farmers = load_farmers()
    for farmer in farmers:
        if farmer["farmer_id"] == farmer_id:
            return farmer
    return None


# --- Pydantic Models ---

class RiskScoreRequest(BaseModel):
    farmer_id: str
    region: str
    farm_type: str
    crop_type: str
    farm_size_hectares: float
    years_experience: int
    previous_bnpl_count: int
    previous_bnpl_status: str
    average_monthly_revenue: float
    seasonal_revenue_volatility: str
    land_ownership: bool = False
    has_irrigation: bool = False
    has_bank_loan: bool = False
    requested_amount: float


class ProductMatchRequest(BaseModel):
    farmer_id: str
    crop_type: str
    farm_size_hectares: float
    budget: float
    requested_products: list[str]


# --- Endpoints ---

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")


@app.get("/")
def root():
    """Serve the frontend dashboard."""
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "service": "BNPL Risk Scoring Engine",
        "version": "1.0.0",
        "description": "Digital Umbrella - Aqrar Ticaret Platformasi",
    }


@app.get("/api/v1/farmers")
def list_farmers():
    """List all synthetic farmer profiles."""
    farmers = load_farmers()
    return {"farmers": farmers, "total": len(farmers)}


@app.get("/api/v1/farmers/{farmer_id}")
def get_farmer(farmer_id: str):
    """Get a specific farmer profile."""
    farmer = get_farmer_by_id(farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return farmer


@app.post("/api/v1/risk-score")
def compute_risk_score(request: RiskScoreRequest):
    """Calculate risk score for a farmer."""
    farmer_data = request.model_dump()
    result = calculate_risk_score(farmer_data)
    return result


@app.get("/api/v1/risk-score/{farmer_id}")
def get_risk_score_by_id(farmer_id: str):
    """Calculate risk score for an existing farmer by ID."""
    farmer = get_farmer_by_id(farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    result = calculate_risk_score(farmer)
    return result


@app.post("/api/v1/product-match")
def compute_product_match(request: ProductMatchRequest):
    """Get product recommendations for a farmer."""
    farmer = get_farmer_by_id(request.farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    # Merge request data with farmer data
    farmer_data = {**farmer, "requested_amount": request.budget, "requested_products": request.requested_products}
    score_result = calculate_risk_score(farmer)
    result = match_products(farmer_data, score_result["bnpl_limit"])
    return result


@app.get("/api/v1/product-match/{farmer_id}")
def get_product_match_by_id(farmer_id: str):
    """Get product recommendations for an existing farmer by ID."""
    farmer = get_farmer_by_id(farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    score_result = calculate_risk_score(farmer)
    result = match_products(farmer, score_result["bnpl_limit"])
    return result


@app.get("/api/v1/risk-score/{farmer_id}/explain")
def get_explanation(farmer_id: str):
    """Get detailed explainability report for a farmer's risk score."""
    farmer = get_farmer_by_id(farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    score_result = calculate_risk_score(farmer)
    explanation = generate_explanation(farmer, score_result)
    return explanation


@app.post("/api/v1/risk-score/batch")
def batch_risk_score():
    """Score all farmers in the dataset."""
    farmers = load_farmers()
    results = []
    for farmer in farmers:
        score = calculate_risk_score(farmer)
        results.append(score)
    return {"results": results, "total": len(results)}


@app.get("/api/v1/dashboard/{farmer_id}")
def get_dashboard_data(farmer_id: str):
    """Get all dashboard data for a farmer in a single call."""
    farmer = get_farmer_by_id(farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    score_result = calculate_risk_score(farmer)
    product_result = match_products(farmer, score_result["bnpl_limit"])
    explanation = generate_explanation(farmer, score_result)

    return {
        "farmer": farmer,
        "risk_score": score_result,
        "products": product_result,
        "explanation": explanation,
    }


@app.get("/api/v1/dashboard/all/summary")
def get_all_farmers_summary():
    """Get summary scoring data for all farmers."""
    farmers = load_farmers()
    summaries = []
    for farmer in farmers:
        score = calculate_risk_score(farmer)
        summaries.append({
            "farmer_id": farmer["farmer_id"],
            "name": farmer["name"],
            "region": farmer["region"],
            "farm_type": farmer["farm_type"],
            "crop_type": farmer["crop_type"],
            "risk_score": score["risk_score"],
            "risk_category": score["risk_category"],
            "decision": score["decision"],
            "bnpl_limit": score["bnpl_limit"],
            "installment_months": score["recommended_installment_months"],
        })
    return {"summaries": summaries, "total": len(summaries)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
