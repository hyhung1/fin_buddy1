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

import pandas as pd

# Define the target sector, ensuring it matches the value in the dataset
target_sector = 'Oil & Gas'

# Define the relevant column names exactly as they appear in the DataFrame
ticker_col = 'Ticker\n'
sector_col = 'Sector L2\n'

# Define the net profit columns for the specified years
net_profit_cols = [
    '18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND\n'
]

# --- Step 1: Filter the DataFrame for the 'Oil & Gas' sector ---
# Use .str.strip() for robust comparison against sector names which might contain whitespace
oil_gas_df = df[df[sector_col].str.strip() == target_sector].copy()

# --- Step 2: Calculate the total net profit for the specified years for each company ---
# Sum the values across the net profit columns (axis=1) for each row in the filtered DataFrame
oil_gas_df['Total Net Profit 2019-2023'] = oil_gas_df[net_profit_cols].sum(axis=1)

# Store the name of the temporary column for easy access
total_net_profit_column_name = 'Total Net Profit 2019-2023'

# --- Step 3: Sort the companies by total net profit and select the top 5 ---
# Sort the filtered DataFrame by the calculated total net profit in descending order
# Use .head(5) to get the top 5 rows
top_5_oil_gas_companies = oil_gas_df.sort_values(by=total_net_profit_column_name, ascending=False).head(5)

# --- Step 4: Print the results ---
# Iterate through the rows of the DataFrame containing the top 5 companies
for index, row in top_5_oil_gas_companies.iterrows():
    # Print the Ticker (stripping any whitespace) and the Total Net Profit (formatted to two decimal places)
    print(f"Ticker: {row[ticker_col].strip()}, Total Net Profit 2019-2023: {row[total_net_profit_column_name]:.2f}")
