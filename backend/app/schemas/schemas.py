from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    database_connected: bool


class ProductBase(BaseModel):
    hs_code: str
    name: str
    sector: str
    description: Optional[str] = None


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    total: int
    page: int
    limit: int
    products: List[ProductResponse]


class CostMetric(BaseModel):
    value: float
    currency: str
    unit: str


class OpportunityItem(BaseModel):
    product_id: int
    hs_code: str
    product_name: str
    sector: str
    opportunity_score: float
    rank: int
    import_cost: CostMetric
    domestic_cost: CostMetric
    potential_savings_percentage: float
    feasibility: str
    confidence: str
    top_production_region: Optional[str] = None


class OpportunitiesResponse(BaseModel):
    opportunities: List[OpportunityItem]


class SectorSummary(BaseModel):
    value_usd: float
    percentage: float


class ImportSummaryResponse(BaseModel):
    financial_year: str
    total_tracked_imports_usd: float
    total_tracked_products: int
    sectors: dict[str, SectorSummary]


class RecommendationItem(BaseModel):
    product_id: int
    name: str
    annual_import_market: str
    action: str
    optimal_states: List[str]
    expected_margin: str


class RecommendationsResponse(BaseModel):
    target_user: str
    total_recommendations: int
    items: List[RecommendationItem]
