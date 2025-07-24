# validator-income-reporter

An Ethereum Validator Income Report Tool, written in Python, that can create reports for any Ethereum blockchain using the Blockscout Explorer and CoinMarketCap price metrics.

![Income Reporter Terminal](/img/income_reporter_terminal.png)

_If this tool helped you out, I would be pleased about a donation:_
`0xE8DFceC1B3637226f05E6828F56815f6417a6116`

## Features

- 🪙 Collects daily income data from an ETH1 address for any given year
- 💸 Calculates FIAT revenue based on daily historical coin prices
- 📊 Exports collected metrics into a CSV file
- 📄 Generates a detailed PDF with 13 pages with metrics and metadata
- 🔧 Blockchain, Coin, and FIAT currency can be freely configured

## Metrics

- 💰 Daily balance increases from withdrawal listings and miner records
- 💯 Validator reward counter for withdrawal listings and miner records
- 📈 Historical median prices for daily revenue insights
- 🧾 Daily, monthly, and yearly income in crypto and FIAT

## Costs

The income reporter uses the [CoinMarketCap API](https://coinmarketcap.com/api/documentation/v1/). To fetch historical price data, you will need to create a [CoinMarketCap Developer Account](https://coinmarketcap.com/api/pricing) and subscribe to either the _Hobbyist_, _Startup_, or _Standard_ pricing model to retrieve historical data.

You will usually get a 100% discount for the first month after signing up, meaning you can generate your reports and switch back to the _free Basic Plan_ after that.

## Report Generation

![Income Reporter Export](/img/income_reporter_export.png)

### General Description

🤝 **Multi-Address Functionality:** The report is generated for one validator withdrawal address. However, you can use this tool to generate multiple reports and merge their raw CSV data using a table calculation program of your choice.

🎯 **Accuracy Measurements**: The script retrieves data based on fetching batched coin balance events and calculating only positive withdrawal deltas that appeared due to being a block miner or listed within block withdrawals. The additional checks allow you to generate accurate staking reports even if you regularly send, receive, or sell coins from the address, as those will not be included.

👟 **Run-Time**: The script's run-time will depend on the number of validators you are running, how far apart the year is from the current date, and if the Blockscout instance supports API Keys. By default, every validator key that receives withdrawals to this address will add around 90 seconds. For every year it has to iterate through, it will add another 15 seconds per validator. If you have 10 validator keys connected to your address and want to generate a report that is one year in the past, the script will need around 18 minutes. If your Blockscout instance supports API Keys, you could further increase the speed to 10 seconds per validator key and 2 seconds per iterated year, meaning you can generate a report for 100 validator keys in just 20 minutes.

### Tax Disclaimers

> The tool and its developers make no guarantees or warranties regarding the data's completeness, reliability, or accuracy. Users acknowledge that the information provided by the tool may contain errors, omissions, or inaccuracies.

> The tool's outputs should not be considered a substitute for professional advice from a qualified tax advisor, accountant, or lawyer. Users are advised to consult with appropriate professionals before making any decisions based on the data provided by the tool. The developers of this tool shall not be held responsible for any legal or tax-related consequences resulting from using the tool or its outputs.

## Development

To run this reporting tool, you must install [Python3](https://www.python.org/). The easiest way for MacOS is to install it using [Homebrew](https://brew.sh/). If you use a different operating system, please [download and install](https://www.python.org/downloads/release/python-3124/) the necessary tools beforehand.

```bash
# Install Python3 using Homebrew
brew install python
```

### Installation

```bash
# Clone the Repository
git clone https://github.com/fhildeb/validator-income-reporter.git

# Create a Virtual Python Environment on Mac and Linux
python3 -m venv report-environment

# Create a Virtual Python Environment on Windows
python -m venv report-environment

# Install Dependencies on Mac and Linux
pip3 install requests pandas fpdf

# Install Dependencies on Windows
pip install requests pandas fpdf
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
3. Blockchain explorer referenced in the `EXPLORER_LINK`

If your Blockscout instance supports [Blockscout API Keys](https://docs.blockscout.com/for-users/my-account/api-keys) modify the:

1. Blockscout API Key at `BLOCKSCOUT_API_KEY`
2. Call Frequency at `BLOCKSCOUT_CALL_WAIT_TIME` to around `0.12`

### Startup

```bash
# Activate the Virtual Python Environment on Mac and Linux
source report-environment/bin/activate

# Activate the Virtual Python Enrironment on Windows
source report-environment\Scripts\Activate.ps1

# Run the Income Reporter Script on Mac and Linux
python3 income_reporter.py

# Run Income Reporter Script on Windows
python income_reporter.py
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
