# AI CFO Agent

Auditable finance-analysis assistant that detects adverse budget variances and generates an executive briefing.

**Synthetic-data portfolio demonstration.** Analysis is deterministic and rules-based; no LLM calls or autonomous external actions.

## Quick start
```bash
pip install -r requirements.txt
python -m cfo_agent.cli --input data/sample_financials.csv --output executive_brief.md
```

## Tests
```bash
pip install pytest
pytest -q
```

CSV: month, department, category (revenue/expense), actual, budget. All figures nonnegative. Operating result is not a GAAP income statement. Never use confidential data.