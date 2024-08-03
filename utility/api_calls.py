# FETCHES API DATA

# External libraries
import requests
from datetime import datetime
import time

# Internal library imports
from utility.terminal_outputs import printLine

# Internal config data
from config import BLOCKSCOUT_API_URL, COINMARKETCAP_API_URL
from config import COINMARKETCAP_CRYPTO_ID, COINMARKETCAP_FIAT_ID, COINMARKETCAP_HEADERS
from config import ETH1_ADDRESS, YEAR

def get_block_details(block_number):
    """
    Fetches block details using the Blockscout API.

    :param block_number (int): The block number to fetch details for.
    :return (dict or None): The block details if successful, None otherwise.
    """
    url = f'{BLOCKSCOUT_API_URL}/v2/blocks/{block_number}'
    
    # API failure tolerance
    retries = 3  # tries
    backoff_factor = 2  # tries
    timeout = 10  # seconds

    for attempt in range(retries):
        try:

            # Call the Blockscout API to retrieve block data
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()

            # Wait 2 seconds for new call to respect rate limits
            time.sleep(2)
            return response.json()
        except (requests.ConnectionError, requests.Timeout) as e:
            printLine(f"🟡 Network error. Retrying. {attempt + 1}/{retries}.", True)
            time.sleep(backoff_factor ** attempt)
        except requests.RequestException as e:
            printLine(f"🔴 Error fetching block details for block {block_number}.", True)
            return None
    
    printLine(f"❌ Failed to fetch block details after {retries} attempts.", True)
    return None