# System libraries
from datetime import datetime
import sys

# Internal library imports
from utility.input_checks import check_blockscout_api, check_coinmarketcap_api
from utility.input_checks import is_valid_eth_address, is_valid_year, check_file
from utility.terminal_outputs import printLine, printHead, printFoot, printIntro

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

# Execute report when script is called
if __name__ == '__main__':
    try:
        generate_income_report()
    # Script gets exited
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting gracefully. \n")
        sys.exit(0)