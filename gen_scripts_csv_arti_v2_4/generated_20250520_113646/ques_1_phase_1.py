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

# The dataset is already loaded into a pandas DataFrame called df.

# Define the columns for Net Profit, Owner's Equity, and Minority Interests by year
years = ['2019', '2020', '2021', '2022', '2023']

net_profit_cols = [f'18. Net profit/(loss) after tax\nYear: {year}\nUnit: Billions VND\n' for year in years]
owner_equity_cols = [f'II. OWNER\'S EQUITY\nYear: {year}\nUnit: Billions VND\n' for year in years]
minority_interests_cols = [f'1.13. Minority interests\nYear: {year}\nUnit: Billions VND\n' for year in years]

# Calculate Parent Equity for each year and create new columns
parent_equity_cols = []
for i, year in enumerate(years):
    parent_equity_col_name = f'Parent Equity\nYear: {year}\nUnit: Billions VND\n'
    # Ensure column names are correctly referenced, including potential newline/spaces
    owner_col = owner_equity_cols[i]
    minority_col = minority_interests_cols[i]

    # Check if columns exist before calculation
    if owner_col in df.columns and minority_col in df.columns:
        df[parent_equity_col_name] = df[owner_col] - df[minority_col]
        parent_equity_cols.append(parent_equity_col_name)
    else:
        # Handle cases where a column might be missing (though unlikely based on prompt)
        print(f"Warning: Required column for {year} not found.")
        # Create the column with NaN or 0 if calculation not possible
        df[parent_equity_col_name] = pd.NA # Or 0, depending on desired NA representation
        parent_equity_cols.append(parent_equity_col_name)


# Calculate the total net profit for each company over the years 2019-2023
# Sum only the existing net profit columns
existing_net_profit_cols = [col for col in net_profit_cols if col in df.columns]
if existing_net_profit_cols:
    df['Total Net Profit 2019-2023'] = df[existing_net_profit_cols].sum(axis=1)
else:
     df['Total Net Profit 2019-2023'] = 0 # Handle case with no net profit data


# Group by sector and select the top 3 companies based on total net profit
# Ensure the grouping column exists
if 'Sector L2\n' in df.columns:
    # Use nlargest within groupby.apply to get top N rows per group
    # Pass group_keys=False to avoid retaining the group keys as index levels
    top_companies_per_sector = df.groupby('Sector L2\n', group_keys=False).apply(
        lambda x: x.nlargest(3, 'Total Net Profit 2019-2023')
    )

    # Define the columns to display for the top companies
    # Ensure all display columns actually exist in the DataFrame
    display_cols = [col for col in ['Ticker\n', 'Company Name\n'] + net_profit_cols + parent_equity_cols if col in top_companies_per_sector.columns]


    # Print the results, grouped by sector
    if not top_companies_per_sector.empty:
        # Iterate through sectors present in the top companies result
        for sector, sector_df in top_companies_per_sector.groupby('Sector L2\n'):
            print(f"Sector: {sector.strip()}") # Use strip for printing
            print("-" * (len(sector.strip()) + 8))
            # Iterate through companies in this sector's top list
            # Use .iterrows() on the DataFrame slice for the sector
            for index, row in sector_df[display_cols].iterrows():
                print(f"  Company: {row['Company Name\n'].strip()} ({row['Ticker\n'].strip()})") # Use strip for printing
                print("    Net Profit (Billions VND):")
                # Print yearly Net Profit
                for year_col in net_profit_cols:
                    if year_col in row: # Check if the column exists for this row/data
                         year = year_col.split('\n')[1].split(': ')[1] # Extract year from column name
                         print(f"      {year}: {row[year_col]:.2f}")
                print("    Parent Equity (Billions VND):")
                # Print yearly Parent Equity
                for year_col in parent_equity_cols:
                     if year_col in row: # Check if the column exists
                         year = year_col.split('\n')[1].split(': ')[1] # Extract year from column name
                         print(f"      {year}: {row[year_col]:.2f}")
                print("-" * 20)
            print("\n")
    else:
        print("No top companies found.")
else:
    print("Sector column not found in the DataFrame.")
