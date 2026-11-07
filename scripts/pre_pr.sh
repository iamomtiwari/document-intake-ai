#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "[1/5] Security review"
"${PYTHON_BIN}" scripts/security_review.py
echo "[2/5] Python lint"
ruff check .
echo "[3/5] Python tests"
"${PYTHON_BIN}" -m pytest
echo "[4/5] Dependency audit and package build"
pip-audit
"${PYTHON_BIN}" -m build
echo "[5/5] Playwright QA"
npm install --no-fund --no-audit
npx playwright install chromium
npm run qa
echo "Pre-PR checks passed. You can now create the pull request."
