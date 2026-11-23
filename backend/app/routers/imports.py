from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.database import get_db
from backend.app.models.models import ImportRecord, Product
from backend.app.schemas.schemas import ImportSummaryResponse, SectorSummary

router = APIRouter(prefix="/imports", tags=["Imports"])


@router.get("/summary", response_model=ImportSummaryResponse)
def get_import_summary(db: Session = Depends(get_db)):
    # Calculate totals
    total_val = db.query(func.sum(ImportRecord.import_value_usd)).scalar() or 0.0
    total_products = db.query(func.count(Product.id)).scalar() or 0

    # Sector breakdown
    sector_query = (
        db.query(Product.sector, func.sum(ImportRecord.import_value_usd))
        .join(ImportRecord, Product.id == ImportRecord.product_id)
        .group_by(Product.sector)
        .all()
    )

    sectors = {}
    for sector, val in sector_query:
        val_float = float(val or 0.0)
        pct = (val_float / float(total_val) * 100.0) if total_val > 0 else 0.0
        sectors[sector] = SectorSummary(value_usd=val_float, percentage=round(pct, 1))

    return ImportSummaryResponse(
        financial_year="2024-25",
        total_tracked_imports_usd=float(total_val),
        total_tracked_products=total_products,
        sectors=sectors,
    )
