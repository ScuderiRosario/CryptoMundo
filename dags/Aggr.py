import numpy as np
import pandas as pd


def Aggregator(data,sentiment):
    data = pd.DataFrame(data, columns=['id','symbol','current_price','market_cap','total_volume','high_24h','low_24h','total_supply','ath','ath_date','last_updated'])
    sentiment=pd.read_json(sentiment, orient ='column')
    final=pd.merge(data,sentiment, on='symbol', how="inner")
    final=final.to_json(orient='records')
    print(final)
    return final