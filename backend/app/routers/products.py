from fastapi import APIRouter, Query
from typing import Optional
from backend.app.database import get_db_connection
from backend.app.schemas.schemas import ProductListResponse, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=ProductListResponse)
def list_products(
    sector: Optional[str] = Query(None, description="Filter by sector"),
    search: Optional[str] = Query(None, description="Search by name or HS code"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT id, hs_code, name, sector, description FROM products WHERE 1=1"
    params = []

    if sector:
        query += " AND sector = ?"
        params.append(sector.lower())

    if search:
        query += " AND (name LIKE ? OR hs_code LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    # Count total
    count_query = query.replace("SELECT id, hs_code, name, sector, description", "SELECT COUNT(*)")
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]

    # Pagination
    query += " LIMIT ? OFFSET ?"
    params.extend([limit, (page - 1) * limit])

    cursor.execute(query, params)
    rows = cursor.fetchall()

    products = [
        ProductResponse(
            id=row["id"],
            hs_code=row["hs_code"],
            name=row["name"],
            sector=row["sector"],
            description=row["description"],
        )
        for row in rows
    ]

    conn.close()

    return ProductListResponse(
        total=total,
        page=page,
        limit=limit,
        products=products,
    )
