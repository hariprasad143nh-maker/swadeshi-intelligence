from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from backend.app.database import get_db
from backend.app.models.models import Product
from backend.app.schemas.schemas import ProductListResponse, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=ProductListResponse)
def list_products(
    sector: Optional[str] = Query(None, description="Filter by sector"),
    search: Optional[str] = Query(None, description="Search by name or HS code"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Product)
    if sector:
        query = query.filter(Product.sector == sector.lower())
    if search:
        query = query.filter((Product.name.ilike(f"%{search}%")) | (Product.hs_code.ilike(f"%{search}%")))

    total = query.count()
    products = query.offset((page - 1) * limit).limit(limit).all()

    return ProductListResponse(
        total=total,
        page=page,
        limit=limit,
        products=[ProductResponse.model_validate(p) for p in products],
    )
