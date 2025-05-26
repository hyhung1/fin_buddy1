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

# Define the relevant column names as per the dataset structure
sector_col = 'Sector L2\n'
ticker_col = 'Ticker\n'
company_name_col = 'Company Name\n'

net_profit_cols = [
    '18. Net profit/(loss) after tax\nYear: 2019\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2020\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2021\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2022\nUnit: Billions VND\n',
    '18. Net profit/(loss) after tax\nYear: 2023\nUnit: Billions VND\n',
]

owner_equity_cols = [
    'II. OWNER\'S EQUITY\nYear: 2019\nUnit: Billions VND\n',
    'II. OWNER\'S EQUITY\nYear: 2020\nUnit: Billions VND\n',
    'II. OWNER\'S EQUITY\nYear: 2021\nUnit: Billions VND\n',
    'II. OWNER\'S EQUITY\nYear: 2022\nUnit: Billions VND\n',
    'II. OWNER\'S EQUITY\nYear: 2023\nUnit: Billions VND\n',
]

minority_interests_cols = [
    '1.13. Minority interests\nYear: 2019\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2020\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2021\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2022\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2023\nUnit: Billions VND\n',
]

# Calculate Parent Equity for each year and store in new columns
parent_equity_cols = [f'Parent Equity {year}' for year in range(2019, 2024)]
for i in range(len(net_profit_cols)):
    df[parent_equity_cols[i]] = df[owner_equity_cols[i]] - df[minority_interests_cols[i]]

# Calculate total Net Profit across the years for ranking purposes
df['Total Net Profit 2019-2023'] = df[net_profit_cols].sum(axis=1)

# Function to get the top N rows within each group based on a specified column
def get_top_n_per_group(group, n, sort_col):
    return group.nlargest(n, sort_col)

# Group by sector and apply the function to get the top 3 companies in each sector
top_companies_per_sector = df.groupby(sector_col, group_keys=False).apply(
    lambda x: get_top_n_per_group(x, 3, 'Total Net Profit 2019-2023')
)

# Define the columns to include in the final output DataFrame
output_cols = [ticker_col, company_name_col, sector_col] + net_profit_cols + parent_equity_cols

# Select only the required columns for the top companies
result_df = top_companies_per_sector[output_cols]

# Print the results, iterating through the rows of the result DataFrame
for index, row in result_df.iterrows():
    print(f"Sector: {row[sector_col]}")
    print(f"Company: {row[ticker_col]} - {row[company_name_col]}")

    print("Net Profit (Billions VND):")
    for i, col in enumerate(net_profit_cols):
        year = 2019 + i
        print(f"{year}: {row[col]:.2f}")

    print("Parent Equity (Billions VND):")
    for i, col in enumerate(parent_equity_cols):
        year = 2019 + i
        print(f"{year}: {row[col]:.2f}")
    print("-" * 30) # Print a separator for readability
