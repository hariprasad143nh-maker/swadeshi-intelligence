# CLAUDE.md — Guidelines for Claude Code in Swadeshi Intelligence

## Project Overview
SWADESHI INTELLIGENCE is an AI-assisted National Import Substitution & Domestic Production Intelligence Platform built for HackWithAditya 2026.

## Development Commands
- **Backend (FastAPI):**
  - Install dependencies: `pip install -r backend/requirements.txt`
  - Run development server: `uvicorn backend.app.main:app --reload --port 8000`
  - Ingest raw data: `python backend/scripts/ingest_imports.py`
  - Run tests: `pytest backend/tests/`
- **Frontend (React + Vite):**
  - Install dependencies: `npm install` (inside `frontend/`)
  - Run development server: `npm run dev` (inside `frontend/`)
  - Build for production: `npm run build` (inside `frontend/`)

## Architecture & Code Standards
1. Follow `PROJECT_SPEC.md` and `ARCHITECTURE.md` as the authoritative project guides.
2. Comply strictly with `docs/api-contract.md` and `docs/database-schema.md`.
3. Keep code modular:
   - Member 1 owns `backend/app/`
   - Member 2 owns `data-engine/`
   - Member 3 owns `intelligence-engine/`
   - Member 4 owns `frontend/`
4. Do not commit credentials or raw datasets (`.env`, large CSVs are ignored in `.gitignore`).
5. Ensure explainable, deterministic mathematical scoring in all ranking and cost comparison functions.
