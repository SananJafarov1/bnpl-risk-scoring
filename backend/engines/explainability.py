"""
Explainability Engine
Generates human-readable explanations for risk scoring decisions.
"""


def generate_explanation(farmer_data: dict, score_result: dict) -> dict:
    """Generate a detailed, human-readable explanation of the risk score."""
    explanation = score_result["explanation"]
    raw = score_result["raw_scores"]

    factors = []

    # Region factor
    region = farmer_data["region"]
    region_score = raw["region"]
    if region_score >= 80:
        region_desc = "excellent agricultural zone"
    elif region_score >= 70:
        region_desc = "good agricultural zone"
    else:
        region_desc = "moderate agricultural zone"

    factors.append({
        "factor": "Region",
        "value": region,
        "raw_score": region_score,
        "weighted_contribution": explanation["region_contribution"],
        "max_contribution": 12.0,
        "icon": "check" if region_score >= 70 else "warning",
        "description": f"Region ({region}): +{explanation['region_contribution']} points ({region_desc})",
    })

    # Experience factor
    years = farmer_data["years_experience"]
    exp_score = raw["experience"]
    if years >= 10:
        exp_desc = "highly experienced farmer"
    elif years >= 5:
        exp_desc = "experienced farmer"
    elif years >= 3:
        exp_desc = "developing farmer"
    else:
        exp_desc = "new farmer"

    factors.append({
        "factor": "Experience",
        "value": f"{years} years",
        "raw_score": exp_score,
        "weighted_contribution": explanation["experience_contribution"],
        "max_contribution": 15.0,
        "icon": "check" if exp_score >= 65 else "warning",
        "description": f"Experience ({years} years): +{explanation['experience_contribution']} points ({exp_desc})",
    })

    # Revenue factor
    revenue = farmer_data["average_monthly_revenue"]
    volatility = farmer_data["seasonal_revenue_volatility"]
    rev_score = raw["revenue"]
    if volatility == "low":
        vol_desc = "stable income"
    elif volatility == "medium":
        vol_desc = "moderate seasonality"
    else:
        vol_desc = "high seasonality risk"

    factors.append({
        "factor": "Revenue Pattern",
        "value": f"{revenue} AZN/month ({volatility} volatility)",
        "raw_score": rev_score,
        "weighted_contribution": explanation["revenue_contribution"],
        "max_contribution": 20.0,
        "icon": "check" if rev_score >= 60 else "warning",
        "description": f"Revenue Pattern: +{explanation['revenue_contribution']} points ({vol_desc})",
    })

    # BNPL history factor
    bnpl_count = farmer_data["previous_bnpl_count"]
    bnpl_status = farmer_data["previous_bnpl_status"]
    hist_score = raw["history"]
    if bnpl_count == 0:
        hist_desc = "no previous BNPL history"
    elif bnpl_status == "all_on_time":
        hist_desc = f"{bnpl_count} on-time payments"
    else:
        hist_desc = f"mixed payment record ({bnpl_status.replace('_', ' ')})"

    factors.append({
        "factor": "BNPL History",
        "value": bnpl_status.replace("_", " "),
        "raw_score": hist_score,
        "weighted_contribution": explanation["history_contribution"],
        "max_contribution": 15.0,
        "icon": "check" if hist_score >= 60 else "warning",
        "description": f"BNPL History: +{explanation['history_contribution']} points ({hist_desc})",
    })

    # Land Ownership factor
    owns_land = farmer_data.get("land_ownership", False)
    land_score = raw["land_ownership"]
    land_desc = "owns the farmland" if owns_land else "rents / does not own farmland"

    factors.append({
        "factor": "Land Ownership",
        "value": "Owner" if owns_land else "Not Owner",
        "raw_score": land_score,
        "weighted_contribution": explanation["land_ownership_contribution"],
        "max_contribution": 12.0,
        "icon": "check" if owns_land else "warning",
        "description": f"Land Ownership: +{explanation['land_ownership_contribution']} points ({land_desc})",
    })

    # Irrigation factor
    has_irrigation = farmer_data.get("has_irrigation", False)
    irr_score = raw["irrigation"]
    irr_desc = "has irrigation system" if has_irrigation else "no irrigation system"

    factors.append({
        "factor": "Irrigation System",
        "value": "Yes" if has_irrigation else "No",
        "raw_score": irr_score,
        "weighted_contribution": explanation["irrigation_contribution"],
        "max_contribution": 8.0,
        "icon": "check" if has_irrigation else "warning",
        "description": f"Irrigation System: +{explanation['irrigation_contribution']} points ({irr_desc})",
    })

    # Bank Loan factor
    has_loan = farmer_data.get("has_bank_loan", False)
    loan_score = raw["bank_loan"]
    loan_desc = "has existing bank loan (debt burden)" if has_loan else "no existing bank loan"

    factors.append({
        "factor": "Bank Loan",
        "value": "Has Loan" if has_loan else "No Loan",
        "raw_score": loan_score,
        "weighted_contribution": explanation["bank_loan_contribution"],
        "max_contribution": 10.0,
        "icon": "warning" if has_loan else "check",
        "description": f"Bank Loan: +{explanation['bank_loan_contribution']} points ({loan_desc})",
    })

    # Farm type factor
    farm_type = farmer_data["farm_type"]
    ft_score = raw["farm_type"]
    factors.append({
        "factor": "Farm Type",
        "value": farm_type.replace("_", " ").title(),
        "raw_score": ft_score,
        "weighted_contribution": explanation["farm_type_contribution"],
        "max_contribution": 8.0,
        "icon": "check" if ft_score >= 75 else "warning",
        "description": f"Farm Type ({farm_type}): +{explanation['farm_type_contribution']} points",
    })

    # Build summary
    score = score_result["risk_score"]
    decision = score_result["decision"]
    category = score_result["risk_category"]

    if decision == "Refused":
        summary = (
            f"{farmer_data['name']} - LOAN REQUEST REFUSED. Risk score {score}/100 is below the minimum threshold of 50. "
            f"Multiple risk factors identified including "
            + (("no land ownership, " if not owns_land else ""))
            + (("existing bank loan, " if has_loan else ""))
            + (("no irrigation system, " if not has_irrigation else ""))
            + f"resulting in too high a risk for BNPL approval."
        )
    elif category == "Low":
        summary = (
            f"{farmer_data['name']} presents a low-risk profile with a score of {score}/100. "
            f"Strong indicators across all factors. "
            f"APPROVED for maximum BNPL limit of {score_result['bnpl_limit']:,} AZN with {score_result['recommended_installment_months']}-month term."
        )
    elif category == "Medium":
        summary = (
            f"{farmer_data['name']} presents a moderate-risk profile with a score of {score}/100. "
            f"Positive indicators balanced with some areas of concern. "
            f"APPROVED for BNPL limit of {score_result['bnpl_limit']:,} AZN with {score_result['recommended_installment_months']}-month term."
        )
    else:
        summary = (
            f"{farmer_data['name']} presents a higher-risk profile with a score of {score}/100. "
            f"Limited history or concerning indicators suggest caution. "
            f"APPROVED for reduced BNPL limit of {score_result['bnpl_limit']:,} AZN with {score_result['recommended_installment_months']}-month short term."
        )

    return {
        "farmer_id": farmer_data["farmer_id"],
        "farmer_name": farmer_data["name"],
        "risk_score": score,
        "risk_category": category,
        "decision": decision,
        "summary": summary,
        "factors": factors,
        "bnpl_limit": score_result["bnpl_limit"],
        "installment_months": score_result["recommended_installment_months"],
        "late_payment_probability": score_result["late_payment_probability"],
        "confidence_level": score_result["confidence_level"],
    }
