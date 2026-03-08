import pytest

from market_sizing.core import compute_tam_sam_som, sensitivity_grid


def test_compute_tam_sam_som_outputs_three_scenarios():
    res = compute_tam_sam_som(
        tam=1000.0,
        sam_percent=50.0,
        som_percent=10.0,
        growth_rates={"Base": 0.0, "Optimistic": 0.1, "Pessimistic": -0.1},
    )
    df = res.table
    assert len(df) == 3
    assert set(df.columns) == {"Scenario", "GrowthRate", "TAM", "SAM", "SOM"}


def test_invalid_percent_raises():
    with pytest.raises(ValueError):
        compute_tam_sam_som(
            tam=1000.0,
            sam_percent=120.0,
            som_percent=10.0,
            growth_rates={"Base": 0.0},
        )


def test_sensitivity_grid_nonempty():
    grid = sensitivity_grid(
        tam=1000.0,
        sam_percent=50.0,
        som_percent_values=[1, 5, 10],
        growth_values=[-0.05, 0.0, 0.05],
    )
    assert len(grid) == 3 * 3
    assert set(grid.columns) == {"SOM%", "GrowthRate", "SOM"}
