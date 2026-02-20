# BNPL Risk Scoring Engine - Digital Umbrella Aqrar Challenge

## Project Overview

Build an AI-based BNPL (Buy Now Pay Later) Risk Scoring and Product Matching prototype for Digital Umbrella's Agricultural Trade Platform using **ONLY synthetic and dummy data** - no real farmer data.

## Success Criteria

- ✅ Minimum **20 different farm scenarios** with scoring results
- ✅ Product matching with ≥85% scenario accuracy
- ✅ Simple visual scoring dashboard (low-fidelity is acceptable)
- ✅ 100% data safety - NO real data used at any stage
- ✅ API-ready module concept for Aqrar Ticarət Platforması integration

## Deliverables

1. **Prototype Demo Video**
2. **Technical Scoring Logic Document**
3. **Product-Matching Algorithm Structure**
4. **Synthetic Dataset**
5. **UX Mockup/Dashboard**

---

## Technical Architecture

### Tech Stack Recommendation

**Backend:**
- Python (Flask/FastAPI) for API
- Pandas for data processing
- Scikit-learn for ML models (optional)
- Rule-based scoring engine

**Frontend:**
- React with TypeScript
- Recharts or Chart.js for visualization
- Tailwind CSS for styling
- Shadcn/ui components (optional)

**Database:**
- JSON files for synthetic data (no DB needed for prototype)
- In-memory storage for demo

---

## Core Components

### 1. Risk Scoring Engine

**Input Parameters:**
- Region (Baku, Ganja, Shirvan, Lankaran, Sheki, Guba, etc.)
- Farm Type (grain, vegetable, livestock, mixed, greenhouse, organic)
- Crop Type (wheat, potato, tomato, cotton, etc.)
- Farm Size (hectares)
- Years of Experience
- Previous BNPL History (synthetic)
- Seasonal Revenue Pattern
- Product Categories Needed

**Output:**
- Risk Score (0-100, where 100 = lowest risk)
- Risk Category (Low, Medium, High, Very High)
- BNPL Limit (AZN)
- Recommended Installment Period (months)
- Late Payment Probability (%)
- Confidence Level

**Scoring Logic:**

```python
# Weighted Risk Factors
risk_score = (
    region_score * 0.20 +
    farm_type_score * 0.15 +
    experience_score * 0.20 +
    revenue_pattern_score * 0.25 +
    bnpl_history_score * 0.20
)

# BNPL Limit Calculation
if risk_score >= 80:
    bnpl_limit = 2500  # Low risk
    installment_months = 12
elif risk_score >= 60:
    bnpl_limit = 1800  # Medium risk
    installment_months = 9
elif risk_score >= 40:
    bnpl_limit = 1200  # High risk
    installment_months = 6
else:
    bnpl_limit = 500   # Very high risk
    installment_months = 3
```

### 2. Product Matching Engine

**Categories:**
- Seeds (toxum)
- Fertilizers (gübrə)
- Pesticides (pestisid)
- Animal Feed (yem)
- Equipment (avadanlıq)
- Irrigation Systems (suvarma)

**Matching Logic:**
```python
def match_products(farm_profile):
    """
    Match products based on:
    - Crop type compatibility
    - Farm size requirements
    - Seasonal timing
    - Budget constraints
    - Historical purchasing patterns
    """
    recommendations = []
    
    # Rule-based matching
    if farm_profile.crop_type == "wheat":
        recommendations.append({
            "category": "seeds",
            "product": "Winter Wheat Seeds - Premium Grade",
            "quantity": calculate_quantity(farm_profile.farm_size),
            "priority": "high",
            "seasonal_timing": "September-October"
        })
        recommendations.append({
            "category": "fertilizer",
            "product": "NPK Complex Fertilizer",
            "priority": "high"
        })
    
    return recommendations
```

### 3. Explainability Engine

Generate human-readable explanations:

