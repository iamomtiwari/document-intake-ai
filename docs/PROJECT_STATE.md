# Project state

## Objective

Create the first portfolio project from the Applied AI Engineering Portfolio Plan: a safe, testable document-intake workflow.

## Current milestone

M4 — Append-only audit log and end-to-end workflow.

## Status

The repository contains a deterministic invoice workflow with a human-review boundary and SQLite persistence. Synthetic JSON fixtures are extracted into typed invoice records, checked with rule-based validation, routed through explicit approval or rejection states, and approved invoices can be persisted locally. The next milestone is append-only audit logging and an end-to-end local workflow.

## Recent changes

- Created the `document-intake-ai` Git repository on the `main` branch.
- Added initial Python packaging and development tooling configuration.
- Added README, roadmap, and project-state documentation.
- Added a small synthetic invoice schema, four fixtures, deterministic extraction, and validation tests.
- Added explicit invoice approval states, reviewer decisions, rejection reasons, and transition tests.
- Added an approved-only SQLite repository with persistence and retrieval tests.
- Merged PRs #1–#5 covering the baseline, workflow documentation, approval, security/QA gates, and SQLite persistence.

## Important decisions

- Start with deterministic synthetic data and rules so the workflow can be understood and evaluated before adding model complexity.
- Use SQLite later for local persistence; defer external services until the local workflow is reliable.
- Keep extraction free of model calls: JSON field normalization and Decimal/date parsing are deterministic and reproducible.
- Treat line-item arithmetic and subtotal-plus-tax arithmetic as validation rules; validation returns all discovered errors.
- Do not allow an invalid invoice to enter review or an approved/rejected invoice to receive another decision.
- Keep SQLite writes behind `InvoiceRepository.save_approved`; unreviewed and rejected invoices must not be stored.

## Verification

- Command: `git status --short --branch`
- Command: `/usr/bin/python3 -m compileall -q src tests`
- Result: Passed.
- Command: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /usr/bin/python3 -m pytest`
- Result: Pending environment check; pytest is not installed in the environment.
- Command: `git diff --check`
- Result: Passed.

## Risks and open questions

- The current fixture format is JSON representing a synthetic document; a future milestone can add a source-text adapter without changing validation rules.
- The current approval boundary is a Python domain object; a CLI or web interface can call it later.
- Line items are stored as deterministic JSON inside the local SQLite record for this first persistence milestone.

## Next three actions

1. Add append-only audit events for extraction, validation, persistence, and decisions.
2. Add end-to-end workflow tests and a small local CLI.
3. Evaluate database migrations and a review interface after the local workflow is stable.
