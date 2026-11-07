"""SQLite persistence for approved invoices."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from document_intake.approval import ApprovalStatus, InvoiceApproval


class PersistenceError(ValueError):
    """Raised when an invoice cannot be persisted safely."""


@dataclass(frozen=True)
class StoredInvoice:
    invoice_id: str
    vendor_name: str
    invoice_date: str
    due_date: str
    currency: str
    line_items: tuple[dict[str, Any], ...]
    subtotal: Decimal
    tax: Decimal
    total: Decimal
    validation_errors: tuple[str, ...]
    approval_status: ApprovalStatus
    reviewer: str
    decided_at: datetime
    rejection_reason: str | None


SCHEMA = """
CREATE TABLE IF NOT EXISTS invoices (
    invoice_id TEXT PRIMARY KEY,
    vendor_name TEXT NOT NULL,
    invoice_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    currency TEXT NOT NULL,
    line_items_json TEXT NOT NULL,
    subtotal TEXT NOT NULL,
    tax TEXT NOT NULL,
    total TEXT NOT NULL,
    validation_errors_json TEXT NOT NULL,
    approval_status TEXT NOT NULL CHECK (approval_status = 'approved'),
    reviewer TEXT NOT NULL,
    decided_at TEXT NOT NULL,
    rejection_reason TEXT,
    created_at TEXT NOT NULL
)
"""


class InvoiceRepository:
    """Persist and retrieve invoices that have passed human approval."""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = str(database_path)
        self.initialize()

    def initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(SCHEMA)

    def save_approved(self, approval: InvoiceApproval) -> None:
        if approval.status is not ApprovalStatus.APPROVED or approval.decision is None:
            raise PersistenceError("only approved invoices can be persisted")

        invoice = approval.invoice
        decision = approval.decision
        line_items = [
            {
                "description": item.description,
                "quantity": str(item.quantity),
                "unit_price": str(item.unit_price),
            }
            for item in invoice.line_items
        ]
        with self._connect() as connection:
            try:
                connection.execute(
                    """
                    INSERT INTO invoices (
                        invoice_id, vendor_name, invoice_date, due_date, currency,
                        line_items_json, subtotal, tax, total, validation_errors_json,
                        approval_status, reviewer, decided_at, rejection_reason, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        invoice.invoice_id,
                        invoice.vendor_name,
                        invoice.invoice_date.isoformat(),
                        invoice.due_date.isoformat(),
                        invoice.currency,
                        json.dumps(line_items, sort_keys=True),
                        str(invoice.subtotal),
                        str(invoice.tax),
                        str(invoice.total),
                        json.dumps(list(approval.validation.errors)),
                        decision.status.value,
                        decision.reviewer,
                        decision.decided_at.isoformat(),
                        decision.reason,
                        datetime.now(UTC).isoformat(),
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise PersistenceError(
                    f"invoice {invoice.invoice_id} could not be persisted"
                ) from exc

    def get(self, invoice_id: str) -> StoredInvoice | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM invoices WHERE invoice_id = ?", (invoice_id,)
            ).fetchone()
        if row is None:
            return None
        return StoredInvoice(
            invoice_id=row["invoice_id"],
            vendor_name=row["vendor_name"],
            invoice_date=row["invoice_date"],
            due_date=row["due_date"],
            currency=row["currency"],
            line_items=tuple(json.loads(row["line_items_json"])),
            subtotal=Decimal(row["subtotal"]),
            tax=Decimal(row["tax"]),
            total=Decimal(row["total"]),
            validation_errors=tuple(json.loads(row["validation_errors_json"])),
            approval_status=ApprovalStatus(row["approval_status"]),
            reviewer=row["reviewer"],
            decided_at=datetime.fromisoformat(row["decided_at"]),
            rejection_reason=row["rejection_reason"],
        )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection
