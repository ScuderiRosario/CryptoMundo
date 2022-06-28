import imp
from json import dumps
from time import sleep
import pandas as pd
from kafka import KafkaProducer

def producer(data,prediction):
    producer = KafkaProducer(bootstrap_servers='broker:29092')
    data=pd.read_json(data, orient ='column')
    prediction=pd.read_json(prediction, orient ='column')
    data=pd.merge(data, prediction, on = "symbol", how = "inner")

    data=data.drop(data.columns.difference(['symbol','current_price','polarity','market_cap','total_volume',"total_supply","prediction"]), 1, inplace=False)
    data=data.to_json(orient='records')
    print(data)
    producer.send('crypto2', data.encode('utf-8'))

