from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.app.database import engine, Base
from backend.app.schemas.schemas import HealthResponse
from backend.app.routers.products import router as products_router
from backend.app.routers.imports import router as imports_router
from backend.app.routers.opportunities import router as opportunities_router

# Auto-create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Swadeshi Intelligence API",
    description="AI-Assisted National Import Substitution & Domestic Production Intelligence Platform",
    version="1.0.0",
)

# CORS setup
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    return HealthResponse(
        status="healthy",
        app_name="Swadeshi Intelligence API",
        version="1.0.0",
        database_connected=True,
    )


# Include domain routers under /api
app.include_router(products_router, prefix="/api")
app.include_router(imports_router, prefix="/api")
app.include_router(opportunities_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
