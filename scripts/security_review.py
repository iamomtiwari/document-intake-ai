#!/usr/bin/env python3
"""Run a small, deterministic security review before a pull request."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


SECRET_PATTERNS = (
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?:ghp|github_pat)_[A-Za-z0-9_]{20,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(
        r"(?i)(?:api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]{8,}['\"]"
    ),
)
SENSITIVE_NAMES = re.compile(
    r"(^|/)(?:\.env|credentials|id_rsa)(?:$|\.)|\.(?:pem|key)$", re.IGNORECASE
)
ALLOWED_ENV_FILE = ".env.example"


def candidate_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-co", "--exclude-standard"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [Path(line) for line in result.stdout.splitlines()]


def review() -> list[str]:
    findings: list[str] = []
    for path in candidate_files():
        normalized = path.as_posix()
        if SENSITIVE_NAMES.search(normalized) and normalized != ALLOWED_ENV_FILE:
            findings.append(f"sensitive filename: {normalized}")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                findings.append(f"possible secret in {normalized}: {pattern.pattern}")
    return findings


if __name__ == "__main__":
    findings = review()
    if findings:
        print("Security review failed:")
        print("\n".join(f"- {finding}" for finding in findings))
        sys.exit(1)
    print("Security review passed: no tracked or untracked secret indicators found.")
