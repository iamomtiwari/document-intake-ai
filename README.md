# Document Intake AI

An applied AI workflow for turning a synthetic business document into a validated, human-approved record.

## First milestone

```text
synthetic document → structured fields → validation → human approval → SQLite
```

The first version intentionally uses deterministic sample data and rules. Model-assisted extraction will be added only after the workflow, tests, and failure handling are understood.

## Status

The deterministic extraction and validation baseline is implemented. Approval, SQLite persistence, and audit logging are the next workflow milestones.

## Repository layout

- `src/document_intake/` — application code
- `tests/` — automated tests
- `sample-data/` — synthetic documents only
- `docs/` — architecture, evaluation, security, and project continuity

## Local setup

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest
```

## Git workflow and delivery

Use `main` for stable code, `dev` for integration, and `feat/*` for changes. Every pull request into `dev` or `main` runs the CI workflow. Pushing a version tag such as `v0.1.0` runs the delivery workflow and stores a built package in GitHub Actions artifacts.

```bash
git switch -c feat/my-change dev
git push -u origin feat/my-change
# Open a pull request from feat/my-change into dev
git switch dev
git pull --ff-only origin dev
git tag v0.1.0
git push origin v0.1.0
```

## Data and safety

This project uses synthetic data. Do not add real invoices, personal data, credentials, or employer-confidential material.

## License

MIT. See [LICENSE](LICENSE).
