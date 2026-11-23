# Contributing to Swadeshi Intelligence

Welcome to the team! This repository is shared across 4 developers building concurrently for **HackWithAditya 2026**.

## 1. Git Workflow

### Branch Naming Conventions
Always create feature branches off `main`:
- `feature/backend-core` (Member 1 - Backend & API)
- `feature/data-pipeline` (Member 2 - Data Extraction & Cleaning)
- `feature/intelligence-engine` (Member 3 - Cost & Ranking Engine)
- `feature/frontend-dashboard` (Member 4 - React UI & Visualizations)

### Commit Message Guidelines
Follow conventional commits:
- `feat(backend): add product and import record models`
- `feat(data): implement Trade Analytics CSV cleaner`
- `feat(intelligence): add opportunity score formula`
- `feat(frontend): build opportunity ranking table`
- `docs: update api contract schema`
- `fix(engine): correct unit conversion in cost comparison`

---

## 2. Pull Request & Integration Protocol

1. **Pull Latest Main:** Before pushing, pull latest changes (`git pull origin main --rebase`).
2. **Contract Compliance:** Ensure any modified routes match `docs/api-contract.md`.
3. **No Direct Pushes to Main:** All substantial features must be submitted via Pull Request and reviewed by at least one teammate (e.g., Backend Lead reviews data & engine integrations).
4. **Clean Commits:** Do not commit `.env`, temporary `.dump` files, or large raw datasets (>10MB).
