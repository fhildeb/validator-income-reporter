# System libraries
from datetime import datetime
import sys

# Internal library imports
from utility.api_calls import get_coin_balance_history
from utility.input_checks import check_blockscout_api, check_coinmarketcap_api
from utility.input_checks import is_valid_eth_address, is_valid_year, check_file
from utility.terminal_outputs import printLine, printHead, printFoot, printIntro
from utility.price_calculation import create_daily_data_with_prices, calculate_total_income
from utility.csv_exports import export_to_csv

# Internal config data
from config import BLOCKSCOUT_API_URL, COINMARKETCAP_HEADERS, COINMARKETCAP_API_URL
from config import ETH1_ADDRESS, YEAR, COIN_NAME, FIAT_CURRENCY

def generate_income_report():
    # Generates the income report.

    # Start terminal outputs
    printHead()
    printIntro()

    """"
    Check if config data is valid.

    - Blockscout API must be reachable
    - CoinMarketCap API must be accessible with API KEY
    - Address must be valid ETH1 address
    - Year must be a valid number
    """
    if not (check_blockscout_api(BLOCKSCOUT_API_URL) and
            check_coinmarketcap_api(COINMARKETCAP_API_URL, COINMARKETCAP_HEADERS) and
            is_valid_eth_address(ETH1_ADDRESS) and
            is_valid_year(YEAR)):
        printLine()
        printLine("❌ Input validation failed. Exiting program.", True)
        printFoot()
        return
    printFoot()

    """
    Check for existing CSV and PDF files
    in the current folder and with the same name
    """
    file_name = f"income_report_{YEAR}_{ETH1_ADDRESS}"
    if not check_file(file_name):
        sys.exit("++ Operation aborted. File was not overwritten.\n")


    start_time = datetime.now()

    print(f"Starting income report at {start_time.strftime('%Y-%m-%d %H:%M')}")
    # Fetch income + withdrawal data from Blockscout
    printHead()

    daily_deltas, miner_count, withdrawal_count = get_coin_balance_history()
    validator_earnings = miner_count + withdrawal_count

    """
    Get price history from CoinMarketCap
    for every day with income, e.g. positive deltas
    """
    daily_data = create_daily_data_with_prices(daily_deltas)

    """
    Export income data into a CSV file including
    
    - dates with their deltas
    - daily price and income
    """
    csv_file_name = f"{file_name}.csv"
    export_to_csv(csv_file_name, daily_data, ['Date', 'Received ' + COIN_NAME, 'Former ' + COIN_NAME + ' Price', 'Income in ' + FIAT_CURRENCY])
    printLine()

# Execute report when script is called
if __name__ == '__main__':
    try:
        generate_income_report()
    # Script gets exited
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting gracefully. \n")
        sys.exit(0)