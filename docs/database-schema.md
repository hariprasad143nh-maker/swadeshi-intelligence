# Database Schema Specification (docs/database-schema.md)

**Status:** FROZEN — Any modifications require approval from the Backend Lead.  
**Database System:** PostgreSQL (compatible with SQLite for local unit testing).

---

## 1. Entity Relationship Overview

```text
  ┌───────────────────────┐
  │       products        │
  │───────────────────────│
  │ id (PK)               │◄───┐
  │ hs_code (UNIQUE)      │    │
  │ name                  │    │
  │ sector                │    │
  │ description           │    │
  └───────────────────────┘    │
            │                  │
            │ 1:N              │ 1:N
            ▼                  │
  ┌───────────────────────┐    │
  │    import_records     │    │
  │───────────────────────│    │
  │ id (PK)               │    │
  │ product_id (FK) ──────┼────┤
  │ financial_year        │    │
  │ country               │    │
  │ import_value_usd      │    │
  │ quantity              │    │
  │ unit                  │    │
  │ source                │    │
  └───────────────────────┘    │
                               │
            ┌──────────────────┴──────────────────┐
            │ 1:1                                 │ 1:N
            ▼                                     ▼
  ┌─────────────────────────┐           ┌─────────────────────────┐
  │ production_assessments  │           │   production_regions    │
  │─────────────────────────│           │─────────────────────────│
  │ id (PK)                 │           │ id (PK)                 │
  │ product_id (FK)         │           │ product_id (FK)         │
  │ import_cost             │           │ state                   │
  │ domestic_cost           │           │ district                │
  │ feasibility_score       │           │ suitability_score       │
  │ confidence              │           │ suitability_reason      │
  │ evidence                │           └─────────────────────────┘
  │ cost_basis              │
  │ updated_at              │
  └─────────────────────────┘
```

---

## 2. Table Definitions (PostgreSQL DDL)

```sql
-- 1. Master Product Catalog
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    hs_code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(100) NOT NULL, -- 'agriculture', 'electronics', 'chemicals', 'machinery', 'other'
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_hs_code ON products(hs_code);
CREATE INDEX idx_products_sector ON products(sector);

-- 2. Import Transaction Records
CREATE TABLE import_records (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    financial_year VARCHAR(20) NOT NULL, -- e.g., '2024-25'
    country VARCHAR(100) DEFAULT 'World',
    import_value_usd NUMERIC(18,2) NOT NULL,
    quantity NUMERIC(18,4),
    unit VARCHAR(50) NOT NULL,           -- 'KG', 'TONNES', 'PIECES'
    source VARCHAR(255) DEFAULT 'Government Trade Analytics Portal',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, financial_year, country)
);

CREATE INDEX idx_imports_product ON import_records(product_id);
CREATE INDEX idx_imports_year ON import_records(financial_year);

-- 3. Production & Cost Feasibility Assessments
CREATE TABLE production_assessments (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE UNIQUE,
    import_cost NUMERIC(18,2) NOT NULL,        -- Estimated landed cost per unit in INR
    domestic_cost NUMERIC(18,2) NOT NULL,      -- Estimated domestic production cost per unit in INR
    feasibility_score NUMERIC(5,2) NOT NULL,   -- 0.00 to 100.00
    confidence VARCHAR(30) DEFAULT 'medium',   -- 'low', 'medium', 'high'
    evidence TEXT,                             -- Reference to ICAR/ASI/CSIR reports
    cost_basis VARCHAR(100),                   -- e.g., 'Per Metric Ton', 'Per Unit'
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_assessments_product ON production_assessments(product_id);

-- 4. Geospatial Production Regions
CREATE TABLE production_regions (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    suitability_score NUMERIC(5,2) NOT NULL,   -- 0.00 to 100.00
    suitability_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_regions_product ON production_regions(product_id);
CREATE INDEX idx_regions_state ON production_regions(state);

-- 5. Domestic Producers Directory (Provisional for MVP)
CREATE TABLE producers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    producer_type VARCHAR(100) NOT NULL,       -- 'farmer', 'msme', 'industrial_manufacturer'
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    capacity NUMERIC(18,2),
    capacity_unit VARCHAR(50),
    contact_email VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Domestic Buyers & Demand Aggregators (Provisional for MVP)
CREATE TABLE buyers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    requirement TEXT,
    contact_email VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```
