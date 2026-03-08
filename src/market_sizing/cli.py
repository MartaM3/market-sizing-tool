from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

from market_sizing.core import compute_tam_sam_som, sensitivity_grid


def _parse_growth_pairs(pairs: List[str]) -> Dict[str, float]:
    """
    Parse list like ["Base=0.02", "Optimistic=0.08", "Pessimistic=-0.05"].
    """
    out: Dict[str, float] = {}
    for p in pairs:
        if "=" not in p:
            raise argparse.ArgumentTypeError(
                "Growth scenarios must be provided as Name=value (e.g., Base=0.02)."
            )
        name, val = p.split("=", 1)
        name = name.strip()
        if not name:
            raise argparse.ArgumentTypeError("Scenario name cannot be empty.")
        out[name] = float(val)
    return out


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scenario analysis tool to compute TAM/SAM/SOM under growth scenarios."
    )
    parser.add_argument("--tam", type=float, required=True, help="Base TAM (e.g., 1e9).")
    parser.add_argument("--sam", type=float, required=True, help="SAM percentage of TAM (0-100).")
    parser.add_argument("--som", type=float, required=True, help="SOM percentage of SAM (0-100).")

    parser.add_argument(
        "--growth",
        nargs="+",
        required=True,
        metavar="SCEN=RATE",
        help="Growth scenarios as Name=value (e.g., Base=0.02 Optimistic=0.08 Pessimistic=-0.05).",
    )

    parser.add_argument(
        "--out",
        type=str,
        default="",
        help="Optional path to write scenario results CSV (e.g., results.csv).",
    )

    parser.add_argument(
        "--sensitivity",
        action="store_true",
        help="Also compute a simple sensitivity grid over SOM% and growth.",
    )
    parser.add_argument(
        "--som-grid",
        nargs="+",
        type=float,
        default=[1, 2, 5, 10],
        help="SOM%% values for sensitivity grid (default: 1 2 5 10).",
    )
    parser.add_argument(
        "--growth-grid",
        nargs="+",
        type=float,
        default=[-0.05, 0.0, 0.05, 0.1],
        help="Growth values for sensitivity grid (default: -0.05 0 0.05 0.1).",
    )
    parser.add_argument(
        "--sens-out",
        type=str,
        default="",
        help="Optional path to write sensitivity grid CSV.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    growth_rates = _parse_growth_pairs(args.growth)

    result = compute_tam_sam_som(
        tam=args.tam,
        sam_percent=args.sam,
        som_percent=args.som,
        growth_rates=growth_rates,
    )

    df = result.table
    print("\nScenario results:")
    print(df.to_string(index=False))

    if args.out:
        out_path = Path(args.out)
        df.to_csv(out_path, index=False)
        print(f"\nSaved scenario results to: {out_path}")

    if args.sensitivity:
        sens = sensitivity_grid(
            tam=args.tam,
            sam_percent=args.sam,
            som_percent_values=args.som_grid,
            growth_values=args.growth_grid,
        )
        print("\nSensitivity grid (SOM as function of SOM% and GrowthRate):")
        print(sens.to_string(index=False))

        if args.sens_out:
            sens_path = Path(args.sens_out)
            sens.to_csv(sens_path, index=False)
            print(f"\nSaved sensitivity grid to: {sens_path}")


if __name__ == "__main__":
    main()
