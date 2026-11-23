# SWADESHI INTELLIGENCE — AI AGENT OPERATIONAL RULES (AGENTS.md)

This file contains non-negotiable operational instructions for AI coding assistants (including Antigravity, Claude Code, Cursor, GitHub Copilot, and Gemini) operating within the `swadeshi-intelligence` repository.

---

## 1. Core Mandate
You are an autonomous AI coding agent assisting one of four developers building **SWADESHI INTELLIGENCE** for the **HackWithAditya 2026** hackathon. Your primary goal is to produce robust, modular code while strictly avoiding integration collisions with other team members.

---

## 2. Hierarchy of Authority
1. `PROJECT_SPEC.md` — The single source of truth for WHAT is being built.
2. `ARCHITECTURE.md` — The single source of truth for HOW modules communicate and who owns them.
3. `docs/database-schema.md` — The frozen source of truth for database tables and column types.
4. `docs/api-contract.md` — The frozen source of truth for API routes, payload structures, and JSON keys.

---

## 3. Strict Development Rules

### Rule 1: Never Break Frozen Contracts
- Never rename, alter, or omit fields in API responses specified in `docs/api-contract.md`.
- Never alter database column names or types without explicit multi-member approval.
- Frontend agents must consume the exact keys provided in the contract.

### Rule 2: Respect Module Ownership Boundaries
- If your assigned task is in `frontend/`, do not alter `backend/app/` code. Use mock data (`frontend/src/mocks/`) if backend endpoints are pending.
- If your assigned task is in `data-engine/`, do not modify `intelligence-engine/` formulas.
- If your assigned task is in `backend/`, import functions from `data-engine` or `intelligence-engine` using the documented interface signatures.

### Rule 3: Unit and Currency Integrity
- Trade data must preserve currency markers (`USD` vs `INR`).
- Volume metrics must preserve units (`KG`, `TONNES`, `PIECES`).
- Never perform mathematical operations on mixed currencies or units without explicit conversion.

### Rule 4: Clean Dependencies & Modular Code
- Backend Python dependencies belong in `backend/requirements.txt`.
- Frontend dependencies belong in `frontend/package.json`.
- Do not add heavy, unverified third-party libraries without necessity.
- Do not write monolithic 1000-line single-file scripts. Keep modules decoupled and testable.

### Rule 5: Transparent & Explainable Algorithms
- The ranking and feasibility engines must be deterministic and explainable.
- Avoid opaque random weights; document the economic rationale for scoring formulas.
