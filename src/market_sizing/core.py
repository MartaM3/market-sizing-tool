from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

import pandas as pd


@dataclass(frozen=True)
class ScenarioResult:
    """Container for scenario outputs."""
    table: pd.DataFrame


def _validate_percent(name: str, value: float) -> None:
    if value < 0 or value > 100:
        raise ValueError(f"{name} must be between 0 and 100. Got {value}.")


def compute_tam_sam_som(
    tam: float,
    sam_percent: float,
    som_percent: float,
    growth_rates: Dict[str, float],
) -> ScenarioResult:
    """
    Compute TAM/SAM/SOM under multiple growth scenarios.

    Args:
        tam: Total Addressable Market (base value, e.g. EUR).
        sam_percent: % of TAM that is serviceable (0..100).
        som_percent: % of SAM expected to be captured (0..100).
        growth_rates: dict like {"Pessimistic": -0.05, "Base": 0.02, "Optimistic": 0.08}
                     values are growth rates in decimal form.

    Returns:
        ScenarioResult with a table containing TAM/SAM/SOM per scenario.
    """
    if tam < 0:
        raise ValueError("TAM must be >= 0.")
    _validate_percent("SAM %", sam_percent)
    _validate_percent("SOM %", som_percent)
    if not growth_rates:
        raise ValueError("growth_rates cannot be empty.")

    sam_ratio = sam_percent / 100.0
    som_ratio = som_percent / 100.0

    rows: List[dict] = []
    for scenario, g in growth_rates.items():
        g = float(g)
        scenario_tam = tam * (1.0 + g)
        scenario_sam = scenario_tam * sam_ratio
        scenario_som = scenario_sam * som_ratio

        rows.append(
            {
                "Scenario": str(scenario),
                "GrowthRate": g,
                "TAM": scenario_tam,
                "SAM": scenario_sam,
                "SOM": scenario_som,
            }
        )

    df = pd.DataFrame(rows).sort_values("Scenario").reset_index(drop=True)
    return ScenarioResult(table=df)


def sensitivity_grid(
    tam: float,
    sam_percent: float,
    som_percent_values: Iterable[float],
    growth_values: Iterable[float],
) -> pd.DataFrame:
    """
    Simple sensitivity analysis grid over SOM% and growth rate.
    Useful to show how SOM changes under assumptions (very quant-friendly).
    """
    if tam < 0:
        raise ValueError("TAM must be >= 0.")
    _validate_percent("SAM %", sam_percent)

    som_vals = list(som_percent_values)
    growth_vals = list(growth_values)
    if not som_vals or not growth_vals:
        raise ValueError("som_percent_values and growth_values must be non-empty.")

    for v in som_vals:
        _validate_percent("SOM %", float(v))

    sam_ratio = sam_percent / 100.0

    rows: List[dict] = []
    for som_percent in som_vals:
        som_ratio = float(som_percent) / 100.0
        for g in growth_vals:
            g = float(g)
            scenario_tam = tam * (1.0 + g)
            scenario_sam = scenario_tam * sam_ratio
            scenario_som = scenario_sam * som_ratio
            rows.append(
                {
                    "SOM%": float(som_percent),
                    "GrowthRate": g,
                    "SOM": scenario_som,
                }
            )

    return pd.DataFrame(rows)
