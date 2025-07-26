# CALCULATES DAILY INCOME DATA

# Internal library imports
from utility.api_calls import get_coin_price
from utility.terminal_outputs import printLine

def create_daily_data_with_prices(daily_deltas, price_lookup_file=None):

    """
    Creates daily income data including prices.
    
    - Iterates over the daily deltas
    - Fetches the coin price for each date
    - Calculates and rounds the daily income
    
    :param daily_deltas (dict): A dictionary of dates and their coin deltas.
    :return (list): A list containing date, income, coin deltas, and prices.
    """

    price_map = {}
    if price_lookup_file:
        import pandas as pd
        df_prices = pd.read_csv(price_lookup_file)

        # Normalize both column names and content
        df_prices.columns = df_prices.columns.str.strip()  # Remove trailing spaces from header names
        df_prices['Date'] = df_prices['Date'].astype(str).str.strip()  # Ensure all dates are strings with no whitespace

        price_map = dict(zip(df_prices['Date'], df_prices['Former LYX Price']))

    daily_data = []
    printLine()

    # Normalize dates for string references
    daily_deltas = {
    date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date).strip(): value
    for date, value in daily_deltas.items()
    }

    # Iterate through all dates with income
    for date, delta_coin in sorted(daily_deltas.items()):
        
        # Retrieve the prices during this date
        printLine(f"🧾 Calculating Income for {date}", True)
        
        # Get local price data
        if price_lookup_file:
            coin_price = price_map.get(date)
        # API price data
        else:
            coin_price = get_coin_price(date)
        
        # If price could be fetched
        if not coin_price is None:
            income = delta_coin * coin_price
            income = round(income, 2)
            coin_price = round(coin_price, 10)
        else:
            income = None
            coin_price = None

        delta_coin = round(delta_coin, 10)

        # Write new daily entry into the report list
        daily_data.append([date, delta_coin, coin_price, income])
        
    # Return report list
    return daily_data

def calculate_total_income(daily_data):
    """
    Calculates the total income from the report list
    and counts the days with missing income data.
    
    :param daily_data (list): A list containing daily income data.
    :return (float, int): The total rounded FIAT income and days with missing income data.
    """
    total_income = 0.0
    total_coins = 0.0
    missing_data_count = 0

    # Iterate through every day of the report
    for row in daily_data:
        coins = row[1]
        income = row[3]

        # Income calculation
        if income is not None:
            total_income += income
        else:
            missing_data_count += 1

        total_coins += coins
    
    # Round the total income to 2 decimal places
    total_income = round(total_income, 2)

    # Return income and days with missing data
    return total_income, total_coins, missing_data_count