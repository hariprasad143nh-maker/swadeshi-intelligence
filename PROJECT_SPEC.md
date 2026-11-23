# SWADESHI INTELLIGENCE
## Project Specification (PROJECT_SPEC.md)

**Project Name:** SWADESHI INTELLIGENCE  
**Project Type:** AI-Assisted National Import Substitution and Domestic Production Intelligence Platform  
**Hackathon:** HackWithAditya 2026  
**Development Team:** 4 Members  
**Backend:** Python + FastAPI  
**Frontend:** React.js + Vite + Tailwind CSS  
**Database:** PostgreSQL  
**Target Online Submission:** 25 November 2026  
**Project Status:** Initial MVP Development  

---

## 1. Project Overview

**SWADESHI INTELLIGENCE** is an AI-assisted economic intelligence platform designed to identify opportunities for replacing economically avoidable imports with competitive domestic production.

The platform analyzes India's official import data across multiple economic sectors, identifies products that India could potentially cultivate, manufacture, process, or produce domestically, evaluates their economic feasibility, compares domestic production costs against landed import costs, and ranks potential domestic production opportunities.

It also identifies suitable geographical locations (states and districts) and recommends production opportunities to relevant stakeholders, including farmers, entrepreneurs, MSMEs, and industrial manufacturers.

The platform bridges the gap between import intelligence, actual domestic production capabilities, and market demand.

**Core Vision:**  
*Discover what India imports, determine what India can produce, calculate whether domestic production is economically competitive, identify where production should take place, and recommend opportunities to the right producers and industries.*

---

## 2. Problem Statement

India imports a wide range of products across agriculture, electronics, chemicals, industrial raw materials, machinery, renewable energy, and other sectors.

Although India has diverse natural resources, agricultural capabilities, industrial infrastructure, and entrepreneurial potential, identifying economically viable domestic production alternatives requires information from multiple disconnected sources.

Potential producers often lack access to consolidated information about:
1. True import demand and volumes.
2. Domestic production feasibility and technology requirements.
3. Geographical suitability (agro-climatic zones, industrial clusters).
4. Comparable production costs versus landed import costs.
5. Direct connections with potential domestic buyers.

Similarly, policymakers and industries need analytical tools to identify products that could be produced domestically at competitive costs and to understand where targeted intervention or investment is most beneficial.

**SWADESHI INTELLIGENCE** bridges this critical information gap through a unified intelligence, ranking, and recommendation platform.

---

## 3. Project Objectives

1. **Ingest & Normalize Trade Data:** Ingest official Indian import records across HS2, HS4, and HS6 classifications.
2. **Sectoral Classification:** Automatically classify imported goods into distinct sectors (Agriculture, Electronics, Chemicals, Machinery, etc.).
3. **Feasibility Assessment:** Evaluate technical and climatic feasibility using sector-specific evaluation rules.
4. **Cost Competitiveness Modeling:** Compare landed import costs against estimated domestic production costs.
5. **Opportunity Ranking Engine:** Rank domestic substitution opportunities by economic viability, import scale, and feasibility.
6. **Geospatial Intelligence:** Identify suitable Indian states and districts for domestic production.
7. **Actionable Recommendations:** Provide tailored opportunity recommendations for farmers, MSMEs, and manufacturers.
8. **Producer-Buyer Linkage:** Provide a foundational directory connecting emerging domestic producers with industrial buyers.
9. **Policy Insights:** Offer macro-level visibility into import dependencies and high-priority substitution candidates.

---

## 4. Target Stakeholders & Capabilities

### 4.1 Government & Policymakers
- Monitor India's sectoral import dependency.
- Identify strategic commodities with high domestic substitution potential.
- Identify regional production clusters and infrastructure gaps.
- Prioritize incentives, subsidies, and PLI schemes with verifiable data.

### 4.2 Farmers, MSMEs & Domestic Producers
- Discover imported goods that offer domestic production opportunities.
- Review feasibility reports, cost benchmarks, and expected margins.
- Understand soil/climate or industrial requirements.
- Identify ready buyers seeking domestic supply.

### 4.3 Industrial Buyers & Corporates
- Identify emerging domestic suppliers to reduce supply-chain vulnerability.
- Signal product specifications and volume requirements to local producers.
- Reduce dependency on volatile foreign exchange and import duties.

---

## 5. Scope for Online Preliminary Round (Deadline: 25 Nov 2026)

For the initial 2-day sprint, the team focuses on an explainable, data-driven MVP:

### In Scope (MVP):
- Ingestion of official import datasets (Trade Analytics / TradeStat) covering representative products across 4 sectors:
  - **Agriculture** (e.g., specific fruits, spices, pulses)
  - **Electronics** (e.g., passive components, sub-assemblies)
  - **Chemicals** (e.g., active pharmaceutical ingredients, polymers)
  - **Machinery** (e.g., motors, pumps, tooling)
- Automated opportunity ranking based on landed cost vs. domestic cost.
- District/State suitability mapping for demonstrated case studies.
- Interactive Web Dashboard (React + Vite + Tailwind) connected via FastAPI REST endpoints.

### Out of Scope for Preliminary Round (Deferred to Finale):
- Nationwide live transactional e-commerce checkout.
- Deep-learning black-box neural networks (explainable scoring preferred).
- Live real-time customs port scraping (static government CSVs used for stability).

---

## 6. Success Metrics for Online Round
1. Real government import data loaded and queryable via API.
2. Transparent calculation of cost advantage and opportunity scores.
3. Clear demonstration of cross-sectoral analysis (not exclusively agriculture).
4. Responsive, clean executive dashboard suitable for live judging.
