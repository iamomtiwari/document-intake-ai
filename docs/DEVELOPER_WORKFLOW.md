# Developer workflow

Use this page as the starting point for every coding session.

## Start a session

```bash
cd /home/imomtiwari/document-intake-ai
git status
git switch dev
git pull --ff-only origin dev
git switch -c feat/<short-description>
```

If you are resuming an existing feature, switch to that feature branch instead of creating a new one.

## Work and verify

Run these checks before committing:

```bash
python -m pytest
ruff check .
python -m build
git diff --check
```

Keep changes focused. Use synthetic data only; never commit credentials, personal data, real invoices, or employer-confidential material.

## Commit and pull request

```bash
git status
git add <files>
git commit -m "feat: describe the change"
git push -u origin feat/<short-description>
gh pr create --base dev --head feat/<short-description>
```

The normal promotion path is:

```text
feat/* → dev → main
```

Do not merge a feature into `dev` locally before opening its PR; otherwise GitHub will report that there are no commits between the branches.

## Finish a session

```bash
git status
git log --oneline --decorate -8
git push
```

After a PR is merged, update local stable branches:

```bash
git switch main
git pull --ff-only origin main
git switch dev
git pull --ff-only origin dev
```

## Delivery

Pushing a tag such as `v0.1.0` runs the package delivery workflow:

```bash
git switch main
git pull --ff-only origin main
git tag v0.1.0
git push origin v0.1.0
```

See [CI/CD](CI_CD.md) for workflow details.
