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

def get_coin_balance_history():
    """
    Uses the Blockscout REST API to fetch the coin balance history
    based on the latest coin change events.

    - Iterates through all balance changes in batch of 50
    - Fetches data until it hit the end of timeframe or is out of balance events
    - When timeframe is valid, stores dates and calculates daily positive incomes

    :return (dict): A dictionary of dates and their coin deltas.
    :return (int): Number of times the validator was listed as miner
    :return (int): Number of times the validator was listed as withdrawal address
    """

    # REST API GET CALL
    url = f'{BLOCKSCOUT_API_URL}/v2/addresses/{ETH1_ADDRESS}/coin-balance-history'

    # Income delta objects
    daily_deltas = {}
    miner_count = 0
    withdrawal_count = 0
    eth_decimal_factor = 10**18

    # Iteration parameters for API calls
    next_page_params = None
    timeframe_min_date = datetime(YEAR, 1, 1).date()
    timeframe_max_date = datetime(YEAR, 12, 31).date()
    start_collecting = False

    # API failure tolerance
    retries = 3 # tries
    backoff_factor = 2 # tries
    timeout = 10  # seconds

    while True:
        params = {}

        # Check if last API call had attached iteration parameters
        if next_page_params:
            params = next_page_params

        # Show status and depth of history events in terminal report
        block_number = params.get('block_number', 'Latest')
        items_count = params.get('items_count', '0')
        printLine(f"⚪️ Fetching data, Block: {block_number}, Balance History Depth: {items_count}")

        for attempt in range(retries):
            try:
                # Call Blockscout API with parameters
                response = requests.get(url, params=params, timeout=timeout)

                # Raise exception for HTTP errors
                response.raise_for_status()  
                data = response.json()

                # Break the retry loop if the request was successful
                break  
            except (requests.ConnectionError, requests.Timeout) as e:
                printLine(f"🟡 Network error. Retrying. {attempt + 1}/{retries}.", True)
                time.sleep(backoff_factor ** attempt)
            except requests.RequestException as e:
                printLine(f"🔴 Error fetching Blockscout data.", True)

                # Return what has been collected so far
                return daily_deltas, miner_count, withdrawal_count
        else:
            printLine(f"❌ Failed to fetch Blockscount data after {retries} attempts.", True)
            printLine("❌ Report incomplete. Please retry.", True)

            # Return what has been collected so far
            return daily_deltas, miner_count, withdrawal_count

        # Check if timeframe has been entered or not
        searchStatus = False
        collectStatus = False

        # For every entry within the batch of 50 historical balance events
        for item in data['items']:

            # Extract data from each item
            transaction_date = datetime.strptime(item['block_timestamp'], '%Y-%m-%dT%H:%M:%SZ').date()
            delta = int(item['delta'])
            item_block_number = item['block_number']

            # Monitor and toggle data fetching status
            if not start_collecting:

                # Event is outside the defined report timeframe, continue searching
                if not searchStatus:
                    printLine(f"🟡 {transaction_date}, searching events in timeframe", True)
                    searchStatus = True
                
                # Event is inside the defined report timeframe, start collecting
                if transaction_date <= timeframe_max_date:
                    printLine(f"🟢 {transaction_date}, found events within timeframe", True)
                    start_collecting = True

            # If data is within the report timeframe
            if start_collecting:
                
                # Check if the events are outside the end date
                if transaction_date < timeframe_min_date:
                    printLine(f"🏁 {transaction_date}, stopping due to end of timeframe", True)
                    return daily_deltas, miner_count, withdrawal_count

                # Only consider positive deltas, if income was withdrawn from validator
                if delta > 0:

                    is_miner = False
                    is_withdrawal = False

                    # Fetch block withdrawals to verify if the address is listed in the withdrawals
                    block_withdrawals = get_block_withdrawals(item_block_number)
                    is_withdrawal = any(
                        withdrawal['receiver']['hash'] == ETH1_ADDRESS
                        for withdrawal in block_withdrawals.get('items', [])
                    )

                    # Log if the address is found in withdrawals
                    if is_withdrawal:
                        withdrawal_count += 1
                        printLine(f"💵 Found validator withdrawal reward in block {item_block_number}. Total: {withdrawal_count}", True)
                    else:
                        # Fetch block details to verify if the address is the miner
                        block_details = get_block_details(item_block_number)
                        miner_count += 1
                        is_miner = True
                        if block_details and block_details.get('miner', {}).get('hash') == ETH1_ADDRESS:
                            printLine(f"🧱 Found validator miner reward in block {item_block_number}. Total: {miner_count}", True)

                    # Only count deltas if the address is the miner or listed in the withdrawals
                    if is_miner or is_withdrawal:
                        # If it is the first event, start collecting deltas from now on
                        if not collectStatus:
                            collectStatus = True
                    
                        """
                        Add date and delta amount to the income metrics list
                        If date already exists, add current delta to the existing one
                        """
                        delta_coin = delta / eth_decimal_factor
                        daily_deltas[transaction_date] = daily_deltas.get(transaction_date, 0) + delta_coin

        next_page_params = data.get('next_page_params')

        # Wait 2 seconds to respect rate limits
        time.sleep(2)

        # If there are no more coin balance history events, break the loop
        if not next_page_params or int(next_page_params.get('block_number', 1)) == 0:
            printLine("🏁 No further balance history available, ending data fetch.", True)
            break

    # Return daily income metrics list
    return daily_deltas, miner_count, withdrawal_count