```
Farmer: Rashid Mammadov
Risk Score: 72/100 (Medium Risk)
BNPL Limit: 1,800 AZN
Installment: 9 months

Breakdown:
✓ Region (Shirvan): +18 points (good agricultural zone)
✓ Experience (8 years): +16 points (experienced farmer)
✓ Farm Type (wheat): +12 points (stable crop)
⚠ Revenue Pattern: +14 points (moderate seasonality)
✓ BNPL History: +12 points (2 on-time payments)

Recommended Products:
1. Winter Wheat Seeds (High Priority) - 850 AZN
2. NPK Fertilizer (High Priority) - 600 AZN
3. Pesticide Package (Medium Priority) - 350 AZN
```

---

## 20 Synthetic Farmer Scenarios

### Scenario 1: High-Performing Wheat Farmer
```json
{
  "farmer_id": "F001",
  "name": "Rashid Mammadov",
  "region": "Shirvan",
  "farm_type": "grain",
  "crop_type": "wheat",
  "farm_size_hectares": 45,
  "years_experience": 12,
  "previous_bnpl_count": 3,
  "previous_bnpl_status": "all_on_time",
  "average_monthly_revenue": 2800,
  "seasonal_revenue_volatility": "low",
  "requested_amount": 2200,
  "requested_products": ["seeds", "fertilizer"],
  "expected_risk_score": 85,
  "expected_bnpl_limit": 2500,
  "expected_installment_months": 12
}
```

### Scenario 2: New Potato Farmer
```json
{
  "farmer_id": "F002",
  "name": "Leyla Hasanova",
  "region": "Guba",
  "farm_type": "vegetable",
  "crop_type": "potato",
  "farm_size_hectares": 8,
  "years_experience": 2,
  "previous_bnpl_count": 0,
  "previous_bnpl_status": "no_history",
  "average_monthly_revenue": 1200,
  "seasonal_revenue_volatility": "high",
  "requested_amount": 1500,
  "requested_products": ["seeds", "fertilizer", "pesticide"],
  "expected_risk_score": 45,
  "expected_bnpl_limit": 1200,
  "expected_installment_months": 6
}
```

### Scenario 3: Experienced Livestock Farmer
```json
{
  "farmer_id": "F003",
  "name": "Elvin Aliyev",
  "region": "Lankaran",
  "farm_type": "livestock",
  "crop_type": "dairy_cattle",
  "farm_size_hectares": 25,
  "years_experience": 18,
  "previous_bnpl_count": 5,
  "previous_bnpl_status": "4_on_time_1_late",
  "average_monthly_revenue": 3500,
  "seasonal_revenue_volatility": "low",
  "requested_amount": 1800,
  "requested_products": ["animal_feed", "veterinary_supplies"],
  "expected_risk_score": 75,
  "expected_bnpl_limit": 2500,
  "expected_installment_months": 12
}
```

### Scenario 4: Greenhouse Tomato Producer
```json
{
  "farmer_id": "F004",
  "name": "Nigar Ismayilova",
  "region": "Baku",
  "farm_type": "greenhouse",
  "crop_type": "tomato",
  "farm_size_hectares": 2,
  "years_experience": 5,
  "previous_bnpl_count": 2,
  "previous_bnpl_status": "all_on_time",
  "average_monthly_revenue": 4200,
  "seasonal_revenue_volatility": "low",
  "requested_amount": 2000,
  "requested_products": ["seeds", "fertilizer", "irrigation"],
  "expected_risk_score": 78,
  "expected_bnpl_limit": 1800,
  "expected_installment_months": 9
}
```

### Scenario 5: Struggling Cotton Farmer
```json
{
  "farmer_id": "F005",
  "name": "Vugar Huseynov",
  "region": "Barda",
  "farm_type": "grain",
  "crop_type": "cotton",
  "farm_size_hectares": 60,
  "years_experience": 7,
  "previous_bnpl_count": 3,
  "previous_bnpl_status": "2_late_1_on_time",
  "average_monthly_revenue": 1800,
  "seasonal_revenue_volatility": "very_high",
  "requested_amount": 2500,
  "requested_products": ["seeds", "pesticide", "fertilizer"],
  "expected_risk_score": 38,
  "expected_bnpl_limit": 500,
  "expected_installment_months": 3
}
```

