from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from backend.app.database import get_db
from backend.app.models.models import Product, ProductionAssessment, ProductionRegion
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
    db: Session = Depends(get_db),
):
    query = (
        db.query(Product, ProductionAssessment)
        .join(ProductionAssessment, Product.id == ProductionAssessment.product_id)
    )

    if sector:
        query = query.filter(Product.sector == sector.lower())

    results = query.all()
    opportunities = []

    for rank, (prod, assess) in enumerate(results, start=1):
        imp_cost = float(assess.import_cost)
        dom_cost = float(assess.domestic_cost)
        savings_pct = round(((imp_cost - dom_cost) / imp_cost * 100), 2) if imp_cost > 0 else 0.0

        if min_savings is not None and savings_pct < min_savings:
            continue

        # Get top region
        top_region = db.query(ProductionRegion).filter(ProductionRegion.product_id == prod.id).order_by(ProductionRegion.suitability_score.desc()).first()
        region_str = f"{top_region.district}, {top_region.state}" if top_region else "Pan-India Clusters"

        unit_str = assess.cost_basis or "KG"

        opportunities.append(
            OpportunityItem(
                product_id=prod.id,
                hs_code=prod.hs_code,
                product_name=prod.name,
                sector=prod.sector,
                opportunity_score=float(assess.feasibility_score),
                rank=rank,
                import_cost=CostMetric(value=imp_cost, currency="INR", unit=unit_str),
                domestic_cost=CostMetric(value=dom_cost, currency="INR", unit=unit_str),
                potential_savings_percentage=savings_pct,
                feasibility="high" if assess.feasibility_score >= 80 else "moderate",
                confidence=assess.confidence,
                top_production_region=region_str,
            )
        )

    # Sort by opportunity score descending
    opportunities.sort(key=lambda x: x.opportunity_score, reverse=True)
    # Re-rank
    for i, opp in enumerate(opportunities[:limit], start=1):
        opp.rank = i

    return OpportunitiesResponse(opportunities=opportunities[:limit])


@router.get("/recommendations", response_model=RecommendationsResponse)
def get_recommendations(
    target_user: str = Query("farmer", description="farmer, msme, manufacturer, or policymaker")
):
    # Standard persona recommendation feed
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
    ]

    return RecommendationsResponse(
        target_user=target_user,
        total_recommendations=len(recs),
        items=recs,
    )
