"""Deterministic extraction and validation for synthetic invoices."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping


@dataclass(frozen=True)
class InvoiceLine:
    description: str
    quantity: Decimal
    unit_price: Decimal

    @property
    def amount(self) -> Decimal:
        return (self.quantity * self.unit_price).quantize(Decimal("0.01"))


@dataclass(frozen=True)
class Invoice:
    invoice_id: str
    vendor_name: str
    invoice_date: date
    due_date: date
    currency: str
    line_items: tuple[InvoiceLine, ...]
    subtotal: Decimal
    tax: Decimal
    total: Decimal


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: tuple[str, ...]


REQUIRED_FIELDS = (
    "invoice_id",
    "vendor_name",
    "invoice_date",
    "due_date",
    "currency",
    "line_items",
    "subtotal",
    "tax",
    "total",
)


def _money(value: Any, field: str) -> Decimal:
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError(f"{field} must be a numeric value") from exc
    if not amount.is_finite():
        raise ValueError(f"{field} must be a finite numeric value")
    return amount.quantize(Decimal("0.01"))


def _date(value: Any, field: str) -> date:
    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must use YYYY-MM-DD format") from exc


def extract_invoice(document: Mapping[str, Any]) -> Invoice:
    """Convert a synthetic document mapping into a typed invoice."""
    missing = [field for field in REQUIRED_FIELDS if field not in document]
    if missing:
        raise ValueError(f"missing required field(s): {', '.join(missing)}")

    raw_items = document["line_items"]
    if not isinstance(raw_items, list) or not raw_items:
        raise ValueError("line_items must be a non-empty list")

    items: list[InvoiceLine] = []
    for index, raw_item in enumerate(raw_items):
        if not isinstance(raw_item, Mapping):
            raise ValueError(f"line_items[{index}] must be an object")
        for field in ("description", "quantity", "unit_price"):
            if field not in raw_item:
                raise ValueError(f"line_items[{index}] is missing {field}")
        items.append(
            InvoiceLine(
                description=str(raw_item["description"]),
                quantity=_money(raw_item["quantity"], f"line_items[{index}].quantity"),
                unit_price=_money(raw_item["unit_price"], f"line_items[{index}].unit_price"),
            )
        )

    return Invoice(
        invoice_id=str(document["invoice_id"]),
        vendor_name=str(document["vendor_name"]),
        invoice_date=_date(document["invoice_date"], "invoice_date"),
        due_date=_date(document["due_date"], "due_date"),
        currency=str(document["currency"]).upper(),
        line_items=tuple(items),
        subtotal=_money(document["subtotal"], "subtotal"),
        tax=_money(document["tax"], "tax"),
        total=_money(document["total"], "total"),
    )


def validate_invoice(invoice: Invoice) -> ValidationResult:
    """Apply deterministic business rules to an extracted invoice."""
    errors: list[str] = []
    if not invoice.invoice_id.strip():
        errors.append("invoice_id must not be empty")
    if not invoice.vendor_name.strip():
        errors.append("vendor_name must not be empty")
    if invoice.due_date < invoice.invoice_date:
        errors.append("due_date must not be before invoice_date")
    if not invoice.currency.isalpha() or len(invoice.currency) != 3:
        errors.append("currency must be a three-letter code")
    if any(item.quantity <= 0 or item.unit_price < 0 for item in invoice.line_items):
        errors.append("line item quantities must be positive and prices non-negative")

    calculated_subtotal = sum((item.amount for item in invoice.line_items), Decimal("0.00"))
    if calculated_subtotal != invoice.subtotal:
        errors.append(
            f"subtotal conflict: expected {calculated_subtotal}, received {invoice.subtotal}"
        )
    calculated_total = (invoice.subtotal + invoice.tax).quantize(Decimal("0.01"))
    if calculated_total != invoice.total:
        errors.append(f"total conflict: expected {calculated_total}, received {invoice.total}")
    if invoice.tax < 0:
        errors.append("tax must be non-negative")

    return ValidationResult(valid=not errors, errors=tuple(errors))
