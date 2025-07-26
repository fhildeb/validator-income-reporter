import pandas as pd

# Load a generated CSV file and remove income and profit.
# File used for dry runs without CoinMarketCap API.

input_file = "median_lyx_prices_eur.csv"       
output_file = "median_lyx_prices_eur_trimmed.csv"

try:
    df = pd.read_csv(input_file)
    df_modified = df[['Date', 'Former LYX Price']]
    df_modified.to_csv(output_file, index=False)
    df_modified.to_csv(output_file, index=False)
except pd.errors.EmptyDataError:
    print("Error: The CSV file is empty or cannot be parsed.")
except FileNotFoundError:
    print("Error: File not found. Please check the file path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print(f"Modified file saved as: {output_file}")