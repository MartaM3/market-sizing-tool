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


