# Project plan and agent handoff

This file is the durable context for continuing `document-intake-ai` without relying on chat history.

## Objective

Build a simple, reliable workflow:

```text
synthetic document → structured extraction → validation → human approval → SQLite persistence → audit log
```

The project deliberately starts with deterministic synthetic data. Agents must not add model calls, agents, cloud infrastructure, real invoices, personal data, or employer-confidential material unless the plan is explicitly revised.

## Completed

- Repository initialized with `main`, `dev`, and `feat/*` branch conventions.
- Synthetic invoice schema and four fixtures added.
- Deterministic extraction and Decimal/date normalization implemented.
- Rule validation added for required fields, dates, currency, line items, subtotal, tax, and total.
- Human approval state machine added: `EXTRACTED → VALIDATED → PENDING_REVIEW → APPROVED/REJECTED`.
- Invalid invoices and terminal approval decisions are blocked.
- Approved-only SQLite persistence added with retrieval and duplicate protection.
- CI runs Python 3.11/3.12 lint, tests, and package build.
- Security review scans run before PRs and in CI.
- `pip-audit` dependency review added.
- Playwright Chromium QA harness added and passing in CI.
- Developer workflow, security guidance, and agent handoff documentation added.
- PRs #1–#5 merged through the project workflow.

## Current state

`dev` contains the merged approval, security/QA, and SQLite work. The next implementation milestone is the append-only audit log.

## Remaining plan

### M4 — Audit log and end-to-end workflow

1. Add an append-only `audit_events` SQLite table.
2. Record extraction, validation, review submission, approval/rejection, and persistence events.
3. Add immutable event fields: event ID, invoice ID, event type, actor, timestamp, and JSON details.
4. Add end-to-end tests proving event order and that existing events are never updated or deleted.
5. Add a small local CLI that runs the workflow on a synthetic fixture.

### M5 — Evaluation and review usability

1. Document extraction and validation metrics.
2. Add a review summary command or minimal local review interface.
3. Add failure-analysis examples using synthetic documents.
4. Add database migration/versioning guidance if the schema expands.

### M6 — Public portfolio delivery

1. Improve the README with a reproducible demo.
2. Add architecture and evaluation diagrams only where they clarify behavior.
3. Publish a case study describing tradeoffs, failures, and security boundaries.

## Explicitly deferred

- LLM-assisted extraction
- PDF parsing and email ingestion
- Multi-agent orchestration
- FastAPI or browser approval UI beyond the QA harness
- PostgreSQL, cloud services, and production deployment

## How to resume

```bash
cd /home/imomtiwari/document-intake-ai
git status
git switch dev
git pull --ff-only origin dev
git switch -c feat/audit-log
```

Before opening a PR:

```bash
bash scripts/pre_pr.sh
git diff --check
git push -u origin feat/audit-log
gh pr create --base dev --head feat/audit-log
```

Read `docs/DEVELOPER_WORKFLOW.md` for the complete branch and delivery routine.
