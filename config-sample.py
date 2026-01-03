""" 
BLOCKSCOUT_API_URL is used to retrieve historical balance 
data from the Blockscout explorer of a given blockchain.

- LUKSO Mainnet Explorer is used as default
- always use without version tag or slash at the end
- always use HTTPS for data transport protocol

- API_KEY not always available, but can increase speed
- CALL_WAIT_TIME is set to 50 calls per minute
- Increase CALL_WAIT_TIME if you get issues retrieving data

"""
BLOCKSCOUT_API_URL = 'https://explorer.execution.mainnet.lukso.network/api'
BLOCKSCOUT_API_KEY = None
BLOCKSCOUT_CALL_WAIT_TIME = 1.2 # seconds (max 75 calls per minute ~0.8)

"""
COINMARKETCAP_API_URL, COINMARKETCAP_API_KEY, COINMARKETCAP_HEADERS,
COINMARKETCAP_FIAT_ID, and COINMARKETCAP_CRYPTO_ID are used to retrieve 
historical price information about a specific blockchain coin, matching
the data cetrieved from Blockscout to calculate FIAT income.

- always use API_URL without version tag or slash at the end
- always use API_URL with HTTPS for data transport protocol

- ensure that your API_KEY is valid
- ensure that your API_KEY has enough credits left
- credits used for a full yearly report: 9125

- keep HEADER as is
- ensure FIAT_ID is valid
- ensure that CRYPTO_ID is valid and matches the blockchain
- CALL_WAIT_TIME is set to 30 calls per minute

- API KEY PRICING: https://coinmarketcap.com/api/pricing
- FIAT ID CODES: - https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions

LUKSO Disclaimer: for LYX income reports for 2023, its recommended to use the 
CRYPTO_ID of the LYXe token, instead of the LYX coin. This is because withdrawals 
got enabled in June 2023, while LYX was listed on the first exchange end of July. 
Due to a big liquidity pool being actively bridged from LYXe, both crypto assets 
only had minimal price fluctuations. For 2024 and beyond, please always use LYX.
- https://coinmarketcap.com/currencies/lukso/
- https://coinmarketcap.com/currencies/lukso-network/
"""
COINMARKETCAP_API_URL = 'https://pro-api.coinmarketcap.com'
COINMARKETCAP_API_KEY = '1a1a1a1a-1234-1234-1a1a-1a1a1a1a1a1a'
COINMARKETCAP_FIAT_ID = '2790' # EUR = '2790', USD = '2781'
COINMARKETCAP_CRYPTO_ID = '27622' # LYXe = '5625', LYX = '27622'
COINMARKETCAP_CALL_WAIT_TIME = 3 # seconds (max 30 calls per minute ~2)
COINMARKETCAP_HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
}

"""
FIAT_CURRENCY, COIN_NAME, REPORT_TITLE, and EXPLORER_LINK are used 
for naming columns and values within the CSV and PDF reports, 
as well as creating a cover sheet
"""
FIAT_CURRENCY = 'EUR'
COIN_NAME = 'LYX'
REPORT_TITLE = 'LUKSO Blockchain Node Validator'
EXPLORER_LINK = 'https://explorer.execution.mainnet.lukso.network'

"""
ETH1_ADDRESS and YEAR are used to fetch blockchain data and
calculate report timeframes.

- ensure that the ETH1_ADDRESS is your validator withdrawal address
- ensure that the blockchain was active during the given year
- ensure that the year is a valid number
"""
ETH1_ADDRESS = '0xcafecafecafecafecafecafecafecafecafecafe'
YEAR = 2023