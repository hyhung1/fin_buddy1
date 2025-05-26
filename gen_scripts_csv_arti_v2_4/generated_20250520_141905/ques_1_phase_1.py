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

# Define column names based on the provided list, handling potential trailing newlines/spaces
sector_col = 'Sector L2\n'
ticker_col = 'Ticker\n'
company_col = 'Company Name\n'
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
minority_interest_cols = [
    '1.13. Minority interests\nYear: 2019\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2020\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2021\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2022\nUnit: Billions VND\n',
    '1.13. Minority interests\nYear: 2023\nUnit: Billions VND\n'
]
parent_equity_years = [2019, 2020, 2021, 2022, 2023]
parent_equity_cols_derived = [f'Parent Equity {year}' for year in parent_equity_years]


# Calculate Total Net Profit from 2019 to 2023 for each company
df['Total Net Profit 2019-2023'] = df[net_profit_cols].sum(axis=1)

# Calculate Parent Equity for each year
for i, year in enumerate(parent_equity_years):
    df[parent_equity_cols_derived[i]] = df[owner_equity_cols[i]] - df[minority_interest_cols[i]]

# Get unique sectors
sectors = df[sector_col].unique()

# Iterate through each sector to find top companies
for sector_name in sectors:
    # Filter df for the current sector, use .copy() to avoid SettingWithCopyWarning
    sector_df = df[df[sector_col] == sector_name].copy()

    if not sector_df.empty:
        # Find the top 3 companies by total net profit within the sector
        # Ensure the total profit column exists in the subset DataFrame
        top_companies_in_sector = sector_df.nlargest(3, 'Total Net Profit 2019-2023')

        if not top_companies_in_sector.empty:
            # Print sector header (strip sector name as it comes from column unique values)
            print(f"Sector: {sector_name.strip()}")

            # Iterate through the top companies in this sector
            # iterrows() is appropriate for iterating over DataFrame rows
            for index, row in top_companies_in_sector.iterrows():
                # Print company details (cell values assumed clean, no strip needed)
                print(f"  Ticker: {row[ticker_col]}")
                print(f"  Company Name: {row[company_col]}")
                print(f"  Total Net Profit (2019-2023): {row['Total Net Profit 2019-2023']:.2f}")

                # Print Parent Equity for each year
                equity_output_parts = []
                for i, year in enumerate(parent_equity_years):
                    # Access the derived column by name
                    equity_value = row[parent_equity_cols_derived[i]]
                    equity_output_parts.append(f"{year}: {equity_value:.2f}")
                print("  Parent Equity (Billions VND): " + ", ".join(equity_output_parts))

            print("-" * 30) # Separator between sectors
