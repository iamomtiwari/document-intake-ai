import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from document_intake.approval import ApprovalError, ApprovalStatus, InvoiceApproval
from document_intake.invoice import extract_invoice, validate_invoice

DATA = Path(__file__).parents[1] / "sample-data"


def load_invoice(name: str = "invoice-valid.json"):
    document = json.loads((DATA / name).read_text())
    return extract_invoice(document)


def test_valid_invoice_can_be_approved_by_a_reviewer() -> None:
    approval = InvoiceApproval(load_invoice(), validate_invoice(load_invoice()))
    decided_at = datetime(2026, 1, 20, tzinfo=UTC)

    approval.mark_validated()
    approval.submit_for_review()
    decision = approval.approve("reviewer@example.test", decided_at)

    assert approval.status is ApprovalStatus.APPROVED
    assert decision.reviewer == "reviewer@example.test"
    assert decision.decided_at == decided_at
    assert decision.reason is None


def test_reviewer_can_reject_with_a_reason() -> None:
    invoice = load_invoice()
    approval = InvoiceApproval(invoice, validate_invoice(invoice))
    approval.mark_validated()
    approval.submit_for_review()

    decision = approval.reject("reviewer@example.test", "Vendor name needs confirmation")

    assert approval.status is ApprovalStatus.REJECTED
    assert decision.reason == "Vendor name needs confirmation"


def test_invalid_invoice_cannot_enter_approval_workflow() -> None:
    invoice = load_invoice("invoice-conflicting-total.json")
    approval = InvoiceApproval(invoice, validate_invoice(invoice))

    with pytest.raises(ApprovalError, match="invalid invoices"):
        approval.mark_validated()


def test_approval_requires_review_and_cannot_be_repeated() -> None:
    invoice = load_invoice()
    approval = InvoiceApproval(invoice, validate_invoice(invoice))

    with pytest.raises(ApprovalError, match="extracted"):
        approval.approve("reviewer@example.test")

    approval.mark_validated()
    approval.submit_for_review()
    approval.approve("reviewer@example.test")

    with pytest.raises(ApprovalError, match="approved"):
        approval.reject("reviewer@example.test", "Too late")


def test_rejection_requires_reviewer_and_reason() -> None:
    invoice = load_invoice()
    approval = InvoiceApproval(invoice, validate_invoice(invoice))
    approval.mark_validated()
    approval.submit_for_review()

    with pytest.raises(ApprovalError, match="reviewer"):
        approval.reject("", "Missing supporting detail")
    with pytest.raises(ApprovalError, match="reason"):
        approval.reject("reviewer@example.test", " ")
