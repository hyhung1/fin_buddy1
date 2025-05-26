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

# Define the net profit columns for the years 2019 to 2023
net_profit_cols = [
    '18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND\n'
]

# Select the relevant columns: Sector and the net profit columns
cols_to_use = ['Sector L2\n'] + net_profit_cols
df_subset = df[cols_to_use]

# Group by 'Sector L2\n' and calculate the sum of net profits for each year
sector_yearly_profit = df_subset.groupby('Sector L2\n')[net_profit_cols].sum()

# Calculate the total net profit for each sector over the entire period (2019-2023)
total_sector_profit = sector_yearly_profit.sum(axis=1)

# Get the top 5 sectors based on the total net profit
top_5_sectors = total_sector_profit.nlargest(5)

# Print the result
for sector, profit in top_5_sectors.items():
    print(f"{sector}: {profit:.2f}")
