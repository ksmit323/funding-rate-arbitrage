# Crypto Perpetuals Funding Rate Arbitrage

Welcome to the Crypto Perpetuals Funding Rate Arbitrage project! This project was done for the Encode Scaling Web3 Hackathon. It focuses on arbitraging funding rates across different decentralized exchanges (DEXs) for perpetual contracts. The program retrieves funding rates, compares them, and applies arbitrage strategies to maximize profit.
<p align="center">
  <img src="public/crypto_cat.png" alt="Crypto Cat" width="400"/>
</p>

## What's Funding Rate Arbitrage?

In the world of perpetual futures, funding rates are like a seesaw between long and short positions. These rates are periodic payments that help keep the perpetual price in sync with the spot price. But here's where the fun begins: funding rates can differ across various DEXs, creating opportunities for savvy traders to play the arbitrage game.

Picture this: DEX A has a positive funding rate, while DEX B has a negative one. This means that on DEX A, longs are paying shorts, and on DEX B, shorts are paying longs. It's like a funding rate tug-of-war!

To seize this arbitrage opportunity, you'll want to go short on DEX A (where the funding rate is higher) and long on DEX B (where the funding rate is lower). This way, you'll be collecting the higher funding rate on your short position while paying the lower funding rate on your long position. It's a delightful dance of funding rates that can lead to profitable arbitrage if executed correctly.

So, get ready to ride the funding rate waves and join the perpetual futures arbitrage party!

## Features

- Fetches funding rates from multiple DEXs
- Compares funding rates across exchanges
- Executes arbitrage strategies to profit from rate differences
- Supports various DEXs and perpetual markets
- Modular design for easy extension and customization

## Getting Started
To start working with the project, clone this repository and install the required dependencies.

```bash
# Clone the repository
git clone <repository-url>

# Change to the project directory
cd <repository-directory>

# Install dependencies
pip install -r requirements.txt
```

## Usage

The Funding Rate Arbitrage program provides a user-friendly interface to interact with various features and perform funding rate arbitrage across multiple decentralized exchanges (DEXs). Upon running the `main.py` script, you'll be presented with a menu of options:

1. **View USDC balances on each DEX**
  - This option displays your available USDC balances on the supported DEXs, including Orderly, Hyperliquid, and ApexPro.

2. **View open positions**
  - Select this option to view your currently open positions across all the integrated DEXs.

3. **Close positions**
  - Here, you can close your existing positions on a specific DEX by providing the asset symbol (e.g., ETH).

4. **Cancel Open orders**
  - This option allows you to cancel all open orders on a selected DEX.

5. **Start Funding Rate Strategy**
  - This is the main feature of the program, where you can perform funding rate arbitrage. Upon selecting this option, you'll have the following choices:

  - **View rates on all available DEXs**
    - Displays the current funding rates across all supported DEXs.

  <!-- Insert screenshot here -->

  - **View top 3 rate differences from Orderly**
    - Shows the top 3 funding rate differences compared to Orderly.

  <!-- Insert screenshot here -->

  - **View top 3 rate differences from all DEXs**
    - Displays the top 3 funding rate differences across all integrated DEXs.

  <!-- Insert screenshot here -->

  - **Execute Strategy**
    - This option allows you to execute the funding rate arbitrage strategy by following these steps:
      1. Enter the asset symbol you want to trade (e.g., ETH).
      2. Select the DEX you want to short on.
      3. Select the DEX you want to long on.
      4. Enter the order quantity.
      5. Review and confirm your choices.
    - If confirmed, the program will execute the funding rate arbitrage strategy by shorting on the selected DEX and longing on the other DEX, taking advantage of the funding rate difference.

  <!-- Insert screenshot here -->

6. **Exit**
  - Choose this option to exit the program.

Throughout the program's execution, you'll see clear prompts and instructions to guide you through the process. The interface aims to be user-friendly and intuitive, making it easy for you to navigate and perform the desired actions.
