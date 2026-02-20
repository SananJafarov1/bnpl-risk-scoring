"""
BNPL Risk Scoring Engine
Calculates risk scores for farmer BNPL applications using weighted factors.

Scoring thresholds:
  < 50  : REFUSED - loan request denied
  50-65 : Short term, small amount (up to 1500 AZN, 6 months)
  65-85 : Mid-term, moderate amount (up to 3500 AZN, 12 months)
  85+   : Maximum amount, long term (up to 5000 AZN, 18 months)

Range: 500 - 5000 AZN | Max term: 18 months
"""

# Region scores: based on agricultural productivity and infrastructure
REGION_SCORES = {
    "Shirvan": 90,
    "Ganja": 85,
    "Lankaran": 82,
    "Baku": 80,
    "Shamkir": 88,
    "Guba": 78,
    "Sheki": 75,
    "Shamakhi": 80,
    "Qabala": 77,
    "Qakh": 72,
    "Masalli": 74,
    "Barda": 70,
    "Goranboy": 68,
    "Yevlakh": 72,
    "Agdash": 75,
    "Ismayilli": 73,
}

# Farm type scores
FARM_TYPE_SCORES = {
    "grain": 80,
    "vegetable": 75,
    "livestock": 78,
    "greenhouse": 85,
    "mixed": 82,
    "organic": 70,
    "orchard": 80,
}

# Volatility scores
VOLATILITY_SCORES = {
    "low": 95,
    "medium": 70,
    "high": 45,
    "very_high": 20,
}


def calculate_region_score(region: str) -> float:
    return REGION_SCORES.get(region, 65)


def calculate_farm_type_score(farm_type: str) -> float:
    return FARM_TYPE_SCORES.get(farm_type, 60)


def calculate_experience_score(years: int) -> float:
    if years >= 15:
        return 100
    elif years >= 10:
        return 85
    elif years >= 5:
        return 65
    elif years >= 3:
        return 45
    elif years >= 1:
        return 25
    else:
        return 10


def calculate_revenue_score(
    avg_monthly_revenue: float, seasonal_volatility: str
) -> float:
    if avg_monthly_revenue >= 4000:
        revenue_magnitude = 95
    elif avg_monthly_revenue >= 3000:
        revenue_magnitude = 85
    elif avg_monthly_revenue >= 2000:
        revenue_magnitude = 70
    elif avg_monthly_revenue >= 1500:
        revenue_magnitude = 55
    elif avg_monthly_revenue >= 1000:
        revenue_magnitude = 40
    else:
        revenue_magnitude = 25

    volatility = VOLATILITY_SCORES.get(seasonal_volatility, 50)
    return revenue_magnitude * 0.5 + volatility * 0.5


def calculate_bnpl_history_score(count: int, status: str) -> float:
    if count == 0:
        return 40  # No history - neutral-low

    if status == "all_on_time":
        base = 90
    elif "late" in status:
        parts = status.split("_")
        late_count = 0
        on_time_count = 0
        for i, part in enumerate(parts):
            if part == "late":
                late_count += int(parts[i - 1]) if i > 0 and parts[i - 1].isdigit() else 1
            elif part == "on" and i + 1 < len(parts) and parts[i + 1] == "time":
                on_time_count += int(parts[i - 1]) if i > 0 and parts[i - 1].isdigit() else 1

        total = late_count + on_time_count
        if total > 0:
            late_ratio = late_count / total
        else:
            late_ratio = 0.5

        if late_ratio >= 0.5:
            base = 25
        elif late_ratio >= 0.3:
            base = 45
        else:
            base = 65
    elif "on_time" in status:
        base = 80
    else:
        base = 40

    history_bonus = min(count * 2, 10)
    return min(base + history_bonus, 100)


def calculate_land_ownership_score(owns_land: bool) -> float:
    return 90 if owns_land else 35


def calculate_irrigation_score(has_irrigation: bool) -> float:
    return 90 if has_irrigation else 40


def calculate_bank_loan_score(has_loan: bool) -> float:
    # Having an existing bank loan is a negative factor (more debt burden)
    return 30 if has_loan else 85


