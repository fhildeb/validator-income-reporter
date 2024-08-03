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