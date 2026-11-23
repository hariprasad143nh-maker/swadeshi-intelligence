# API Contract Specification (docs/api-contract.md)

**Status:** FROZEN  
**Base URL:** `http://localhost:8000/api`  
**Protocol:** REST over HTTP / JSON  

---

## Endpoint Summary

| HTTP Method | Route | Responsible Owner | Purpose |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Member 1 | Health check & system diagnostics |
| `GET` | `/products` | Member 1 | Paginated catalog of tracked import products |
| `GET` | `/products/{id}` | Member 1 | Detailed product profile with import history |
| `GET` | `/imports/summary` | Member 1 + 2 | High-level national import dependency indicators |
| `GET` | `/imports/top` | Member 1 + 2 | Top imported commodities ranked by value |
| `GET` | `/opportunities` | Member 1 + 3 | Ranked list of domestic substitution opportunities |
| `GET` | `/opportunities/{id}` | Member 1 + 3 | Deep-dive economic feasibility and cost metrics |
| `GET` | `/recommendations` | Member 1 + 3 | Stakeholder-filtered opportunity feeds |
| `GET` | `/regions/{product_id}` | Member 1 + 3 | Regional/district suitability scores |

---

## Detailed Request & Response Schemas

### 1. `GET /api/health`
**Response (200 OK):**
```json
{
  "status": "healthy",
  "app_name": "Swadeshi Intelligence API",
  "version": "1.0.0",
  "database_connected": true
}
```

---

### 2. `GET /api/products`
**Query Parameters:**
- `sector` (optional, string): Filter by sector (`agriculture`, `electronics`, `chemicals`, `machinery`)
- `search` (optional, string): Search query on name or HS code
- `page` (optional, integer, default: 1)
- `limit` (optional, integer, default: 20)

**Response (200 OK):**
```json
{
  "total": 45,
  "page": 1,
  "limit": 20,
  "products": [
    {
      "id": 1,
      "hs_code": "081010",
      "name": "Fresh Strawberries",
      "sector": "agriculture",
      "description": "Imported high-value commercial berries"
    }
  ]
}
```

---

### 3. `GET /api/imports/summary`
**Response (200 OK):**
```json
{
  "financial_year": "2024-25",
  "total_tracked_imports_usd": 14250000000,
  "total_tracked_products": 120,
  "sectors": {
    "electronics": { "value_usd": 6800000000, "percentage": 47.7 },
    "machinery": { "value_usd": 3900000000, "percentage": 27.4 },
    "chemicals": { "value_usd": 2200000000, "percentage": 15.4 },
    "agriculture": { "value_usd": 1350000000, "percentage": 9.5 }
  }
}
```

---

### 4. `GET /api/opportunities`
**Query Parameters:**
- `sector` (optional, string)
- `min_savings` (optional, float)
- `limit` (optional, integer, default: 10)

**Response (200 OK):**
```json
{
  "opportunities": [
    {
      "product_id": 1,
      "hs_code": "081010",
      "product_name": "Fresh Strawberries",
      "sector": "agriculture",
      "opportunity_score": 87.5,
      "rank": 1,
      "import_cost": {
        "value": 350.00,
        "currency": "INR",
        "unit": "KG"
      },
      "domestic_cost": {
        "value": 220.00,
        "currency": "INR",
        "unit": "KG"
      },
      "potential_savings_percentage": 37.14,
      "feasibility": "high",
      "confidence": "high",
      "top_production_region": "Mahabaleshwar, Maharashtra"
    }
  ]
}
```

---

### 5. `GET /api/opportunities/{id}`
**Response (200 OK):**
```json
{
  "product_id": 1,
  "hs_code": "081010",
  "product_name": "Fresh Strawberries",
  "sector": "agriculture",
  "opportunity_score": 87.5,
  "rank": 1,
  "economic_analysis": {
    "annual_import_value_usd": 24000000,
    "annual_import_quantity": 4800000,
    "unit": "KG",
    "landed_cost_inr": 350.00,
    "estimated_domestic_cost_inr": 220.00,
    "unit_cost_savings_inr": 130.00,
    "savings_percentage": 37.14,
    "estimated_national_savings_inr": 624000000
  },
  "feasibility": {
    "score": 85.00,
    "rating": "high",
    "climate_soil_suitability": "Sub-tropical temperate highland",
    "input_availability": "Indigenous tissue-culture plants available",
    "capital_intensity": "Moderate",
    "evidence": "ICAR Horticulture Technical Bulletin 2024"
  },
  "recommended_stakeholders": [
    "farmers",
    "horticulture_fpos",
    "cold_chain_aggregators"
  ]
}
```

---

### 6. `GET /api/recommendations`
**Query Parameters:**
- `target_user`: `farmer` | `msme` | `manufacturer` | `policymaker`

**Response (200 OK):**
```json
{
  "target_user": "farmer",
  "total_recommendations": 3,
  "items": [
    {
      "product_id": 1,
      "name": "Fresh Strawberries",
      "annual_import_market": "₹200 Crores",
      "action": "Adopt precision polyhouse cultivation",
      "optimal_states": ["Maharashtra", "Himachal Pradesh", "Meghalaya"],
      "expected_margin": "35-40%"
    }
  ]
}
```
