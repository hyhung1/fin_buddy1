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

# Assume the DataFrame 'df' is already loaded as per the instructions.

# Define the columns for Net Profit for each year from 2019 to 2023
net_profit_cols_2019_2023 = [
    '18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND\n'
]

# Calculate the total net profit for each company across the specified years
# Use .sum(axis=1) to sum horizontally across the specified columns for each row
df['Total Net Profit 2019-2023'] = df[net_profit_cols_2019_2023].sum(axis=1)

# Group the DataFrame by the 'Sector L2\n' column
# Calculate the sum of the 'Total Net Profit 2019-2023' for each sector
sector_net_profit = df.groupby('Sector L2\n')['Total Net Profit 2019-2023'].sum()

# Sort the resulting Series in descending order and select the top 3 entries
top_3_sectors = sector_net_profit.sort_values(ascending=False).head(3)

# Print the result
# Iterate through the Series using .items() to get the index (sector) and value (profit)
for sector, profit in top_3_sectors.items():
    # Strip any leading/trailing whitespace from the sector name before printing
    print(f"{sector.strip()}: {profit:.2f}")
