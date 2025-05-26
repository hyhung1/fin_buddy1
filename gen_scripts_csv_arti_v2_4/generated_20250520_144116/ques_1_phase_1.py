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

# Define the exact column names from the dataset structure
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

years = [2019, 2020, 2021, 2022, 2023]
parent_equity_calc_cols = [f'Parent Equity {year}' for year in years] # Names for the calculated columns

# Check which net profit columns actually exist in the DataFrame
net_profit_cols_exist = [col for col in net_profit_cols if col in df.columns]

# 1. Calculate total net profit for 2019-2023 for each company
if net_profit_cols_exist:
    # Calculate sum only if relevant columns are present
    df['Total Net Profit 2019-2023'] = df[net_profit_cols_exist].sum(axis=1)
    total_net_profit_col = 'Total Net Profit 2019-2023'
else:
    # If no net profit columns exist, we cannot proceed with ranking by profit
    print("Error: Net profit columns not found in DataFrame.")
    total_net_profit_col = None # Indicate that this column was not created

if total_net_profit_col:
    # 2. Define the target sectors (from the previous output)
    target_sectors = ['Banks', 'Real Estate', 'Food & Beverage']

    # 3. Filter DataFrame to include only the target sectors
    # Use .copy() to avoid SettingWithCopyWarning in subsequent assignments
    filtered_df = df[df[sector_col].isin(target_sectors)].copy()

    # 4. Group by sector and find the top 3 companies by total net profit
    # Ensure the grouping column and the ranking column exist before applying nlargest
    if sector_col in filtered_df.columns and total_net_profit_col in filtered_df.columns:
        # Use group_keys=False to prevent the sector name from becoming an extra index level
        top_companies_per_sector = filtered_df.groupby(sector_col, group_keys=False).apply(
            lambda x: x.nlargest(3, total_net_profit_col)
        )

        # 5. Calculate Parent Equity for each year for the top companies
        # Ensure we have the correct number of owner and minority columns
        if len(owner_equity_cols) == len(minority_interests_cols) == len(years):
            for i, year in enumerate(years):
                owner_col = owner_equity_cols[i]
                minority_col = minority_interests_cols[i]
                parent_col_name = parent_equity_calc_cols[i]

                # Ensure both owner_col and minority_col exist in the DataFrame before calculating
                if owner_col in top_companies_per_sector.columns and minority_col in top_companies_per_sector.columns:
                    # Calculate Parent Equity
                    top_companies_per_sector[parent_col_name] = top_companies_per_sector[owner_col] - top_companies_per_sector[minority_col]
                else:
                    # Assign NaN if source columns are missing for that year
                    top_companies_per_sector[parent_col_name] = pd.NA
        else:
            print("Warning: Mismatch in number of owner/minority columns or years.")


        # 6. Select the relevant columns for output and sort
        output_cols_base = [sector_col, ticker_col, company_name_col] + parent_equity_calc_cols
        # Ensure all columns we intend to print actually exist in the result DataFrame
        output_cols_exist = [col for col in output_cols_base if col in top_companies_per_sector.columns]

        result_df = top_companies_per_sector[output_cols_exist].sort_values(
            by=[sector_col, total_net_profit_col], ascending=[True, False]
        )

        # 7. Print the results
        # Convert the DataFrame to a list of dictionaries or similar structure for easier iteration if needed,
        # but iterating rows directly is also fine.
        # Iterating using iterrows() as requested in guidelines
        for index, row in result_df.iterrows():
            sector = row[sector_col].strip() # Use strip() to clean potential newline/whitespace
            ticker = row[ticker_col].strip()
            company = row[company_name_col].strip()

            print(f"Sector: {sector}")
            print(f"  Ticker: {ticker}")
            print(f"  Company: {company}")
            print("  Parent Equity:")

            for year in years:
                parent_col_name = f'Parent Equity {year}'
                if parent_col_name in row.index: # Check if the calculated column exists in the row
                    value = row[parent_col_name]
                    if pd.notna(value): # Check if the calculated value is not NaN
                        print(f"    {year}: {value:.2f}")
                    else:
                        print(f"    {year}: N/A (Data Missing)")
                else:
                     print(f"    {year}: Calculation column not found")

    else:
        print("Required columns for grouping or ranking are missing after filtering.")
else:
    # Message already printed above if total_net_profit_col is None
    pass # No further action needed, error message already shown.
