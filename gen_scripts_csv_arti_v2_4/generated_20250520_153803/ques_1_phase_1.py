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

# Define the relevant columns, ensuring exact names including newlines/spaces
net_profit_cols = [
    '18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND\n'
]

owner_equity_cols = [
    'II. OWNER\'S EQUITY\nYear: 2019\nUnit: Billions VND\n',
    'II. OWNER\'S EQUITY\nYear: 2020\nUnit: Billions VND\n',
    'II. OWNER\'S EQUITY\nYear: 2021\nUnit: Billions VND\n',
    'II. OWNER\'S EQUITY\nYear: 2022\nUnit: Billions VND\n',
    'II. OWNER\'S EQUITY\nYear: 2023\nUnit: Billions VND\n'
]

minority_interests_cols = [
    '1.13. Minority interests\nYear: 2019\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2020\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2021\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2022\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2023\nUnit: Billions VND\n'
]

years = ['2019', '2020', '2021', '2022', '2023']
parent_equity_year_cols = []

# Calculate Parent Equity for each year and create new columns
for i, year in enumerate(years):
    parent_equity_col_name = f'Parent Equity {year}'
    df[parent_equity_col_name] = df[owner_equity_cols[i]] - df[minority_interests_cols[i]]
    parent_equity_year_cols.append(parent_equity_col_name)

# Calculate cumulative net profit for 2019-2023
df['Cumulative Net Profit 2019-2023'] = df[net_profit_cols].sum(axis=1)

# Define the target sectors
target_sectors = ['Banks', 'Real Estate', 'Food & Beverage']

# Filter DataFrame for the target sectors
df_filtered = df[df['Sector L2\n'].isin(target_sectors)].copy()

# Find top 3 companies in each sector based on cumulative net profit
# Using group_keys=False to avoid the original group keys becoming part of the index unnecessarily
top_companies_by_sector = df_filtered.groupby('Sector L2\n', group_keys=False).apply(lambda group: group.nlargest(3, 'Cumulative Net Profit 2019-2023'))

# Select the Ticker and Parent Equity columns for these top companies
result_df = top_companies_by_sector[['Ticker\n'] + parent_equity_year_cols + ['Sector L2\n', 'Cumulative Net Profit 2019-2023']]

# Print the results grouped by sector
for sector in target_sectors:
    print(f"Sector: {sector}")
    # Filter results for the current sector
    sector_results = result_df[result_df['Sector L2\n'] == sector]

    # Sort by cumulative profit descending to present clearly
    sector_results_sorted = sector_results.sort_values(by='Cumulative Net Profit 2019-2023', ascending=False)

    for index, row in sector_results_sorted.iterrows():
        ticker = row['Ticker\n']
        # Optional: Print cumulative profit for context
        # cumulative_profit = row['Cumulative Net Profit 2019-2023']
        # print(f"  Ticker: {ticker} (Cumulative Profit: {cumulative_profit:.2f})")
        print(f"  Ticker: {ticker}")
        for i, year in enumerate(years):
            print(f"    Parent Equity {year}: {row[parent_equity_year_cols[i]]:.2f}")
