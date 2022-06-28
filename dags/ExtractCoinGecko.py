import numpy as np
from pycoingecko import CoinGeckoAPI

def ExtractCoinGecko():
    cg = CoinGeckoAPI()
    data = cg.get_coins_markets(vs_currency='eur')
    return data