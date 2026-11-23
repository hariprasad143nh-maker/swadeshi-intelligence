from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    hs_code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    sector = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    import_records = relationship("ImportRecord", back_populates="product", cascade="all, delete-orphan")
    assessment = relationship("ProductionAssessment", back_populates="product", uselist=False, cascade="all, delete-orphan")
    regions = relationship("ProductionRegion", back_populates="product", cascade="all, delete-orphan")


class ImportRecord(Base):
    __tablename__ = "import_records"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    financial_year = Column(String(20), nullable=False, index=True)
    country = Column(String(100), default="World")
    import_value_usd = Column(Numeric(18, 2), nullable=False)
    quantity = Column(Numeric(18, 4), nullable=True)
    unit = Column(String(50), nullable=False)
    source = Column(String(255), default="Government Trade Analytics Portal")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="import_records")


class ProductionAssessment(Base):
    __tablename__ = "production_assessments"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    import_cost = Column(Numeric(18, 2), nullable=False)
    domestic_cost = Column(Numeric(18, 2), nullable=False)
    feasibility_score = Column(Numeric(5, 2), nullable=False)
    confidence = Column(String(30), default="medium")
    evidence = Column(Text, nullable=True)
    cost_basis = Column(String(100), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    product = relationship("Product", back_populates="assessment")


class ProductionRegion(Base):
    __tablename__ = "production_regions"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    state = Column(String(100), nullable=False, index=True)
    district = Column(String(100), nullable=False)
    suitability_score = Column(Numeric(5, 2), nullable=False)
    suitability_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="regions")


class Producer(Base):
    __tablename__ = "producers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    producer_type = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    capacity = Column(Numeric(18, 2), nullable=True)
    capacity_unit = Column(String(50), nullable=True)
    contact_email = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Buyer(Base):
    __tablename__ = "buyers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    sector = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    requirement = Column(Text, nullable=True)
    contact_email = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
