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

## Sample Export Files

A sample CSV and PDF report for address
[`0x6e13888469A55A9899A9f270fe34e342853FB725`↗](https://explorer.execution.mainnet.lukso.network/address/0x6e13888469A55A9899A9f270fe34e342853FB725?tab=coin_balance_history)
on the LUKSO Blockchain can be found within [`sample-data`↗](/sample-data/)

The validator started staking on 30th June 2023 after validator
withdrawals got enabled on 6th June 2023.

## Tools

- [Blockscout API](https://github.com/blockscout/blockscout)
- [CoinMarketCap API](https://coinmarketcap.com/api/)
