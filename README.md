# validator-income-reporter

The Ethereum Validator Income Report Tool, written in Python, can create reports for any Ethereum blockchain with a Blockscout Explorer listed on CoinMarketCap.

![Income Reporter Terminal](/img/income_reporter_terminal.png)

_If this tool helped you out, I would be pleased about a donation:_
`0xE8DFceC1B3637226f05E6828F56815f6417a6116`

## Features

- 🪙 Collects daily income data from an ETH1 address for any given year
- 💸 Calculates FIAT income based on daily historical coin prices
- 📊 Exports collected metrics into a CSV file
- 📄 Generates a detailed PDF with 13 pages for yearly income reports
- 🔧 Blockchain, Coin, and FIAT currency can be freely configured

## Metrics

- 💰 Daily positive coin deltas from withdrawal listings and miner records
- 💯 Validator reward counter for withdrawal listings and block records
- 📈 Historical median prices for daily earned income
- 🧾 Daily, monthly, and yearly income metrics

## Report Generation

![Income Reporter Export](/img/income_reporter_export.png)

## Development

To run this reporting tool, you must install [Python3](https://www.python.org/). The easiest way for MacOS is to install it using [Homebrew](https://brew.sh/). If you use a different operating system, please [download and install](https://www.python.org/downloads/release/python-3124/) the necessary tools beforehand.

```bash
# Install Python3 using Homebrew
brew install python
```

### Installation

```
# Clone the repository
git clone https://github.com/fhildeb/validator-income-reporter.git

# Create a Virtual Python Environment
python3 -m venv income-reporter-tool

# Install necessary dependencies
pip3 install requests install pandas fpdf
```

### Configuration

You can configure this report tool to work with any blockchain or coin. You can copy and modify a global configuration file to your liking. Complete documentation can be found [within the config file](./config-sample.py).

```bash
# Copy the sample configuration file
cp config-sample.py config.py
```

1. Open the `config.py` file
2. Edit the `COINMARKETCAP_API_KEY`
3. Set your `ETH1_ADDRESS` and `YEAR`
4. Choose the `COINMARKETCAP_FIAT_ID` and `COINMARKETCAP_CRYPTO_ID`
5. Define the `COIN_NAME` and `FIAT_CURRENCY`
6. Specify the `REPORT_TITLE`

**By default, the report will be generated for the LUKSO Blockchain**

If you want to create a report for a different [EVM-based Network](https://www.coincarp.com/chainlist/) modify the:

1. API endpoints at `BLOCKSCOUT_API_URL` and `COINMARKETCAP_API_URL`
2. Cryptocurrency at `COINMARKETCAP_CRYPTO_ID` and `COIN_NAME`
3. Blockchain explorer referenced at the `EXPLORER_LINK`

### Startup

```bash
# Activate the Virtual Python Environment
source python-tool/bin/activate

# Run Income Reporter Script
python3 income_reporter.py
```

### Shutdown

After the tool finished sucessfully, you will see the generated CSV and PDF files within the folder. They are both called income report and include the year and your address within the file name. After the files have been generated, the virtual environment can be deactivated.

```bash
# Deactivate the Virtual Python Environment
deactivate
```

## Sample Export Files

A sample CSV and PDF report for address
[`0x6e13888469A55A9899A9f270fe34e342853FB725`↗](https://explorer.execution.mainnet.lukso.network/address/0x6e13888469A55A9899A9f270fe34e342853FB725?tab=coin_balance_history)
on the LUKSO Blockchain can be found within [`sample-data`↗](/sample-data/)

The validator started staking on 30th June 2023 after validator
withdrawals got enabled on 6th June 2023.

## Tools

- [Blockscout API](https://github.com/blockscout/blockscout)
- [CoinMarketCap API](https://coinmarketcap.com/api/)
