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

# Select the columns for Sector and Net Profit for years 2019 to 2023
net_profit_cols = [
    '18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND\n'
]
sector_col = 'Sector L2\n'

# Calculate the total net profit for each company across the selected years
# Summing across axis=1 calculates the row sum
df['Total Net Profit 2019-2023'] = df[net_profit_cols].sum(axis=1)

# Group the DataFrame by the Sector column and sum the total net profit for each sector
sector_total_profit = df.groupby(sector_col)['Total Net Profit 2019-2023'].sum()

# Sort the sectors by their total net profit in descending order
sorted_sectors = sector_total_profit.sort_values(ascending=False)

# Get the top 3 sectors
top_3_sectors = sorted_sectors.head(3)

# Print the top 3 sectors and their total net profit
# Use .items() to iterate over the Series
for sector, profit in top_3_sectors.items():
    print(f"{sector}: {profit:.2f}")
