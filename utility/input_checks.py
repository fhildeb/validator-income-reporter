# VALIDATES CONFIG DATA

# System libraries
import os
import re
from datetime import datetime
import requests

# Internal library imports
from utility.terminal_outputs import printLine
from config import BLOCKSCOUT_API_KEY

def check_blockscout_api(api_url):
    """
    Check if the Blockscout API is accessible.

    :param api_url (str): The URL of the Blockscout API.
    :return (bool): True if the API is reachable, False otherwise.
    """
    url = f'{api_url}'
    
    if BLOCKSCOUT_API_KEY is not None:
        url += f'&apikey={BLOCKSCOUT_API_KEY}'

    try:
        # Sample request parameters
        params = {
            'module': 'stats',
            'action': 'ethprice'
        }

        response = requests.get(url, params=params)

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
    
def is_valid_year(year):
    """
    Check if the provided year is a valid integer.

    :param year (int): The year to validate.
    :return (bool): True if the year is valid, False otherwise.
    """
    current_year = datetime.now().year

    # If year is between current system date and 2014
    if isinstance(year, int) and 2014 <= year <= current_year:
        printLine("🟢 Valid year.", True)
        return True
    else:
        printLine(f"🔴 Invalid year. Must be between 2014 and {current_year}.", True)
        return False
    
def check_file(filename):
    """
    Check if there already is a CSV and/or PDF file with an equal name. 
    If yes, ask for approval to overwrite.

    :param filename (str): The base name of the file to check for existence.
    :return (bool): True if the file can be overwritten or does not exist, False otherwise.

    """

    # If filename exists for CSV or PDF, require user input
    if os.path.exists(f"{filename}.csv") or os.path.exists(f"{filename}.pdf"):
        print(f"\n++ Found CSV or PDF files with the following name:")
        print(f"++ {filename}")
        user_input = input("++ Do you want to overwrite them? (Y/N): ").strip().upper()
        # User denied overwriting the files
        if user_input != 'Y':
            return False
        print("++ Overwriting the files... \n")
    return True