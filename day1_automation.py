import pandas as pd
import numpy as np

# Set random seed for consistent data
np.random.seed(42)

# Create 36 months of dates (3 years)
dates = pd.date_range(start="2023-01-01", periods=36, freq="MS")

# Generate mock financial data
revenue = np.random.randint(50000, 120000, size=36)
cogs = (revenue * np.random.uniform(0.4, 0.55, size=36)).astype(int)
operating_expenses = np.random.randint(15000, 30000, size=36)

# Create DataFrame
df = pd.DataFrame({
    'Date': dates,
    'Revenue': revenue,
    'COGS': cogs,
    'Operating_Expenses': operating_expenses
})

# Intentionally introduce a few "messy" null values to simulate real-world data cleaning
df.loc[5, 'Revenue'] = np.nan
df.loc[18, 'COGS'] = np.nan

# Save to your local directory as a CSV file
df.to_csv('raw_financial_data.csv', index=False)
print("SUCCESS: 'raw_financial_data.csv' has been created in your folder!")