### Scenario 6: Mixed Farm - High Diversification
```json
{
  "farmer_id": "F006",
  "name": "Kamran Jafarov",
  "region": "Ganja",
  "farm_type": "mixed",
  "crop_type": "wheat_vegetables_livestock",
  "farm_size_hectares": 35,
  "years_experience": 15,
  "previous_bnpl_count": 6,
  "previous_bnpl_status": "all_on_time",
  "average_monthly_revenue": 3200,
  "seasonal_revenue_volatility": "medium",
  "requested_amount": 2100,
  "requested_products": ["seeds", "fertilizer", "animal_feed"],
  "expected_risk_score": 82,
  "expected_bnpl_limit": 2500,
  "expected_installment_months": 12
}
```

### Scenario 7: Organic Farm Startup
```json
{
  "farmer_id": "F007",
  "name": "Aynur Mammadova",
  "region": "Sheki",
  "farm_type": "organic",
  "crop_type": "vegetables_mixed",
  "farm_size_hectares": 6,
  "years_experience": 1,
  "previous_bnpl_count": 0,
  "previous_bnpl_status": "no_history",
  "average_monthly_revenue": 800,
  "seasonal_revenue_volatility": "high",
  "requested_amount": 1000,
  "requested_products": ["organic_seeds", "organic_fertilizer"],
  "expected_risk_score": 42,
  "expected_bnpl_limit": 1200,
  "expected_installment_months": 6
}
```

### Scenario 8: Large-Scale Wheat Operation
```json
{
  "farmer_id": "F008",
  "name": "Rafiq Rasulov",
  "region": "Shamkir",
  "farm_type": "grain",
  "crop_type": "wheat",
  "farm_size_hectares": 120,
  "years_experience": 22,
  "previous_bnpl_count": 8,
  "previous_bnpl_status": "all_on_time",
  "average_monthly_revenue": 5800,
  "seasonal_revenue_volatility": "low",
  "requested_amount": 2400,
  "requested_products": ["seeds", "fertilizer", "equipment"],
  "expected_risk_score": 92,
  "expected_bnpl_limit": 2500,
  "expected_installment_months": 12
}
```

### Scenario 9: Small Cucumber Farm
```json
{
  "farmer_id": "F009",
  "name": "Sevinj Ahmadova",
  "region": "Masalli",
  "farm_type": "vegetable",
  "crop_type": "cucumber",
  "farm_size_hectares": 4,
  "years_experience": 3,
  "previous_bnpl_count": 1,
  "previous_bnpl_status": "1_on_time",
  "average_monthly_revenue": 1400,
  "seasonal_revenue_volatility": "medium",
  "requested_amount": 800,
  "requested_products": ["seeds", "fertilizer"],
  "expected_risk_score": 58,
  "expected_bnpl_limit": 1800,
  "expected_installment_months": 9
}
```

### Scenario 10: Poultry Farm
```json
{
  "farmer_id": "F010",
  "name": "Tural Tagiyev",
  "region": "Ganja",
  "farm_type": "livestock",
  "crop_type": "poultry",
  "farm_size_hectares": 3,
  "years_experience": 6,
  "previous_bnpl_count": 4,
  "previous_bnpl_status": "all_on_time",
  "average_monthly_revenue": 2200,
  "seasonal_revenue_volatility": "low",
  "requested_amount": 1500,
  "requested_products": ["animal_feed", "veterinary_supplies"],
  "expected_risk_score": 71,
  "expected_bnpl_limit": 1800,
  "expected_installment_months": 9
}
```

### Scenario 11: Apple Orchard
```json
{
  "farmer_id": "F011",
  "name": "Murad Guliyev",
  "region": "Guba",
  "farm_type": "orchard",
  "crop_type": "apple",
  "farm_size_hectares": 15,
  "years_experience": 10,
  "previous_bnpl_count": 3,
  "previous_bnpl_status": "2_on_time_1_late",
  "average_monthly_revenue": 2600,
  "seasonal_revenue_volatility": "medium",
  "requested_amount": 1700,
  "requested_products": ["fertilizer", "pesticide", "irrigation"],
  "expected_risk_score": 68,
  "expected_bnpl_limit": 1800,
  "expected_installment_months": 9
}
```

