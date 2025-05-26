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

# Identify the relevant net profit columns for the years 2019 to 2023.
net_profit_columns = [
    '18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND',
    '18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND',
    '18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND',
    '18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND',
    '18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND'
]

# Group the DataFrame by 'Sector L2\n' and calculate the sum of net profit for each year for each sector.
sector_yearly_profits = df.groupby('Sector L2\n')[net_profit_columns].sum()

# Calculate the total net profit for each sector over the entire period (2019-2023) by summing across the columns.
sector_total_profit = sector_yearly_profits.sum(axis=1)

# Sort the sectors by their total net profit in descending order.
sorted_sectors = sector_total_profit.sort_values(ascending=False)

# Get the top 5 sectors.
top_5_sectors = sorted_sectors.head(5)

# Print the top 5 sectors and their total net profit.
for sector, total_profit in top_5_sectors.items():
    print(f"{sector}: {total_profit:.2f}")
