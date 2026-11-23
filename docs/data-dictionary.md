# Data Dictionary & Standardization Guide (docs/data-dictionary.md)

This document standardizes all units, HS classifications, currency handling, and naming conventions used across all modules of **SWADESHI INTELLIGENCE**.

---

## 1. Currency Handling
* **Import Values in Trade Records:** Stored primarily in **USD** (`import_value_usd`), matching Government of India Department of Commerce source extracts.
* **Cost Competitiveness Calculations:** Computed in **INR** (`import_cost`, `domestic_cost`).
* **Conversion Standard:** A standardized exchange rate is applied and logged (e.g., 1 USD = 85.00 INR for FY 2024–25 / 2025–26 baseline comparisons).
* **Rule:** Never compare USD against INR without explicit conversion.

---

## 2. Quantity & Metric Units
All volume and quantity records must use standard uppercase unit identifiers:
- `KG` (Kilograms)
- `TONNES` (Metric Tonnes)
- `PIECES` (Discrete manufactured units, e.g., electronic modules, motors)
- `LITRES` (Liquid chemical volumes)
- `METERS` (Textiles, wires, cable runs)

---

## 3. HS Code Standards
- **HS2 (2-Digit Chapter):** Major commodity classification (e.g., `08` - Edible fruits & nuts, `85` - Electrical machinery & electronics).
- **HS4 (4-Digit Heading):** Primary classification used for MVP aggregation (e.g., `0810` - Other fruit, fresh; `8504` - Electrical transformers/converters).
- **HS6 / HS8 (Subheading & ITC National Tariff Lines):** Detailed product level.
- **Data Cleaner Rule:** Strip any trailing `.0` resulting from pandas float parsing (e.g., `850440.0` $\rightarrow$ `850440`).

---

## 4. Sector Classifications
Products are mapped into five core sectors:
1. `agriculture`: Edible produce, fruits, vegetables, spices, oilseeds, cash crops.
2. `electronics`: Semiconductors, integrated circuits, passive components, PCBs, displays.
3. `chemicals`: Active pharmaceutical ingredients (APIs), polymers, fertilizers, specialty chemicals.
4. `machinery`: Pumps, industrial motors, CNC tooling, agricultural equipment.
5. `other`: Unclassified or cross-sector industrial raw materials.
