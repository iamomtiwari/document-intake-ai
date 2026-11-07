# Daily log

## 2026-11-07

- Verified the intended repository at `/home/imomtiwari/document-intake-ai`; local branches `main`, `dev`, and `feat/document-intake-baseline` all pointed to `824eb95`.
- Confirmed the configured GitHub remote. Push was attempted but DNS access to GitHub was unavailable in the restricted environment.
- Defined the synthetic invoice schema: invoice metadata, ISO dates, three-letter currency, line items, subtotal, tax, and total.
- Added four synthetic JSON fixtures and deterministic extraction/validation tests.
- Verification: source changes are syntactically checked without bytecode writes; the environment does not currently provide pytest or ruff.
- Added matrix CI for Python 3.11/3.12, package build verification, a tag-based delivery artifact workflow, and a pull-request template.
- Documented GitHub authentication and branch protection requirements in `docs/CI_CD.md`.
- Implemented the human approval state machine with deterministic transitions and reviewer decisions.
- Added tests for approval, rejection, invalid invoices, duplicate decisions, and required decision fields.
- Implemented approved-only SQLite persistence with deterministic line-item serialization and retrieval.
- Added persistence tests covering approved, unreviewed, rejected, and duplicate invoices.
