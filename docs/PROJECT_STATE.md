# Project state

## Objective

Create the first portfolio project from the Applied AI Engineering Portfolio Plan: a safe, testable document-intake workflow.

## Current milestone

M1 — Deterministic invoice extraction and validation.

## Status

The repository contains a deterministic invoice workflow. Synthetic JSON fixtures are extracted into typed invoice records and checked with rule-based validation. Approval, SQLite persistence, and audit logging remain future milestones.

## Recent changes

- Created the `document-intake-ai` Git repository on the `main` branch.
- Added initial Python packaging and development tooling configuration.
- Added README, roadmap, and project-state documentation.
- Added a small synthetic invoice schema, four fixtures, deterministic extraction, and validation tests.

## Important decisions

- Start with deterministic synthetic data and rules so the workflow can be understood and evaluated before adding model complexity.
- Use SQLite later for local persistence; defer external services until the local workflow is reliable.
- Keep extraction free of model calls: JSON field normalization and Decimal/date parsing are deterministic and reproducible.
- Treat line-item arithmetic and subtotal-plus-tax arithmetic as validation rules; validation returns all discovered errors.

## Verification

- Command: `git status --short --branch`
- Command: `/usr/bin/python3 -m compileall -q src tests`
- Result: Passed.
- Command: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /usr/bin/python3 -m pytest`
- Result: Pending environment check; pytest is not installed in the environment.
- Command: `git diff --check`
- Result: Passed.

## Risks and open questions

- The approval interface is not yet chosen.
- The current fixture format is JSON representing a synthetic document; a future milestone can add a source-text adapter without changing validation rules.

## Next three actions

1. Add explicit approval state transitions and a human-review boundary.
2. Persist approved invoices and validation results in SQLite.
3. Add append-only audit events and end-to-end workflow tests.
