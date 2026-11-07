# Project state

## Objective

Create the first portfolio project from the Applied AI Engineering Portfolio Plan: a safe, testable document-intake workflow.

## Current milestone

M0 — Repository and environment setup.

## Status

The repository is initialized with the planned structure, packaging metadata, contribution guidance, a smoke test, and continuity documents. No business workflow has been implemented yet.

## Recent changes

- Created the `document-intake-ai` Git repository on the `main` branch.
- Added initial Python packaging and development tooling configuration.
- Added README, roadmap, and project-state documentation.

## Important decisions

- Start with deterministic synthetic data and rules so the workflow can be understood and evaluated before adding model complexity.
- Use SQLite later for local persistence; defer external services until the local workflow is reliable.

## Verification

- Command: `git status --short --branch`
- Command: `/usr/bin/python3 -m compileall -q src tests`
- Result: Passed.
- Command: `PYTHONPATH=src /usr/bin/python3 -m pytest`
- Result: Not run because `pytest` is not installed in the environment.
- Command: `git diff --check`
- Result: Passed.

## Risks and open questions

- The exact document type and field schema need to be selected before M1.
- The approval interface is not yet chosen.

## Next three actions

1. Choose a synthetic invoice schema and add representative fixtures.
2. Implement extraction and rule-based validation with tests.
3. Add approval state transitions and SQLite persistence.
