"""Human approval state transitions for validated invoices."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

from document_intake.invoice import Invoice, ValidationResult


class ApprovalError(ValueError):
    """Raised when an approval transition or decision is invalid."""


class ApprovalStatus(StrEnum):
    EXTRACTED = "extracted"
    VALIDATED = "validated"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass(frozen=True)
class ApprovalDecision:
    status: ApprovalStatus
    reviewer: str
    decided_at: datetime
    reason: str | None = None


class InvoiceApproval:
    """Manage the human-review boundary for one extracted invoice."""

    def __init__(self, invoice: Invoice, validation: ValidationResult) -> None:
        self.invoice = invoice
        self.validation = validation
        self.status = ApprovalStatus.EXTRACTED
        self.decision: ApprovalDecision | None = None

    def mark_validated(self) -> None:
        self._require_status(ApprovalStatus.EXTRACTED)
        if not self.validation.valid:
            raise ApprovalError("invalid invoices cannot enter the approval workflow")
        self.status = ApprovalStatus.VALIDATED

    def submit_for_review(self) -> None:
        self._require_status(ApprovalStatus.VALIDATED)
        self.status = ApprovalStatus.PENDING_REVIEW

    def approve(self, reviewer: str, decided_at: datetime | None = None) -> ApprovalDecision:
        self._require_status(ApprovalStatus.PENDING_REVIEW)
        self._require_reviewer(reviewer)
        self.decision = ApprovalDecision(
            status=ApprovalStatus.APPROVED,
            reviewer=reviewer.strip(),
            decided_at=decided_at or datetime.now(UTC),
        )
        self.status = ApprovalStatus.APPROVED
        return self.decision

    def reject(
        self,
        reviewer: str,
        reason: str,
        decided_at: datetime | None = None,
    ) -> ApprovalDecision:
        self._require_status(ApprovalStatus.PENDING_REVIEW)
        self._require_reviewer(reviewer)
        if not reason.strip():
            raise ApprovalError("a rejection reason is required")
        self.decision = ApprovalDecision(
            status=ApprovalStatus.REJECTED,
            reviewer=reviewer.strip(),
            decided_at=decided_at or datetime.now(UTC),
            reason=reason.strip(),
        )
        self.status = ApprovalStatus.REJECTED
        return self.decision

    def _require_status(self, expected: ApprovalStatus) -> None:
        if self.status != expected:
            raise ApprovalError(f"cannot transition from {self.status} to this operation")

    @staticmethod
    def _require_reviewer(reviewer: str) -> None:
        if not reviewer.strip():
            raise ApprovalError("reviewer is required")
