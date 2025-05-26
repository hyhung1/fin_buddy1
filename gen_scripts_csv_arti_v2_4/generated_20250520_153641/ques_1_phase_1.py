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

# Define the columns for net profit from 2019 to 2023
net_profit_cols = [
    '18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND\n'
]

# Define key columns
ticker_col = 'Ticker\n'
sector_col = 'Sector L2\n'
target_sector = 'Oil & Gas'

# Filter the DataFrame for the 'Oil & Gas' sector
# Use .copy() to avoid SettingWithCopyWarning
oil_gas_df = df[df[sector_col] == target_sector].copy()

# Calculate the total net profit for each company within the filtered sector
# Use fillna(0) to handle potential missing values before summing
oil_gas_df['Total Net Profit 2019-2023'] = oil_gas_df[net_profit_cols].fillna(0).sum(axis=1)

# Sort companies by total net profit in descending order and select the top 5
top_5_oil_gas_companies = oil_gas_df.sort_values(by='Total Net Profit 2019-2023', ascending=False).head(5)

# Select the Ticker and the calculated Total Net Profit columns for printing
result_df = top_5_oil_gas_companies[[ticker_col, 'Total Net Profit 2019-2023']]

# Print the result
for index, row in result_df.iterrows():
    print(f"{row[ticker_col].strip()}: {row['Total Net Profit 2019-2023']:.2f}")
