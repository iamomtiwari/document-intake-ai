# Architecture

## Target workflow

```text
document input
    ↓
deterministic or model-assisted extraction
    ↓
schema validation and confidence checks
    ↓
human approval for accepted records
    ↓
SQLite record and audit event
```

The first implementation will use deterministic extraction from synthetic input. Model-assisted extraction, PDF parsing, and external integrations are deferred until the baseline behavior is tested.