def calculate_risk_score(farmer_data: dict) -> dict:
    """
    Calculate the overall risk score for a farmer.

    Weighted factors (8 total):
    - Region: 12%
    - Farm Type: 8%
    - Experience: 15%
    - Revenue Pattern: 20%
    - BNPL History: 15%
    - Land Ownership: 12%
    - Irrigation System: 8%
    - Existing Bank Loan: 10%
    """
    region_raw = calculate_region_score(farmer_data["region"])
    farm_type_raw = calculate_farm_type_score(farmer_data["farm_type"])
    experience_raw = calculate_experience_score(farmer_data["years_experience"])
    revenue_raw = calculate_revenue_score(
        farmer_data["average_monthly_revenue"],
        farmer_data["seasonal_revenue_volatility"],
    )
    history_raw = calculate_bnpl_history_score(
        farmer_data["previous_bnpl_count"],
        farmer_data["previous_bnpl_status"],
    )
    land_raw = calculate_land_ownership_score(farmer_data.get("land_ownership", False))
    irrigation_raw = calculate_irrigation_score(farmer_data.get("has_irrigation", False))
    bank_loan_raw = calculate_bank_loan_score(farmer_data.get("has_bank_loan", False))

    weights = {
        "region": 0.12,
        "farm_type": 0.08,
        "experience": 0.15,
        "revenue": 0.20,
        "history": 0.15,
        "land_ownership": 0.12,
        "irrigation": 0.08,
        "bank_loan": 0.10,
    }

    risk_score = (
        region_raw * weights["region"]
        + farm_type_raw * weights["farm_type"]
        + experience_raw * weights["experience"]
        + revenue_raw * weights["revenue"]
        + history_raw * weights["history"]
        + land_raw * weights["land_ownership"]
        + irrigation_raw * weights["irrigation"]
        + bank_loan_raw * weights["bank_loan"]
    )

    risk_score = round(risk_score, 1)

    # New decision thresholds
    if risk_score >= 85:
        # Approved - maximum amount, long term
        decision = "Approved"
        category = "Low"
        bnpl_limit = 5000
        installment_months = 18
        late_probability = max(3, round(100 - risk_score))
    elif risk_score >= 65:
        # Approved - mid-term, moderate amount
        decision = "Approved"
        category = "Medium"
        # Scale from 1500 to 3500 based on score (65-85 range)
        ratio = (risk_score - 65) / 20
        bnpl_limit = round(1500 + ratio * 2000)
        installment_months = round(6 + ratio * 6)  # 6-12 months
        late_probability = max(10, round(100 - risk_score * 0.85))
    elif risk_score >= 50:
        # Approved - short term, small amount
        decision = "Approved"
        category = "High"
        # Scale from 500 to 1500 based on score (50-65 range)
        ratio = (risk_score - 50) / 15
        bnpl_limit = round(500 + ratio * 1000)
        installment_months = round(3 + ratio * 3)  # 3-6 months
        late_probability = max(20, round(100 - risk_score * 0.6))
    else:
        # REFUSED
        decision = "Refused"
        category = "Very High"
        bnpl_limit = 0
        installment_months = 0
        late_probability = max(50, round(100 - risk_score * 0.3))

    confidence = round(60 + min(farmer_data.get("previous_bnpl_count", 0) * 4, 32), 1)

    return {
        "farmer_id": farmer_data["farmer_id"],
        "risk_score": risk_score,
        "risk_category": category,
        "decision": decision,
        "bnpl_limit": bnpl_limit,
        "recommended_installment_months": installment_months,
        "late_payment_probability": late_probability,
        "confidence_level": confidence,
        "explanation": {
            "region_contribution": round(region_raw * weights["region"], 1),
            "farm_type_contribution": round(farm_type_raw * weights["farm_type"], 1),
            "experience_contribution": round(experience_raw * weights["experience"], 1),
            "revenue_contribution": round(revenue_raw * weights["revenue"], 1),
            "history_contribution": round(history_raw * weights["history"], 1),
            "land_ownership_contribution": round(land_raw * weights["land_ownership"], 1),
            "irrigation_contribution": round(irrigation_raw * weights["irrigation"], 1),
            "bank_loan_contribution": round(bank_loan_raw * weights["bank_loan"], 1),
        },
        "raw_scores": {
            "region": region_raw,
            "farm_type": farm_type_raw,
            "experience": experience_raw,
            "revenue": revenue_raw,
            "history": history_raw,
            "land_ownership": land_raw,
            "irrigation": irrigation_raw,
            "bank_loan": bank_loan_raw,
        },
    }
