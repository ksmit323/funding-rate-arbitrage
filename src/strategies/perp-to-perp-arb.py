from hyperliq.funding_rate import HyperliquidFundingRates
from orderly.funding_rate import OrderlyFundingRates


class PerpToPerpArbitrage(object):
    def __init__(self):
        self.dex_rates = {}

    def add_dex_rates(self, dex_name: str, funding_rates: dict):
        """Adds a new set of rates for a given DEX"""
        self.dex_rates[dex_name] = funding_rates

    def compile_rates(self):
        """
        Compiles funding rates from all DEXs into a structured dictionary format.

        Returns:
        dict: A dictionary where keys are symbols and values are dictionaries of DEX names and rates.
        """
        all_rates = {}

        for dex_name, funding_rates in self.dex_rates.items():
            for symbol, rate in funding_rates.items():
                if symbol not in all_rates:
                    all_rates[symbol] = {}
                all_rates[symbol][dex_name] = rate
        
        return all_rates

# Usage
orderly_rates = OrderlyFundingRates().get_orderly_funding_rates
hyperliquid_rates = HyperliquidFundingRates().get_hyperliquid_funding_rates()

perpArb = PerpToPerpArbitrage()

perpArb.add_dex_rates("Orderly", orderly_rates)
perpArb.add_dex_rates("Hyperlink", hyperliquid_rates)

rates_table = perpArb.compile_rates()

print(rates_table)