# Roadmap

## Project goal

Build a reproducible document-intake workflow that extracts structured fields, validates them, obtains human approval, and records an audit trail.

## Milestones

- [x] M0 — Repository and environment setup
- [x] M1 — Deterministic extraction and validation
- [x] M2 — Human approval and transition tests
- [x] M3 — SQLite persistence for approved invoices
- [x] M4a — Tests, security gates, Playwright QA, and CI
- [ ] M4b — Append-only audit log and end-to-end workflow
- [ ] M5 — Evaluation and failure analysis
- [ ] M6 — Public demo and case study

## Current milestone

M4b — Append-only audit log and end-to-end workflow.

## Definition of done

A new contributor can run the test suite locally, understand the workflow from the README and architecture note, and reproduce the documented evaluation results.

## Deferred ideas

- LLM-assisted extraction
- PDF parsing and email ingestion
- FastAPI and browser approval UI
- PostgreSQL and cloud deployment
