from fastapi import APIRouter, Query
from typing import Optional
from backend.app.database import get_db_connection
from backend.app.schemas.schemas import (
    OpportunitiesResponse,
    OpportunityItem,
    CostMetric,
    RecommendationsResponse,
    RecommendationItem,
)

router = APIRouter(tags=["Opportunities & Recommendations"])


@router.get("/opportunities", response_model=OpportunitiesResponse)
def get_opportunities(
    sector: Optional[str] = Query(None, description="Filter by sector"),
    min_savings: Optional[float] = Query(None, description="Minimum potential savings percentage"),
    limit: int = Query(10, ge=1, le=50),
):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        SELECT 
            p.id, p.hs_code, p.name, p.sector,
            a.import_cost, a.domestic_cost, a.feasibility_score, a.confidence, a.cost_basis,
            reg.state, reg.district
        FROM products p
        JOIN production_assessments a ON p.id = a.product_id
        LEFT JOIN production_regions reg ON p.id = reg.product_id
        WHERE 1=1
    """
    params = []

    if sector:
        sql += " AND p.sector = ?"
        params.append(sector.lower())

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    opportunities = []

    for rank, row in enumerate(rows, start=1):
        imp_cost = float(row["import_cost"])
        dom_cost = float(row["domestic_cost"])
        savings_pct = round(((imp_cost - dom_cost) / imp_cost * 100), 2) if imp_cost > 0 else 0.0

        if min_savings is not None and savings_pct < min_savings:
            continue

        region_str = f"{row['district']}, {row['state']}" if row["state"] else "Pan-India Clusters"
        unit_str = row["cost_basis"] or "KG"
        if unit_str.startswith("Per "):
            unit_str = unit_str[4:]

        opportunities.append(
            OpportunityItem(
                product_id=row["id"],
                hs_code=row["hs_code"],
                product_name=row["name"],
                sector=row["sector"],
                opportunity_score=float(row["feasibility_score"]),
                rank=rank,
                import_cost=CostMetric(value=imp_cost, currency="INR", unit=unit_str),
                domestic_cost=CostMetric(value=dom_cost, currency="INR", unit=unit_str),
                potential_savings_percentage=savings_pct,
                feasibility="high" if row["feasibility_score"] >= 80 else "moderate",
                confidence=row["confidence"] or "medium",
                top_production_region=region_str,
            )
        )

    # Sort by opportunity score descending
    opportunities.sort(key=lambda x: x.opportunity_score, reverse=True)
    for i, opp in enumerate(opportunities[:limit], start=1):
        opp.rank = i

    return OpportunitiesResponse(opportunities=opportunities[:limit])


@router.get("/recommendations", response_model=RecommendationsResponse)
def get_recommendations(
    target_user: str = Query("farmer", description="farmer, msme, manufacturer, or policymaker")
):
    recs = [
        RecommendationItem(
            product_id=1,
            name="Fresh Strawberries & Specialty Berries",
            annual_import_market="₹200 Crores",
            action="Adopt climate-controlled polyhouse cultivation & cold-chain clustering",
            optimal_states=["Maharashtra", "Himachal Pradesh", "Meghalaya"],
            expected_margin="35-42%",
        ),
        RecommendationItem(
            product_id=2,
            name="Electronic MLCC Capacitors & Resistor Arrays",
            annual_import_market="₹4,500 Crores",
            action="Establish SMT surface-mount automated component assembly under EMC 2.0 scheme",
            optimal_states=["Tamil Nadu", "Karnataka", "Uttar Pradesh"],
            expected_margin="22-28%",
        ),
        RecommendationItem(
            product_id=3,
            name="Active Pharmaceutical Intermediate: Paracetamol/Amoxicillin Precursors",
            annual_import_market="₹1,800 Crores",
            action="Utilize bulk drug park common effluent facilities and fermentation tanks",
            optimal_states=["Gujarat", "Andhra Pradesh", "Telangana"],
            expected_margin="25-30%",
        ),
        RecommendationItem(
            product_id=4,
            name="Precision Centrifugal & Submersible Industrial Pumps",
            annual_import_market="₹6,200 Crores",
            action="Scale high-efficiency impellers and motor winding units with MSME tooling clusters",
            optimal_states=["Karnataka", "Tamil Nadu", "Gujarat"],
            expected_margin="26-32%",
        ),
    ]

    return RecommendationsResponse(
        target_user=target_user,
        total_recommendations=len(recs),
        items=recs,
    )
