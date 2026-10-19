
import pytest

from app.calculator import calculate_cagr_projection


def test_market_projection():
    result = calculate_cagr_projection(
        base_value=4.21,
        cagr_percent=11.2,
        years=6,
        base_year=2024,
        target_year=2030,
    )

    expected = round(4.21 * (1.112 ** 6), 2)

    assert result["projected_value"] == pytest.approx(expected)


def test_rejects_negative_years():
    with pytest.raises(ValueError):
        calculate_cagr_projection(4.21, 11.2, -1)


def test_rejects_inconsistent_years():
    with pytest.raises(ValueError):
        calculate_cagr_projection(
            4.21,
            11.2,
            6,
            base_year=2024,
            target_year=2029,
        )
