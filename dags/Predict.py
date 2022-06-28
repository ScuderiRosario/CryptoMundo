from resource import prlimit
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.sql import types as st
from pyspark.sql.functions import from_json, col
from pyspark.ml import PipelineModel
from pyspark import SparkFiles
from History_Download import download
import pandas as pd
import json
import os
from pyspark.sql import SparkSession
from pyspark.ml.regression import LinearRegression
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import IndexToString, StringIndexer
from pyspark.sql import SparkSession
from pyspark import SparkFiles
import pyspark.sql.functions as funcs
import pandas as pd
import os

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell'
spark = SparkSession.builder.appName('Linear_Regression').getOrCreate()

def Training(crypto,current):
    data=download(crypto)
    print(data)
    print("Training for: %s"%crypto)
    if len(data)>0:
        data['High']= round(data['High'],2)
        data['Low']= round(data['Low'],2)
        data['Close']= round(data['Close'],2)
        data.to_csv ("/opt/airlfow/data/%s.csv"%crypto, index = False, header=True)
        spark.sparkContext.addFile("/opt/airlfow/data/%s.csv"%crypto)
        dataset_path = SparkFiles.get("%s.csv"%crypto)
        df = spark.read.format('csv').option('header', True).load(dataset_path)
        df=df.drop("Open","Adj Close")

        df = df.select(
            funcs.col("Volume").cast('float'),
            funcs.col("High").cast('float'),
            funcs.col("Low").cast('float'),
            funcs.col("Close").cast('float')
        )

        current = current.select(
            funcs.col("Volume").cast('float'),
            funcs.col("High").cast('float'),
            funcs.col("Low").cast('float')
        )
        
        #Training
        vectorAssembler = VectorAssembler(inputCols=['Volume','High','Low'], outputCol='Attributes')
        output = vectorAssembler.transform(df)
        final_data = output.select("Attributes", "Close")
        train_data, test_data = final_data.randomSplit(weights=[0.85,0.15])
        model = LinearRegression(featuresCol='Attributes', labelCol='Close',maxIter=100, regParam=0.05, elasticNetParam=0.80)
        model = model.fit(train_data)
        
        #Prediction

        current = vectorAssembler.transform(current)
        current = current.select(['Attributes'])
        pred = model.transform(current)
        pred = pred.toPandas()
        pred=pred.iloc[0]['prediction']
        pred=round(pred,2)
        return pred
    return 0



def _Predict(data):
    data=pd.read_json(data)
    final = pd.DataFrame(columns = ['symbol','prediction'])
    #print(data)
    for i in range(len(data)):
        current=data.iloc[i]
        current = pd.DataFrame(current)
        current= current.T
        crypto=current.iloc[0]["symbol"]

        current = current.drop(data.columns.difference(['total_volume','high_24h','low_24h']), 1, inplace=False)
        current.columns = ['Volume','High','Low']
        current.to_csv ("/opt/airlfow/data/tmp%s.csv"%crypto, index = False, header=True)

        spark.sparkContext.addFile("/opt/airlfow/data/tmp%s.csv"%crypto)
        dataset_path = SparkFiles.get("tmp%s.csv"%crypto)
        current = spark.read.format('csv').option('header', True).load(dataset_path)
        prediction=Training(crypto,current)
        print(crypto)
        print(prediction)
        final = final.append({'symbol':crypto, 'prediction':prediction},ignore_index=True)
    print(final)
    final=final.to_json(orient='records')
    return final