### Scenario 12: First-Time Barley Farmer
```json
{
  "farmer_id": "F012",
  "name": "Zemfira Huseynova",
  "region": "Goranboy",
  "farm_type": "grain",
  "crop_type": "barley",
  "farm_size_hectares": 18,
  "years_experience": 1,
  "previous_bnpl_count": 0,
  "previous_bnpl_status": "no_history",
  "average_monthly_revenue": 900,
  "seasonal_revenue_volatility": "high",
  "requested_amount": 1300,
  "requested_products": ["seeds", "fertilizer"],
  "expected_risk_score": 40,
  "expected_bnpl_limit": 1200,
  "expected_installment_months": 6
}
```

### Scenario 13: Established Vineyard
```json
{
  "farmer_id": "F013",
  "name": "Eldar Mammadov",
  "region": "Shamakhi",
  "farm_type": "orchard",
  "crop_type": "grapes",
  "farm_size_hectares": 22,
  "years_experience": 16,
  "previous_bnpl_count": 7,
  "previous_bnpl_status": "all_on_time",
  "average_monthly_revenue": 3400,
  "seasonal_revenue_volatility": "low",
  "requested_amount": 2000,
  "requested_products": ["fertilizer", "pesticide"],
  "expected_risk_score": 86,
  "expected_bnpl_limit": 2500,
  "expected_installment_months": 12
}
```

### Scenario 14: Pepper Production
```json
{
  "farmer_id": "F014",
  "name": "Gulnara Rzayeva",
  "region": "Lankaran",
  "farm_type": "vegetable",
  "crop_type": "pepper",
  "farm_size_hectares": 5,
  "years_experience": 4,
  "previous_bnpl_count": 2,
  "previous_bnpl_status": "1_on_time_1_late",
  "average_monthly_revenue": 1600,
  "seasonal_revenue_volatility": "high",
  "requested_amount": 1100,
  "requested_products": ["seeds", "fertilizer", "pesticide"],
  "expected_risk_score": 52,
  "expected_bnpl_limit": 1200,
  "expected_installment_months": 6
}
```

### Scenario 15: Sheep Farm
```json
{
  "farmer_id": "F015",
  "name": "Ramiz Abdullayev",
  "region": "Qakh",
  "farm_type": "livestock",
  "crop_type": "sheep",
  "farm_size_hectares": 40,
  "years_experience": 13,
  "previous_bnpl_count": 5,
  "previous_bnpl_status": "4_on_time_1_late",
  "average_monthly_revenue": 2900,
  "seasonal_revenue_volatility": "medium",
  "requested_amount": 1900,
  "requested_products": ["animal_feed", "veterinary_supplies"],
  "expected_risk_score": 72,
  "expected_bnpl_limit": 1800,
  "expected_installment_months": 9
}
```

### Scenario 16: Sunflower Farm - Risky Profile
```json
{
  "farmer_id": "F016",
  "name": "Farid Nabiyev",
  "region": "Yevlakh",
  "farm_type": "grain",
  "crop_type": "sunflower",
  "farm_size_hectares": 35,
  "years_experience": 4,
  "previous_bnpl_count": 2,
  "previous_bnpl_status": "2_late",
  "average_monthly_revenue": 1300,
  "seasonal_revenue_volatility": "very_high",
  "requested_amount": 2000,
  "requested_products": ["seeds", "fertilizer"],
  "expected_risk_score": 32,
  "expected_bnpl_limit": 500,
  "expected_installment_months": 3
}
```

### Scenario 17: Premium Greenhouse Flowers
```json
{
  "farmer_id": "F017",
  "name": "Aysel Mammadova",
  "region": "Baku",
  "farm_type": "greenhouse",
  "crop_type": "flowers",
  "farm_size_hectares": 1,
  "years_experience": 7,
  "previous_bnpl_count": 3,
  "previous_bnpl_status": "all_on_time",
  "average_monthly_revenue": 3800,
  "seasonal_revenue_volatility": "low",
  "requested_amount": 1600,
  "requested_products": ["seeds", "fertilizer", "equipment"],
  "expected_risk_score": 79,
  "expected_bnpl_limit": 1800,
  "expected_installment_months": 9
}
```

