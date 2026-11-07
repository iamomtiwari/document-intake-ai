import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from document_intake.approval import ApprovalStatus, InvoiceApproval
from document_intake.invoice import extract_invoice, validate_invoice
from document_intake.persistence import InvoiceRepository, PersistenceError

DATA = Path(__file__).parents[1] / "sample-data"


def approved_invoice() -> InvoiceApproval:
    document = json.loads((DATA / "invoice-valid.json").read_text())
    invoice = extract_invoice(document)
    approval = InvoiceApproval(invoice, validate_invoice(invoice))
    approval.mark_validated()
    approval.submit_for_review()
    approval.approve("reviewer@example.test", datetime(2026, 1, 20, tzinfo=UTC))
    return approval


def test_approved_invoice_is_persisted(tmp_path: Path) -> None:
    repository = InvoiceRepository(tmp_path / "invoices.sqlite3")
    approval = approved_invoice()

    repository.save_approved(approval)
    stored = repository.get("INV-1001")

    assert stored is not None
    assert stored.approval_status is ApprovalStatus.APPROVED
    assert stored.total == approval.invoice.total
    assert stored.reviewer == "reviewer@example.test"
    assert stored.line_items[0]["description"] == "Printer paper"


def test_unreviewed_invoice_cannot_be_persisted(tmp_path: Path) -> None:
    document = json.loads((DATA / "invoice-valid.json").read_text())
    invoice = extract_invoice(document)
    approval = InvoiceApproval(invoice, validate_invoice(invoice))
    repository = InvoiceRepository(tmp_path / "invoices.sqlite3")

    with pytest.raises(PersistenceError, match="only approved"):
        repository.save_approved(approval)
    assert repository.get(invoice.invoice_id) is None


def test_rejected_invoice_cannot_be_persisted(tmp_path: Path) -> None:
    approval = approved_invoice()
    approval = InvoiceApproval(approval.invoice, approval.validation)
    approval.mark_validated()
    approval.submit_for_review()
    approval.reject("reviewer@example.test", "Supporting detail is missing")
    repository = InvoiceRepository(tmp_path / "invoices.sqlite3")

    with pytest.raises(PersistenceError, match="only approved"):
        repository.save_approved(approval)
    assert repository.get(approval.invoice.invoice_id) is None


def test_duplicate_invoice_id_is_rejected(tmp_path: Path) -> None:
    repository = InvoiceRepository(tmp_path / "invoices.sqlite3")
    approval = approved_invoice()
    repository.save_approved(approval)

    with pytest.raises(PersistenceError, match="could not be persisted"):
        repository.save_approved(approval)
