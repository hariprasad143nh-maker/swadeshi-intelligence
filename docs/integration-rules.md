# Integration & Testing Protocol (docs/integration-rules.md)

This protocol governs how the 4 developer modules connect seamlessly and how testing is performed during rapid iteration.

---

## 1. Decoupled Development via Mocks

While backend and analytics pipelines are under construction, frontend and intelligence modules must operate against mock data:

### Frontend Mocking
- Member 4 creates `frontend/src/mocks/opportunities.json` adhering to `docs/api-contract.md`.
- In `frontend/src/services/api.js`, implement a flag:
  ```javascript
  const USE_MOCKS = import.meta.env.VITE_USE_MOCKS === 'true';
  ```
- This ensures UI development proceeds without waiting for live database seeding.
- **Rule:** Before final submission, verify with `VITE_USE_MOCKS=false` against the live FastAPI backend.

---

## 2. Ingestion to Database Testing
1. Member 2 produces clean canonical CSVs in `backend/data/raw/india_imports.csv`.
2. Run ingestion script:
   ```bash
   python backend/scripts/ingest_imports.py
   ```
3. Verify ingestion count:
   ```sql
   SELECT sector, COUNT(*) FROM products GROUP BY sector;
   SELECT COUNT(*) FROM import_records;
   ```

---

## 3. Analytical Engine Integration
- Member 3 implements pure Python modules inside `intelligence-engine/`.
- Member 1 writes service adapters in `backend/app/services/` that call Member 3's functions and store/retrieve results from PostgreSQL.
- Member 3 writes standalone unit tests in `intelligence-engine/tests/` using `pytest`.

---

## 4. End-to-End Smoke Test Checklist
Before committing to `main` or submitting pull requests:
- [ ] Database schema matches `docs/database-schema.md`.
- [ ] FastAPI boots without error on `http://localhost:8000`.
- [ ] `GET /api/health` returns status `healthy`.
- [ ] `GET /api/opportunities` returns valid JSON matching the contract.
- [ ] Frontend builds without TypeScript/Vite syntax errors (`npm run build`).
