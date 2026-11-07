# Project state

## Objective

Create the first portfolio project from the Applied AI Engineering Portfolio Plan: a safe, testable document-intake workflow.

## Current milestone

M2 — Human approval state transitions.

## Status

The repository contains a deterministic invoice workflow with a human-review boundary. Synthetic JSON fixtures are extracted into typed invoice records, checked with rule-based validation, and routed through explicit approval or rejection states. SQLite persistence and audit logging remain future milestones.

## Recent changes

- Created the `document-intake-ai` Git repository on the `main` branch.
- Added initial Python packaging and development tooling configuration.
- Added README, roadmap, and project-state documentation.
- Added a small synthetic invoice schema, four fixtures, deterministic extraction, and validation tests.
- Added explicit invoice approval states, reviewer decisions, rejection reasons, and transition tests.

## Important decisions

- Start with deterministic synthetic data and rules so the workflow can be understood and evaluated before adding model complexity.
- Use SQLite later for local persistence; defer external services until the local workflow is reliable.
- Keep extraction free of model calls: JSON field normalization and Decimal/date parsing are deterministic and reproducible.
- Treat line-item arithmetic and subtotal-plus-tax arithmetic as validation rules; validation returns all discovered errors.
- Do not allow an invalid invoice to enter review or an approved/rejected invoice to receive another decision.

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

## Next three actions

1. Persist approved invoices and validation results in SQLite.
2. Add append-only audit events for extraction, validation, and decisions.
3. Add end-to-end workflow tests and a small local CLI.
