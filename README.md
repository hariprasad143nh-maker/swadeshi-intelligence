# 🇮🇳 SWADESHI INTELLIGENCE
### AI-Assisted National Import Substitution & Domestic Production Intelligence Platform

> **HackWithAditya 2026** — National Level Hackathon  
> *Target Submission:* 25 November 2026 | *Team Size:* 4 Developers

---

## 📌 Executive Summary

**SWADESHI INTELLIGENCE** is an intelligent economic decision-support platform designed to convert India's import dependency into domestic production opportunities.

By consolidating official trade data from the **Department of Commerce (Trade Analytics Portal & TradeStat)** with agricultural and industrial feasibility models, the platform identifies high-value imported products that can be viably produced within India at competitive costs.

It delivers actionable intelligence to:
1. **Farmers & Agricultural Entrepreneurs:** High-value domestic cultivation alternatives (e.g., specific fruits, spices, oilseeds).
2. **MSMEs & Industrial Manufacturers:** Component-level import substitution targets (e.g., electronic passive components, chemical intermediates, precision machinery).
3. **Government & Policymakers:** Data-backed prioritization of PLI schemes, tariff protections, and regional manufacturing clusters.
4. **Corporate Buyers:** Direct discovery of emerging domestic suppliers to de-risk global supply chains.

---

## ⚡ The 6-Stage Intelligence Pipeline

1. **Trade Ingestion Engine:** Normalizes official Indian import statistics across HS2, HS4, and HS6 classifications.
2. **Product & Sector Classifier:** Segregates imported goods into Agriculture, Electronics, Chemicals, Machinery, and Industrial categories.
3. **Feasibility Assessment Engine:** Evaluates agro-climatic requirements, input availability, and capital intensity.
4. **Domestic Cost & Ranking Engine:** Calculates landed import cost vs estimated domestic production cost to derive the **Opportunity Score**.
5. **Geospatial Intelligence:** Maps optimal Indian states and districts possessing historical advantages or specialized industrial clusters.
6. **Stakeholder Dashboards:** Role-tailored recommendations for producers, buyers, and government planners.

---

## 🏗️ System Architecture

Built on a **Modular Monolithic Architecture** optimized for high-velocity 4-developer concurrent engineering:

```
swadeshi-intelligence/
├── docs/                 # Single source of truth (API & Database contracts)
├── backend/              # FastAPI application, database connections, and routes
├── data-engine/          # Data collection, cleaning, and HS-code mapping pipelines
├── intelligence-engine/  # Cost advantage, opportunity scoring, and recommendation logic
└── frontend/             # React.js + Vite + Tailwind CSS executive intelligence dashboard
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.11+
- Node.js 18+ & npm
- PostgreSQL 14+ (or SQLite for local development)

### 2. Backend Setup
```bash
# Clone the repository
git clone https://github.com/hariprasad143nh/swadeshi-intelligence.git
cd swadeshi-intelligence

# Configure environment
cp .env.example .env

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Run database migrations / seed data
python scripts/ingest_imports.py

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```
Interactive API docs available at: `http://localhost:8000/docs`

### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```
Dashboard available at: `http://localhost:5173`

---

## 👥 Team Workstream Allocation

| Team Member | Role | Owned Modules |
| :--- | :--- | :--- |
| **Member 1** | **Backend & Integration Lead** | `backend/app/`, `docs/api-contract.md` |
| **Member 2** | **Data Engineering Lead** | `data-engine/`, `backend/scripts/ingest_imports.py` |
| **Member 3** | **Intelligence & Analytics Lead** | `intelligence-engine/` |
| **Member 4** | **Frontend & Visualization Lead** | `frontend/` |

---

## 📜 Development Standards
All contributors and AI coding assistants must adhere to:
- [`PROJECT_SPEC.md`](./PROJECT_SPEC.md)
- [`ARCHITECTURE.md`](./ARCHITECTURE.md)
- [`AGENTS.md`](./AGENTS.md)
- [`docs/api-contract.md`](./docs/api-contract.md)
- [`docs/database-schema.md`](./docs/database-schema.md)
