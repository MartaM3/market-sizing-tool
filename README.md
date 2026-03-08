# Market Sizing & Scenario Analysis Tool (Python)

Reproducible scenario analysis tool to estimate **TAM / SAM / SOM** under multiple growth assumptions and run a simple **sensitivity analysis**.

## Install (local)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```
## Run (CLI)
### Scenario results (with optional CSV export)
```bash
python -m market_sizing.cli \
  --tam 1e9 --sam 30 --som 5 \
  --growth Base=0.02 Optimistic=0.08 Pessimistic=-0.05 \
  --out results.csv
```
### Sensitivity grid
```bash
python -m market_sizing.cli \
  --tam 1e9 --sam 30 --som 5 \
  --growth Base=0.02 Optimistic=0.08 Pessimistic=-0.05 \
  --sensitivity --sens-out sensitivity.csv
```


## What it does
- Validates inputs (percent ranges, empty scenarios, etc.)
- Produces scenario tables (optional CSV export)
- Computes an optional sensitivity grid over assumptions

## Run tests
```bash
pytest -q
```
## Example output

```text
Scenario results:
   Scenario  GrowthRate           TAM           SAM           SOM
      Base       0.02  1020000000.0  306000000.0   15300000.0
 Optimistic    0.08  1080000000.0  324000000.0   16200000.0
Pessimistic   -0.05   950000000.0  285000000.0   14250000.0

