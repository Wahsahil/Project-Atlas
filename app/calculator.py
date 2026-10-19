
from typing import Any


def calculate_cagr_projection(
    base_value: float,
    cagr_percent: float,
    years: int,
    base_year: int | None = None,
    target_year: int | None = None,
) -> dict[str, Any]:
    """Project a market value using compound annual growth."""

    if base_value < 0:
        raise ValueError("Base value cannot be negative.")

    if cagr_percent <= -100:
        raise ValueError("CAGR must be greater than -100%.")

    if years < 0:
        raise ValueError("Years cannot be negative.")

    if base_year is not None and target_year is not None:
        if target_year < base_year:
            raise ValueError("Target year cannot precede base year.")
        if target_year - base_year != years:
            raise ValueError("Years must equal target_year - base_year.")

    projected_value = base_value * (
        1 + cagr_percent / 100
    ) ** years

    return {
        "base_value": round(base_value, 4),
        "cagr_percent": cagr_percent,
        "years": years,
        "base_year": base_year,
        "target_year": target_year,
        "projected_value": round(projected_value, 4),
        "formula": "base_value * (1 + CAGR / 100) ** years",
    }
