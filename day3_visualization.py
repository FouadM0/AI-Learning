import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter, MonthLocator
from matplotlib.ticker import FuncFormatter

sns.set_style('whitegrid')
plt.rcParams.update({'figure.dpi': 120})

# File names
monthly_csv_candidate = 'cleaned_financial_model.csv'
fallback_csv = 'cleaned_financial_data.csv'
annual_csv = 'annual_finance_summary.csv'

monthly_output = 'monthly_financial_trends.png'
annual_output = 'annual_profit_comparison.png'

# Load monthly data (use fallback if candidate not found)
if os.path.exists(monthly_csv_candidate):
    monthly_csv = monthly_csv_candidate
else:
    monthly_csv = fallback_csv
    print(f"Note: '{monthly_csv_candidate}' not found — using '{fallback_csv}' as fallback.")

if not os.path.exists(monthly_csv):
    raise FileNotFoundError(f"Monthly CSV not found: {monthly_csv}")

monthly_df = pd.read_csv(monthly_csv)
if 'Date' not in monthly_df.columns:
    raise KeyError("'Date' column not found in monthly CSV")

monthly_df['Date'] = pd.to_datetime(monthly_df['Date'])
monthly_df = monthly_df.sort_values('Date')

# Ensure Net_Income exists (fallback to Operating_Income if needed)
if 'Net_Income' not in monthly_df.columns:
    if 'Operating_Income' in monthly_df.columns:
        monthly_df['Net_Income'] = monthly_df['Operating_Income']
        print("Note: 'Net_Income' not found — using 'Operating_Income' as proxy for plotting.")
    else:
        raise KeyError("Neither 'Net_Income' nor 'Operating_Income' found in monthly CSV")

# Chart 1: Monthly Revenue and Net Income line chart
fig, ax = plt.subplots(figsize=(12, 6))

sns.lineplot(data=monthly_df, x='Date', y='Revenue', marker='o', label='Revenue', ax=ax)
sns.lineplot(data=monthly_df, x='Date', y='Net_Income', marker='o', label='Net Income', ax=ax)

# Date formatting on x-axis
ax.xaxis.set_major_locator(MonthLocator(interval=2))
ax.xaxis.set_major_formatter(DateFormatter('%b %Y'))
plt.xticks(rotation=45, ha='right')

ax.set_title('Monthly Revenue and Net Income Trends')
ax.set_xlabel('Date')
ax.set_ylabel('Amount (USD)')
ax.legend()
plt.tight_layout()
plt.savefig(monthly_output, bbox_inches='tight', dpi=300)
plt.close(fig)
print(f"Saved monthly chart to '{monthly_output}'")

# Load annual summary
if not os.path.exists(annual_csv):
    raise FileNotFoundError(f"Annual summary CSV not found: {annual_csv}")

annual_df = pd.read_csv(annual_csv)

# Ensure expected columns exist
gross_col = None
for c in ['Total_Gross_Profit', 'Total_GrossProfit', 'Gross_Profit']:
    if c in annual_df.columns:
        gross_col = c
        break
if gross_col is None:
    raise KeyError("Couldn't find a Total Gross Profit column in annual CSV")

# Chart 2: Annual Total Gross Profit bar chart
fig, ax = plt.subplots(figsize=(8, 6))

# Convert Year to string for categorical x-axis
annual_df['Year'] = annual_df['Year'].astype(str)

sns.barplot(data=annual_df, x='Year', y=gross_col, palette='Blues_d', ax=ax)

# Format y-axis as currency
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x:,.0f}"))

ax.set_title('Annual Total Gross Profit by Year')
ax.set_xlabel('Year')
ax.set_ylabel('Total Gross Profit (USD)')
plt.tight_layout()
plt.savefig(annual_output, bbox_inches='tight', dpi=300)
plt.close(fig)
print(f"Saved annual chart to '{annual_output}'")

print('\nAll done.')
