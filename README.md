# Document Intake AI

An applied AI workflow for turning a synthetic business document into a validated, human-approved record.

## First milestone

```text
synthetic document → structured fields → validation → human approval → SQLite
```

The first version intentionally uses deterministic sample data and rules. Model-assisted extraction will be added only after the workflow, tests, and failure handling are understood.

## Status

Repository scaffolded. The minimal extraction, validation, approval, and persistence workflow is the next implementation step.

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

## Data and safety

This project uses synthetic data. Do not add real invoices, personal data, credentials, or employer-confidential material.

## License

MIT. See [LICENSE](LICENSE).