### Scenario 18: Corn Production
```json
{
  "farmer_id": "F018",
  "name": "Sahib Hasanov",
  "region": "Agdash",
  "farm_type": "grain",
  "crop_type": "corn",
  "farm_size_hectares": 28,
  "years_experience": 9,
  "previous_bnpl_count": 4,
  "previous_bnpl_status": "3_on_time_1_late",
  "average_monthly_revenue": 2100,
  "seasonal_revenue_volatility": "medium",
  "requested_amount": 1600,
  "requested_products": ["seeds", "fertilizer"],
  "expected_risk_score": 64,
  "expected_bnpl_limit": 1800,
  "expected_installment_months": 9
}
```

### Scenario 19: Hazelnut Orchard
```json
{
  "farmer_id": "F019",
  "name": "Nazim Ibrahimov",
  "region": "Qabala",
  "farm_type": "orchard",
  "crop_type": "hazelnut",
  "farm_size_hectares": 12,
  "years_experience": 11,
  "previous_bnpl_count": 6,
  "previous_bnpl_status": "all_on_time",
  "average_monthly_revenue": 2800,
  "seasonal_revenue_volatility": "low",
  "requested_amount": 1800,
  "requested_products": ["fertilizer", "pesticide"],
  "expected_risk_score": 81,
  "expected_bnpl_limit": 2500,
  "expected_installment_months": 12
}
```

### Scenario 20: Cabbage Farm - Medium Risk
```json
{
  "farmer_id": "F020",
  "name": "Gunay Aliyeva",
  "region": "Ismayilli",
  "farm_type": "vegetable",
  "crop_type": "cabbage",
  "farm_size_hectares": 7,
  "years_experience": 5,
  "previous_bnpl_count": 2,
  "previous_bnpl_status": "2_on_time",
  "average_monthly_revenue": 1700,
  "seasonal_revenue_volatility": "medium",
  "requested_amount": 1200,
  "requested_products": ["seeds", "fertilizer", "pesticide"],
  "expected_risk_score": 62,
  "expected_bnpl_limit": 1800,
  "expected_installment_months": 9
}
```

---

## API Endpoints Specification

### 1. Calculate Risk Score
```
POST /api/v1/risk-score
```

**Request Body:**
```json
{
  "farmer_id": "F001",
  "region": "Shirvan",
  "farm_type": "grain",
  "crop_type": "wheat",
  "farm_size_hectares": 45,
  "years_experience": 12,
  "previous_bnpl_count": 3,
  "previous_bnpl_status": "all_on_time",
  "average_monthly_revenue": 2800,
  "seasonal_revenue_volatility": "low",
  "requested_amount": 2200
}
```

**Response:**
```json
{
  "farmer_id": "F001",
  "risk_score": 85,
  "risk_category": "Low",
  "bnpl_limit": 2500,
  "recommended_installment_months": 12,
  "late_payment_probability": 8,
  "confidence_level": 92,
  "explanation": {
    "region_contribution": 18,
    "farm_type_contribution": 13,
    "experience_contribution": 20,
    "revenue_contribution": 22,
    "history_contribution": 12
  }
}
```

### 2. Get Product Recommendations
```
POST /api/v1/product-match
```

**Request Body:**
```json
{
  "farmer_id": "F001",
  "crop_type": "wheat",
  "farm_size_hectares": 45,
  "budget": 2200,
  "requested_products": ["seeds", "fertilizer"]
}
```

**Response:**
```json
{
  "farmer_id": "F001",
  "recommendations": [
    {
      "product_id": "P001",
      "category": "seeds",
      "name": "Winter Wheat Seeds - Premium Grade",
      "estimated_quantity": "225 kg",
      "estimated_price": 850,
      "priority": "high",
      "match_score": 95,
      "seasonal_timing": "September-October"
    },
    {
      "product_id": "P042",
      "category": "fertilizer",
      "name": "NPK Complex Fertilizer 15-15-15",
      "estimated_quantity": "1200 kg",
      "estimated_price": 600,
      "priority": "high",
      "match_score": 92
    }
  ],
  "total_estimated_cost": 1450,
  "remaining_budget": 750
}
```

### 3. Batch Score Multiple Farmers
```
POST /api/v1/risk-score/batch
```

### 4. Get Explainability Report
```
GET /api/v1/risk-score/{farmer_id}/explain
```

---

## Dashboard Requirements

### Main Dashboard Components:

