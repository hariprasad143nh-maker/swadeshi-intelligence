# Data Engine Module (data-engine)

**Owner:** Member 2 (Data Engineering Lead)  
**Assigned AI Assistants:** Claude / ChatGPT / Antigravity  

## Purpose
The Data Engine is responsible for:
1. Extracting trade data from the official Government of India Trade Analytics Portal and TradeStat.
2. Normalizing inconsistent column headers, currency symbols, and quantity units.
3. Classifying HS4/HS6 codes into sectors (`agriculture`, `electronics`, `chemicals`, `machinery`, `other`).
4. Validating data integrity before ingestion into PostgreSQL.

## Directory Structure
- `collectors/`: Web and API collection scripts for official datasets.
- `processors/`: Cleaning, deduplication, and currency/unit standardization.
- `mappings/`: HS classification dictionaries and sectoral rule definitions.
- `validators/`: Sanity checks for missing fields, invalid numbers, and corrupted records.

## Canonical Data Output
All processed datasets must conform to `docs/data-dictionary.md` and match the schema required by `backend/scripts/ingest_imports.py`.
