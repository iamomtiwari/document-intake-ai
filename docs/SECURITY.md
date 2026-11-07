# Security and privacy

## Pre-PR security gate

Run `bash scripts/pre_pr.sh` before opening every pull request. The security portion scans tracked and untracked non-ignored files for common credential indicators and sensitive filenames, then `pip-audit` checks Python dependencies. The same checks run in GitHub Actions alongside the Playwright browser QA harness.

This baseline does not replace human security review. Do not commit secrets, personal data, real invoices, or employer-confidential material.

- Use synthetic or explicitly permitted documents only.
- Treat extracted values as untrusted input and validate them before storage or action.
- Require human approval before a record is considered accepted.
- Keep local databases and environment files out of Git.
- Do not add credentials, tokens, personal data, or employer-confidential content.
