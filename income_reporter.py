# System libraries
from datetime import datetime
import sys
import argparse
import os

# Internal library imports
from utility.api_calls import get_coin_balance_history
from utility.input_checks import check_blockscout_api, check_coinmarketcap_api
from utility.input_checks import is_valid_eth_address, is_valid_year, check_file
from utility.terminal_outputs import printLine, printHead, printFoot, printIntro
from utility.price_calculation import create_daily_data_with_prices, calculate_total_income
from utility.pdf_generation import csv_to_pdf
from utility.csv_exports import export_to_csv

# Internal config data
from config import BLOCKSCOUT_API_URL, COINMARKETCAP_HEADERS, COINMARKETCAP_API_URL
from config import ETH1_ADDRESS, YEAR, COIN_NAME, FIAT_CURRENCY

def generate_income_report(dry_run_file=None):
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
        sys.exit("++ Aborted. File was not overwritten.\n")


    start_time = datetime.now()

    print(f"Starting income report at {start_time.strftime('%Y-%m-%d %H:%M')}")
    # Fetch income + withdrawal data from Blockscout
    printHead()

    daily_deltas, miner_count, withdrawal_count = get_coin_balance_history()
    validator_earnings = miner_count + withdrawal_count

    """
    Get price history from CoinMarketCap or local CSV file
    for every day with income, e.g. positive deltas
    """
    daily_data = create_daily_data_with_prices(daily_deltas, dry_run_file)

    """
    Export income data into a CSV file including
    
    - dates with their deltas
    - daily price and income
    """
    csv_file_name = f"{file_name}.csv"
    export_to_csv(csv_file_name, daily_data, ['Date', 'Received ' + COIN_NAME, 'Former ' + COIN_NAME + ' Price', 'Income in ' + FIAT_CURRENCY])
    printLine()

    """
    Generate report data metrics:

    - Calculate yearly income in FIAT and crypto currency
    - Measure failure tolerance of days without price
    - Show total withdrawal listings and miner records
    """
    total_income, total_coins, missing_data_count = calculate_total_income(daily_data)
    total_rows = len(daily_data)
    total_coins_formatted = f"{total_coins:.8f}"

    printLine(f"⏩ The address received a total of {validator_earnings} validator payments from:", True)
    printLine(f"⏩ {withdrawal_count} withdrawal listings and {miner_count} miner records.", True)
    printLine()
    printLine(f"⏩ Received {total_coins_formatted} {COIN_NAME} in {YEAR} worth", True)
    printLine(f"⏩ {total_income} {FIAT_CURRENCY} in price-adjusted income.", True)
    printLine()
    printLine(f"🔎 {missing_data_count} of {total_rows} days with income are missing price data", True)
    printLine()

    """
    Generate PDF validator report including:

    - Front page with address, description, and links
    - Table showing monthly and yearly income
    - Detailed pages for every month, showing daily income 
    """
    pdf_file_name = f"{file_name}.pdf"
    csv_to_pdf(csv_file_name, pdf_file_name, miner_count, withdrawal_count)

    end_time = datetime.now()
    
     # Calculate the duration
    duration = end_time - start_time

    # Format the duration as hours, minutes, and seconds
    duration_seconds = duration.total_seconds()
    hours, minutes = divmod(duration_seconds // 60, 60)


    # End terminal outputs
    printLine()
    printLine("🏁 Income report finished successfully", True)
    printFoot()
    print(f"Stopping income report at {end_time.strftime('%Y-%m-%d %H:%M')} after {int(hours):02}:{int(minutes):02}h \n\n")

# Execute report when script is called
if __name__ == '__main__':
    try:
        # Parse CLI arguments
        parser = argparse.ArgumentParser(description="Generate LYX income report")
        parser.add_argument('--dry-run', type=str, help='Use a local CSV file with daily prices instead of API')
        parser.add_argument('--pdf-only', type=str, help='Use an existing CSV file to generate PDF only')
        args = parser.parse_args()

        # Validate optional file paths
        if args.dry_run:
            if not os.path.isfile(args.dry_run):
                print(f"❌ The dry-run file '{args.dry_run}' does not exist or is not a file.")
                sys.exit(1)
            if not args.dry_run.lower().endswith('.csv'):
                print(f"❌ The dry-run file '{args.dry_run}' is not a .csv file.")
                sys.exit(1)
        if args.pdf_only:
            if not os.path.isfile(args.pdf_only):
                print(f"❌ The pdf-only file '{args.pdf_only}' does not exist or is not a file.")
                sys.exit(1)
            if not args.pdf_only.lower().endswith('.csv'):
                print(f"❌ The pdf-only file '{args.pdf_only}' is not a .csv file.")
                sys.exit(1)

        # Only generate PDF from CSV
        if args.pdf_only:
            printHead()
            file_base = os.path.splitext(args.pdf_only)[0]
            pdf_file_name = file_base + ".pdf"
            csv_to_pdf(args.pdf_only, pdf_file_name, miner_count=0, withdrawal_count=0)
            printLine("🏁 PDF generated successfully.", True)
            printFoot()
            sys.exit(0)

        # Run main reporter script
        generate_income_report(args.dry_run)
    # Script gets exited
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting gracefully. \n")
        sys.exit(0)