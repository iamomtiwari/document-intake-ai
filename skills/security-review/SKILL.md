---
name: document-intake-security-review
description: Review document-intake-ai changes for secrets, sensitive files, dependency vulnerabilities, and required pre-PR checks.
---

# Document intake security review

Use this review for every change before creating a pull request in `document-intake-ai`.

Run `scripts/pre_pr.sh` from the repository root. It performs the deterministic secret/sensitive-file scan, Ruff, pytest, `pip-audit`, package build, and Playwright QA smoke test.

Do not bypass a failed security review. Investigate the finding and remove real secrets or sensitive data from the working tree and Git history as appropriate. `.env.example` is allowed only for placeholders and must never contain credentials.

This is a baseline automated review. It does not prove that the application is secure, replace human review, or cover production infrastructure, authorization policy, database access controls, or threat modeling.
