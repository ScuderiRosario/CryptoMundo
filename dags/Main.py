from datetime import datetime
from tracemalloc import Snapshot
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import date

from ExtractCoinGecko import ExtractCoinGecko
from ExtractSymbol import ex_symb
from Twitter import twitter_Ex
from Aggr import Aggregator
from Kafka import producer
from Predict import _Predict


def ExtractSymbol(ti):
    data=ti.xcom_pull(task_ids='Extract_CoinGecko')
    return ex_symb(data)

def TwitterExtractor(ti):
    data=ti.xcom_pull(task_ids='Extract_Symbol')
    return twitter_Ex(data)

def PRED(ti):
    data=ti.xcom_pull(task_ids='Aggregate')
    return _Predict(data)


def Aggr(ti):
    data=ti.xcom_pull(task_ids='Extract_CoinGecko')
    sentiment=ti.xcom_pull(task_ids='Extract_Twitter')
    return Aggregator(data,sentiment)

def Kafka_prod(ti):
    data=ti.xcom_pull(task_ids='Aggregate')
    prediction=ti.xcom_pull(task_ids='Predict')
    producer(data,prediction)


default_args={"owner":"airflow",}
with DAG(
    dag_id="myCrypto",
    start_date=datetime(2022,5,23),
    schedule_interval='*/2 * * * *', #..every 2 minutes
    catchup=False,
    default_args=default_args)as dag:


    Extract_CoinGecko = PythonOperator(
        task_id= 'Extract_CoinGecko',
        python_callable= ExtractCoinGecko
    )

    Extract_Symbol = PythonOperator(
        task_id= 'Extract_Symbol',
        python_callable= ExtractSymbol
    )

    Extract_Twitter = PythonOperator(
        task_id= 'Extract_Twitter',
        python_callable= TwitterExtractor
    )

    Aggregate = PythonOperator(
        task_id= 'Aggregate',
        python_callable= Aggr
    )

 
    Kafka_Producer = PythonOperator(
        task_id= 'Kafka_Producer',
        python_callable= Kafka_prod
    )

    Predict = PythonOperator(
        task_id= 'Predict',
        python_callable= PRED
    )

    
Extract_CoinGecko >> [Aggregate,Extract_Symbol]
Extract_Symbol >> Extract_Twitter
Extract_Twitter>> Aggregate
Aggregate >> Predict >> Kafka_Producer