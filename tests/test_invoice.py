import json
from pathlib import Path

import pytest

from document_intake.invoice import extract_invoice, validate_invoice

DATA = Path(__file__).parents[1] / "sample-data"


def load_fixture(name: str) -> dict:
    return json.loads((DATA / name).read_text())


def test_valid_invoice_extracts_and_validates() -> None:
    invoice = extract_invoice(load_fixture("invoice-valid.json"))
    result = validate_invoice(invoice)
    assert result.valid
    assert invoice.total == invoice.subtotal + invoice.tax


def test_missing_field_is_rejected() -> None:
    with pytest.raises(ValueError, match="missing required field.*tax"):
        extract_invoice(load_fixture("invoice-missing-field.json"))


def test_malformed_value_is_rejected() -> None:
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        extract_invoice(load_fixture("invoice-malformed.json"))


def test_conflicting_total_fails_validation() -> None:
    result = validate_invoice(extract_invoice(load_fixture("invoice-conflicting-total.json")))
    assert not result.valid
    assert "total conflict" in result.errors[0]
