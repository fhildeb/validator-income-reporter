# VALIDATES CONFIG DATA

# System libraries
import os
import re
from datetime import datetime
import requests

# Internal library imports
from utility.terminal_outputs import printLine

def check_blockscout_api(api_url):
    """
    Check if the Blockscout API is accessible.

    :param api_url (str): The URL of the Blockscout API.
    :return (bool): True if the API is reachable, False otherwise.
    """
    try:
        # Sample request parameters
        params = {
            'module': 'stats',
            'action': 'ethprice'
        }

        # Call API
        response = requests.get(api_url, params=params)

        # If there was a valid return
        if response.status_code == 200:
            printLine("🟢 Blockscout API is reachable.", True)
            return True
        else:
            printLine("🟡 Blockscout API is not reachable.", True)
            return False
        
    # If the API is offline
    except requests.RequestException as e:
        printLine(f"🔴 Error connecting to Blockscout API.", True)
        return False
    
def check_coinmarketcap_api(api_url, headers):
    """
    Check if the CoinMarketCap API is accessible.

    :param api_url (str): The URL of the CoinMarketCap API.
    :param headers (dict): Headers required for the CoinMarketCap API request.
    :return (bool): True if the API is reachable, False otherwise.
    """

    # Sample request parameters
    sample_params = {
    'start': '1',
    'limit': '5000',
    'convert': 'EUR',  
    }

    try:
        # Call API
        sample_call = api_url + '/v1/cryptocurrency/listings/latest'
        response = requests.get(sample_call, headers=headers, params=sample_params)

        # If there was a valid return
        if response.status_code == 200:
            printLine("🟢 CoinMarketCap API is reachable.", True)
            return True
        else:
            printLine("🟡 CoinMarketCap API is not reachable.", True)
            return False
    
    # If the API is offline
    except requests.RequestException as e:
        printLine(f"🔴 Error connecting to CoinMarketCap API.", True)
        return False

def is_valid_eth_address(address):
    """
    Check if the provided Ethereum address is valid.

    :param address (str): The Ethereum address to validate.
    :return (bool): True if the address is valid, False otherwise.
    """

    # Verify REGEX
    if re.match(r'^0x[a-fA-F0-9]{40}$', address):
        printLine("🟢 Valid Ethereum address.", True)
        return True
    else:
        printLine("🔴 Invalid Ethereum address.", True)
        return False