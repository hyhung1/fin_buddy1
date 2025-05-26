import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
df = pd.read_csv(r"C:\Users\HP\Downloads\excel_bud\fin_buddy\python_backend\uploads\2023Q4_Sheet1_processed_header7.csv")
# Make cleaned aliases for columns (whitespace variants) so any reference works
orig_cols = df.columns.tolist()
strip_cols = pd.Series(orig_cols).str.strip().tolist()
collapsed_cols = (pd.Series(orig_cols)
                 .str.replace(r"\s+", " ", regex=True)
                 .str.strip()
                 .tolist())
for orig, s, c in zip(orig_cols, strip_cols, collapsed_cols):
    if s not in orig_cols and s not in df.columns:
        df[s] = df[orig]
    if c not in orig_cols and c not in df.columns:
        df[c] = df[orig]
# Remove duplicate columns if any
df = df.loc[:, ~df.columns.duplicated()]
pd.set_option('display.float_format', '{:,.0f}'.format)

# Define the columns for Net Profit for each year from 2019 to 2023
net_profit_columns = [
    "18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND\n",
    "18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND\n",
    "18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND\n",
    "18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND\n",
    "18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND\n",
]

# Filter the DataFrame for the 'Oil & Gas' sector
# Using .copy() to avoid SettingWithCopyWarning when adding the new column
oil_gas_df = df[df['Sector L2\n'] == 'Oil & Gas'].copy()

# Calculate the sum of Net Profit for each company in the filtered DataFrame
# across the years 2019-2023. Use axis=1 to sum horizontally across the specified columns.
# Store this in a new column 'Total Net Profit 2019-2023'.
oil_gas_df['Total Net Profit 2019-2023'] = oil_gas_df[net_profit_columns].sum(axis=1)

# Sort the filtered DataFrame by the calculated total net profit in descending order
# and select the top 5 rows.
top_5_companies_oil_gas = oil_gas_df.sort_values(
    by='Total Net Profit 2019-2023',
    ascending=False
).head(5)

# Print the Ticker and Total Net Profit for the top 5 companies
print("Top 5 Companies in Oil & Gas by Total Net Profit (2019-2023):")
# Iterate through the rows of the resulting DataFrame using iterrows()
for index, row in top_5_companies_oil_gas.iterrows():
    # Access data using row['Column Name']
    ticker = row['Ticker\n']
    total_profit = row['Total Net Profit 2019-2023']
    print(f"{ticker}: {total_profit:.2f}")

# Note: The temporary column 'Total Net Profit 2019-2023' exists only in the oil_gas_df copy.
# It is not added to the original df, so no explicit drop is needed for df.
