import pandas as pd
import numpy as np

# Load the CSV file
df = pd.read_csv('cleaned_financial_data.csv')

# Ensure the 'Date' column is treated as a datetime object
df['Date'] = pd.to_datetime(df['Date'])

# Extract the 'Year' from the date (or use existing Year column if needed)
df['Year'] = df['Date'].dt.year

# Use Operating_Margin_Pct as a proxy for EBITDA Margin %
# (Operating Income is approximation of EBITDA when depreciation/amortization data is not available)
df['EBITDA_Margin_Percent'] = df['Operating_Margin_Pct']

# Group by Year and calculate annual aggregates
annual_summary = df.groupby('Year').agg({
    'Revenue': 'sum',
    'Gross_Profit': 'sum',
    'EBITDA_Margin_Percent': 'mean'
}).reset_index()

# Rename columns for clarity
annual_summary.columns = ['Year', 'Total_Revenue', 'Total_Gross_Profit', 'Average_EBITDA_Margin_Percent']

# Calculate Year-over-Year Revenue Growth Rate
annual_summary['Revenue_YoY_Growth_Percent'] = annual_summary['Total_Revenue'].pct_change() * 100

# Format financial metrics for better readability
annual_summary['Total_Revenue'] = annual_summary['Total_Revenue'].apply(lambda x: f"${x:,.2f}")
annual_summary['Total_Gross_Profit'] = annual_summary['Total_Gross_Profit'].apply(lambda x: f"${x:,.2f}")
annual_summary['Average_EBITDA_Margin_Percent'] = annual_summary['Average_EBITDA_Margin_Percent'].apply(lambda x: f"{x:.2f}%")
annual_summary['Revenue_YoY_Growth_Percent'] = annual_summary['Revenue_YoY_Growth_Percent'].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "N/A")

# Print the summary table to the terminal
print("=" * 130)
print("YEAR-OVER-YEAR FINANCIAL PERFORMANCE ANALYSIS")
print("=" * 130)
print(annual_summary.to_string(index=False))
print("=" * 130)

# Save the output to a CSV file
# Create a copy with original numeric values for CSV export
annual_summary_export = df.groupby('Year').agg({
    'Revenue': 'sum',
    'Gross_Profit': 'sum',
    'EBITDA_Margin_Percent': 'mean'
}).reset_index()

annual_summary_export.columns = ['Year', 'Total_Revenue', 'Total_Gross_Profit', 'Average_EBITDA_Margin_Percent']
annual_summary_export['Revenue_YoY_Growth_Percent'] = annual_summary_export['Total_Revenue'].pct_change() * 100

# Round numeric values for cleaner output
annual_summary_export['Total_Revenue'] = annual_summary_export['Total_Revenue'].round(2)
annual_summary_export['Total_Gross_Profit'] = annual_summary_export['Total_Gross_Profit'].round(2)
annual_summary_export['Average_EBITDA_Margin_Percent'] = annual_summary_export['Average_EBITDA_Margin_Percent'].round(2)
annual_summary_export['Revenue_YoY_Growth_Percent'] = annual_summary_export['Revenue_YoY_Growth_Percent'].round(2)

# Save to CSV
annual_summary_export.to_csv('annual_finance_summary.csv', index=False)
print("\n✓ Results saved to 'annual_finance_summary.csv'")