def get_coin_price(date):
    """
    Uses the CoinMarketCap REST API to fetch the OHLCV coin price of a historical day.
    Calculates the median value from open and closing position

    :param date (datetime): The date for which to fetch the coin price.
    :return (float or None): The median coin price for the given date, None if an error occurs.
    """
    
    # REST API GET CALL
    url = COINMARKETCAP_API_URL + '/v2/cryptocurrency/ohlcv/historical'
    headers = COINMARKETCAP_HEADERS
    params = {
        'id': COINMARKETCAP_CRYPTO_ID,
        'convert_id': COINMARKETCAP_FIAT_ID,
        'time_period': 'daily',
        'time_start': date.strftime('%Y-%m-%d'),
        'time_end': date.strftime('%Y-%m-%d')
    }

    # API failure tolerance
    retries = 3 # tries
    backoff_factor = 2 # tries
    timeout = 10  # seconds

    for attempt in range(retries):
        try:
            # Call CoinMarketCap API with parameters
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
            response.raise_for_status()
            data = response.json()

            # Break the retry loop if the request was successful
            break  
        except (requests.ConnectionError, requests.Timeout) as e:
            printLine(f"🟡 Network error. Retrying. {attempt + 1}/{retries}.", True)
            time.sleep(backoff_factor ** attempt)
        except requests.RequestException as e:
            printLine(f"🔴 Error fetching CoinMarketCap data.", True)
            return None
    else:
        printLine(f"❌ Failed to fetch CoinMarketCap data after {retries} attempts.", True)
        return None

    try:
        # Extract open and closing price
        ohlcv = data['data']['quotes'][0]['quote'][COINMARKETCAP_FIAT_ID]
        open_price = ohlcv['open']
        close_price = ohlcv['close']
        
        # Calculate daily median price
        median_price = (open_price + close_price) / 2

        # Wait 2 seconds for new call to respect rate limits
        time.sleep(2)

        return median_price
    except (KeyError, IndexError) as e:
        printLine(f"🟠 No available CoinMarketCap price data for {date}.", True)
        return None

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

def get_block_withdrawals(block_number):
    """
    Fetches block withdrawal details using the Blockscout API.

    :param block_number (int): The block number to fetch withdrawal details for.
    :return (dict or None): The block withdrawal details if successful, None otherwise.
    """
    url = f'{BLOCKSCOUT_API_URL}/v2/blocks/{block_number}/withdrawals'
    
    # API failure tolerance
    retries = 3  # tries
    backoff_factor = 2  # tries
    timeout = 10  # seconds

    for attempt in range(retries):
        try:

            # Call the Blockscout API to retrieve withdrawal data
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()

            # Wait 2 seconds for new call to respect rate limits
            time.sleep(2)

            return response.json()
        except (requests.ConnectionError, requests.Timeout) as e:
            printLine(f"🟡 Network error. Retrying. {attempt + 1}/{retries}.", True)
            time.sleep(backoff_factor ** attempt)
        except requests.RequestException as e:
            printLine(f"🔴 Error fetching withdrawals for block {block_number}.", True)
            return None
    
    printLine(f"❌ Failed to fetch withdrawals after {retries} attempts.", True)
    return None