1. **Risk Score Gauge** (0-100)
2. **Risk Category Badge** (Color-coded)
3. **BNPL Limit Display**
4. **Installment Recommendation**
5. **Late Payment Probability** (Percentage bar)
6. **Risk Factor Breakdown** (Horizontal bar chart)
7. **Product Recommendations Table**
8. **Explainability Panel** (Expandable)

### Mockup Structure:

```
┌─────────────────────────────────────────────────────────┐
│  Digital Umbrella - BNPL Risk Scoring Engine            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Farmer: Rashid Mammadov (F001)                         │
│  Region: Shirvan | Farm Type: Grain (Wheat)             │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Risk Score   │  │  BNPL Limit  │  │  Installment │  │
│  │     85       │  │   2,500 AZN  │  │   12 months  │  │
│  │  ┌────────┐  │  │              │  │              │  │
│  │  │ ██████ │  │  │   [LOW RISK] │  │              │  │
│  │  └────────┘  │  │              │  │              │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                          │
│  Late Payment Probability: 8%                           │
│  ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░                    │
│                                                          │
│  Risk Factor Breakdown:                                 │
│  Region         ████████████████░░░░  18/20             │
│  Experience     ████████████████████  20/20             │
│  Revenue        ██████████████████░░  22/25             │
│  BNPL History   ████████████░░░░░░░░  12/20             │
│  Farm Type      █████████████░░░░░░░  13/15             │
│                                                          │
│  Recommended Products:                                  │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Product              Category  Price   Priority    │ │
│  │ Winter Wheat Seeds   Seeds     850 AZN   High      │ │
│  │ NPK Fertilizer       Fertilizer 600 AZN  High      │ │
│  │ Pesticide Package    Pesticide  350 AZN  Medium    │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  [View Full Explanation] [Export Report]                │
└─────────────────────────────────────────────────────────┘
```

---

## Implementation Steps

### Phase 1: Backend Setup
1. Create synthetic dataset (20 farmer profiles in JSON)
2. Implement risk scoring algorithm
3. Build product matching engine
4. Create explainability function
5. Set up API endpoints (Flask/FastAPI)

### Phase 2: Frontend Dashboard
1. Set up React project with TypeScript
2. Create dashboard layout
3. Build risk score visualization components
4. Implement product recommendation table
5. Add explainability panel

### Phase 3: Integration & Testing
1. Connect frontend to backend API
2. Test all 20 scenarios
3. Validate product matching accuracy
4. Generate explainability reports

### Phase 4: Documentation & Demo
1. Create technical documentation
2. Record demo video
3. Prepare presentation materials

---

## Evaluation Criteria Alignment

| Criterion | Weight | How to Achieve |
|-----------|--------|----------------|
| Scoring logic & accuracy | 35% | - Well-documented algorithm<br>- 20+ scenarios tested<br>- Clear risk categorization |
| Data-safety principle | 25% | - 100% synthetic data<br>- No real farmer info<br>- Document data generation |
| Innovation & technical architecture | 20% | - Clean API design<br>- Explainability engine<br>- Product matching AI |
| Visualization & dashboard quality | 10% | - Intuitive UI/UX<br>- Clear data presentation<br>- Interactive elements |
| Team qualification | 10% | - Technical skills demo<br>- Code quality<br>- Documentation |

---

## Key Innovation Points

1. **Explainability First**: Every risk score comes with clear reasoning
2. **Product-Farmer Matching**: AI suggests optimal products based on profile
3. **Synthetic Data Excellence**: Realistic scenarios without privacy concerns
4. **API-Ready**: Plug-and-play integration with Aqrar platform
5. **Azerbaijani Context**: Region-specific, crop-specific logic

---

## Next Steps

1. Clone/create project repository
2. Set up backend (Python + Flask/FastAPI)
3. Generate synthetic dataset JSON
4. Implement scoring engine
5. Build React dashboard
6. Test with 20 scenarios
7. Create demo video
8. Prepare documentation

---

## Questions to Consider

- Should we use ML model (scikit-learn) or pure rule-based?
- Do you want multilingual support (Azerbaijani + English)?
- Should we add a farmer comparison feature?
- Do you need export to PDF/Excel functionality?

---

Good luck with the challenge! 🚀
