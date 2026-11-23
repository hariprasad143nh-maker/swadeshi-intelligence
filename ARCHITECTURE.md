# SWADESHI INTELLIGENCE
## System Architecture (ARCHITECTURE.md)

**Architecture Style:** Modular Monolithic Architecture  
**Backend:** Python 3.11+ with FastAPI  
**Frontend:** React.js + Vite + Tailwind CSS  
**Database:** PostgreSQL (with SQLAlchemy ORM)  
**Data Processing:** Python + Pandas + NumPy  
**Version Control:** Git + GitHub  
**Team Size:** 4 Developers  

---

## 1. Architectural Principles

SWADESHI INTELLIGENCE adopts a **Modular Monolithic** design pattern. All backend capabilities reside within a single repository and FastAPI service, but are separated into distinct, independently owned modules communicating via agreed contracts.

### Why this architecture?
1. **Parallel Development:** 4 developers using different AI tools can work simultaneously on separate directories without merge conflicts.
2. **Zero Deployment Friction:** Avoids microservice network latency, orchestrators, and multi-container complexity for the 2-day hackathon sprint.
3. **Strict Interface Boundaries:** Internal modules communicate using typed schemas and service interfaces rather than raw ad-hoc database queries.
4. **Future Scalability:** Individual modules (`data-engine`, `intelligence-engine`) can easily be split into microservices for production if needed.

---

## 2. High-Level System Architecture

```text
                  DATA SOURCES
                       │
        ┌──────────────┴───────────────┐
        ▼                              ▼
    TradeStat                     Trade Intelligence
     Portal                       & Analytics Portal
  (Dept of Commerce)              (Govt of India)
        │                              │
        └──────────────┬───────────────┘
                       ▼
              DATA INGESTION ENGINE
          (data-engine/collectors)
                       │
                       ▼
             DATA PROCESSING ENGINE
          (data-engine/processors)
                       │
                       ▼
                 POSTGRESQL DB
        ┌──────────────┴───────────────┐
        ▼                              ▼
   IMPORT API                  INTELLIGENCE ENGINE
 (backend/app/routers)        (intelligence-engine/)
        │                     ┌────────┼────────┐
        │                     ▼        ▼        ▼
        │                   Cost  Feasibility  Geo
        │                 Analysis  Scoring  Mapping
        │                     └────────┬────────┘
        │                              ▼
        └──────────────┬───────────────┘
                       ▼
                 FASTAPI REST API
                       │
                       ▼
                REACT DASHBOARD
        (Overview | Explorer | Rankings | Map)
```

---

## 3. Repository Structure & Module Boundaries

```text
swadeshi-intelligence/
├── README.md
├── PROJECT_SPEC.md
├── ARCHITECTURE.md
├── CONTRIBUTING.md
├── AGENTS.md
├── CLAUDE.md
├── .gitignore
├── .env.example
│
├── docs/
│   ├── api-contract.md
│   ├── database-schema.md
│   ├── data-dictionary.md
│   └── integration-rules.md
│
├── backend/                        # OWNED BY MEMBER 1
│   ├── app/
│   │   ├── main.py                 # FastAPI application root & middleware
│   │   ├── database.py             # SQLAlchemy engine & session maker
│   │   ├── config.py               # Settings & environment parser
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   ├── schemas/                # Pydantic schemas (request/response)
│   │   ├── routers/                # API route definitions
│   │   └── services/               # Integration bridge to engines
│   ├── scripts/                    # Database seeding and migration utilities
│   ├── tests/
│   └── requirements.txt
│
├── data-engine/                    # OWNED BY MEMBER 2
│   ├── collectors/                 # Trade data extraction scripts
│   ├── processors/                 # CSV/Excel cleaners & parsers
│   ├── mappings/                   # HS-code to sector taxonomies
│   ├── validators/                 # Data sanity & unit checks
│   ├── tests/
│   └── README.md
│
├── intelligence-engine/            # OWNED BY MEMBER 3
│   ├── cost_analysis/              # Landed vs domestic cost modeling
│   ├── ranking/                    # Opportunity score algorithms
│   ├── feasibility/                # Sectoral viability evaluators
│   ├── recommendations/            # Persona-based recommendations
│   ├── tests/
│   └── README.md
│
└── frontend/                       # OWNED BY MEMBER 4
    ├── src/
    │   ├── components/             # Reusable UI widgets & cards
    │   ├── pages/                  # Route views (Dashboard, Explorer, Rankings)
    │   ├── services/               # Axios API client & mock services
    │   ├── charts/                 # Recharts visualizations
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    └── README.md
```

---

## 4. Team Ownership & Responsibilities

| Role | Member | Primary Focus | Primary Directories |
| :--- | :--- | :--- | :--- |
| **Backend Lead** | Member 1 | FastAPI setup, PostgreSQL models, DB sessions, REST API endpoints, integrating data & intelligence services | `backend/app/`, `docs/api-contract.md` |
| **Data Engineering** | Member 2 | Government import data extraction, cleaning CSVs, HS-code normalization, canonical schema ingestion | `data-engine/`, `backend/scripts/ingest_imports.py` |
| **Intelligence Lead** | Member 3 | Cost comparison formulas, multi-factor opportunity ranking, feasibility metrics, recommendation generators | `intelligence-engine/` |
| **Frontend Lead** | Member 4 | React dashboard, product search/filter, economic comparison charts, geo suitability map, API client | `frontend/` |

---

## 5. Standard Communication Interfaces

To ensure independent development without lockouts, each engine exposes clean Python callable signatures:

### 5.1 Data Engine Interface (`data-engine`)
```python
def normalize_import_record(raw_record: dict) -> dict:
    """Standardizes HS codes, currencies, and volume units."""
    pass

def classify_sector(hs_code: str, product_name: str) -> str:
    """Returns sector: 'agriculture', 'electronics', 'chemicals', 'machinery', or 'other'."""
    pass
```

### 5.2 Intelligence Engine Interface (`intelligence-engine`)
```python
def calculate_cost_advantage(landed_import_cost: float, estimated_domestic_cost: float) -> dict:
    """Returns absolute savings, savings percentage, and viability flag."""
    pass

def compute_opportunity_score(import_volume: float, cost_advantage_pct: float, feasibility_score: float) -> float:
    """Returns 0-100 normalized domestic substitution opportunity score."""
    pass

def generate_recommendations(product_id: int, sector: str) -> list[dict]:
    """Generates tailored recommendations based on target stakeholder."""
    pass
```

---

## 6. Integration & Branching Protocol

1. **`main` Branch:** Protected production branch. Code must be tested and compile cleanly.
2. **Feature Branches:**
   - `feature/backend-core` (Member 1)
   - `feature/data-pipeline` (Member 2)
   - `feature/intelligence-engine` (Member 3)
   - `feature/frontend-dashboard` (Member 4)
3. **Pull Request Protocol:** Before merging into `main`, verify:
   - Database schema modifications conform to `docs/database-schema.md`.
   - API endpoints conform to `docs/api-contract.md`.
   - All unit tests pass.
