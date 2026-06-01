# AI Learning — Financial Data Pipeline

This repository contains a compact, reproducible three-day workshop-style pipeline that demonstrates data engineering, time-series financial analysis, and presentation-ready visualizations using Python. The pipeline synthesizes monthly financial records, cleans and aggregates them, performs Year-over-Year (YoY) analysis, and produces charts suitable for executive reports.

**Key outputs:** cleaned monthly data, an annual performance summary, and two PNG charts.

**Files in this folder**

```
AI Learning/
├─ day1_automation.py              # Generate & clean synthetic monthly financial data
├─ cleaned_financial_data.csv     # Cleaned monthly dataset (output of Day 1)
├─ day2_analysis.py               # Annual aggregation + YoY calculations
├─ annual_finance_summary.csv     # Annual metrics summary (output of Day 2)
├─ day3_visualization.py          # Create and save professional charts
├─ monthly_financial_trends.png   # Line chart (Revenue vs Net Income)
└─ annual_profit_comparison.png   # Bar chart (Total Gross Profit by Year)
```

## Design & Data Pipeline Overview

The pipeline is intentionally simple and modular to emphasize good engineering choices and reproducibility across three focused stages:

- Day 1 — Data generation & cleaning (`day1_automation.py`)
	- Produces synthetic monthly time-series financial data for 36 months.
	- Detects and imputes missing values using *yearly medians* (see rationale below).
	- Calculates core financial metrics per row such as Gross Profit, EBITDA (where applicable), and Net Income.

- Day 2 — Aggregation & analysis (`day2_analysis.py`)
	- Ensures `Date` is parsed to a datetime type and extracts `Year`.
	- Aggregates monthly rows into annual totals (Total Revenue, Total Gross Profit) and computes the *average EBITDA margin* across months in the year.
	- Computes Year-over-Year percentage growth for Revenue.

- Day 3 — Visualization (`day3_visualization.py`)
	- Uses `matplotlib` and `seaborn` to produce two professional charts:
		1. Monthly line chart showing `Revenue` and `Net_Income` across the 36-month timeline.
		2. Annual bar chart comparing `Total Gross Profit` by `Year`.
	- Charts are saved as PNG files for embedding into presentations.

## Engineering Choices (Why these approaches?)

- Median imputation by year
	- Using the median computed within the same year protects seasonality (monthly patterns) while remaining robust to outliers.
	- Median is less sensitive to extreme synthetic values or one-off data glitches compared to a mean, so it preserves central tendency without skew.

- Per-year aggregation
	- Annual totals and average margins give executive-level, comparable KPIs and make YoY % growth straightforward to interpret.

- Using operating-income as a reasonable proxy when EBITDA is missing
	- Some source datasets may not provide an `EBITDA` column. When unavailable, the pipeline will fall back to `Operating_Income` for plotting/analysis with a clear note — this keeps the reporting flow uninterrupted while documenting the approximation.

- Clear artifact separation
	- Each stage produces a versioned artifact (`cleaned_financial_data.csv`, `annual_finance_summary.csv`, PNGs). This makes the pipeline auditable and re-runnable per stage.

## Prerequisites

- Python 3.8+ (this project was developed using Python 3.13)
- Install required packages (recommended in a virtual environment):

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install pandas numpy matplotlib seaborn
```

Note: If you prefer a single-line install, run:

```bash
pip install pandas numpy matplotlib seaborn
```

## How to run the pipeline (Day 1 → Day 3)

Run each step sequentially from the repository root.

1) Day 1 — Generate and clean monthly data

```bash
python day1_automation.py
```

This creates/overwrites `cleaned_financial_data.csv` with cleaned monthly rows and computed metrics.

2) Day 2 — Aggregate and calculate YoY metrics

```bash
python day2_analysis.py
```

This reads `cleaned_financial_data.csv`, produces `annual_finance_summary.csv`, and prints a formatted annual summary to the terminal.

3) Day 3 — Generate charts

```bash
python day3_visualization.py
```

This produces two images in the project root:

- `monthly_financial_trends.png` — monthly Revenue vs Net Income line chart
- `annual_profit_comparison.png` — annual Total Gross Profit bar chart

If `cleaned_financial_model.csv` exists, `day3_visualization.py` prefers it; otherwise it falls back to `cleaned_financial_data.csv`.

## Expected Outputs

- [cleaned_financial_data.csv](cleaned_financial_data.csv) — cleaned monthly dataset
- [annual_finance_summary.csv](annual_finance_summary.csv) — annual KPI summary
- [monthly_financial_trends.png](monthly_financial_trends.png) — monthly chart
- [annual_profit_comparison.png](annual_profit_comparison.png) — annual chart

## Troubleshooting

- KeyError: missing column
	- Ensure the CSVs contain the expected headers: `Date`, `Revenue`, `Gross_Profit`, `Operating_Income` or `Net_Income`, etc.
	- If `EBITDA` is missing, `day2_analysis.py` and `day3_visualization.py` may use `Operating_Income` as a proxy.

- Date parsing issues
	- Confirm the `Date` column follows an ISO-like format (e.g., `YYYY-MM-DD`). `pandas.to_datetime()` is used to parse dates.

- Visualization not showing or PNG files missing
	- Confirm that the scripts run without errors. The scripts save charts to the repository root; check console output for saved file names.

## Next steps & suggestions

- Add a `requirements.txt` or `pyproject.toml` for reproducible installs.
- Add unit tests around the data-cleaning step to validate imputation behavior.
- Add a short Jupyter notebook that loads the final CSV and renders figures inline for iterative exploration.

---

If you'd like, I can:

- generate a `requirements.txt` and update the README run commands, or
- add a short Jupyter notebook that reproduces the Day 3 charts inline for interactive exploration.

If you want any of those additions, tell me which one and I will add it.