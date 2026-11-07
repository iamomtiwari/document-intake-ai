# CI/CD

## Continuous integration

`.github/workflows/ci.yml` runs on feature pushes and pull requests targeting `dev` or `main`. It tests Python 3.11 and 3.12, runs Ruff, executes pytest, and builds the package once on Python 3.11.

## Continuous delivery

`.github/workflows/release.yml` runs for semantic version tags matching `v*.*.*` or manually from the Actions tab. It builds the wheel and source distribution and uploads them as a workflow artifact. No cloud deployment or package registry is configured yet; that remains intentionally outside the current deterministic baseline.

## GitHub setup

Authenticate locally before pushing or creating pull requests:

```bash
gh auth login
gh auth status
```

The repository should protect `main` and `dev` with required CI checks and require pull requests. Those settings require repository-owner access in GitHub and are not stored in source control.
