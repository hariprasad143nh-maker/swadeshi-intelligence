from fastapi import APIRouter
from backend.app.database import get_db_connection
from backend.app.schemas.schemas import ImportSummaryResponse, SectorSummary

router = APIRouter(prefix="/imports", tags=["Imports"])


@router.get("/summary", response_model=ImportSummaryResponse)
def get_import_summary():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(import_value_usd) FROM import_records")
    total_val = cursor.fetchone()[0] or 0.0

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT p.sector, SUM(r.import_value_usd) as sector_val
        FROM products p
        JOIN import_records r ON p.id = r.product_id
        GROUP BY p.sector
    """)
    rows = cursor.fetchall()

    sectors = {}
    for row in rows:
        sector = row["sector"]
        val_float = float(row["sector_val"] or 0.0)
        pct = (val_float / float(total_val) * 100.0) if total_val > 0 else 0.0
        sectors[sector] = SectorSummary(value_usd=val_float, percentage=round(pct, 1))

    conn.close()

    return ImportSummaryResponse(
        financial_year="2024-25",
        total_tracked_imports_usd=float(total_val),
        total_tracked_products=total_products,
        sectors=sectors,
    )
