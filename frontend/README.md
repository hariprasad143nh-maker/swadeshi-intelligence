# Frontend Module (frontend)

**Owner:** Member 4 (Frontend & Visualization Lead)  
**Assigned AI Assistants:** Antigravity / Claude  

## Purpose
The Frontend delivers an executive government/industrial economic intelligence dashboard built with **React**, **Vite**, and **Tailwind CSS**.

## Main Sections
1. **Overview Dashboard:** Macro national import dependency metrics, total tracked billions USD, sectoral pie chart.
2. **Product Explorer:** Searchable, paginated table of imported HS-code commodities with sector filters.
3. **Opportunity Rankings:** Ranked table sorted by Opportunity Score, landed vs domestic cost diff, and potential savings %.
4. **Regional Suitability Map:** Interactive district/state suitability indicators.
5. **Stakeholder Recommendations:** Persona toggle (Farmer, MSME, Industrialist, Policymaker).

## Quickstart
```bash
npm install
npm run dev
```

## Mock Mode
If backend is not yet running locally, enable mock mode in `.env`:
```env
VITE_USE_MOCKS=true
```
This loads structured data from `src/mocks/opportunities.json`.
