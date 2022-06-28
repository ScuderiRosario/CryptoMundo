from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import snscrape.modules.twitter as sntwitter
import pandas as pd
import itertools
import numpy as np

def twitter_Ex(data):
    export= pd.DataFrame(columns = ["symbol", "polarity"])
    for crypto in data:
        df=pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper('"(#%s) lang:en within_time:10m"'%crypto).get_items(),50))
        #df=df.drop(['url','date','id', 'username', 'outlinks', 'outlinksss','tcooutlinks', 'tcooutlinksss'], axis = 1)
        polar=0
        for sentence in df['content']:
            sid_obj = SentimentIntensityAnalyzer()
            sentiment_dict = sid_obj.polarity_scores(sentence)
            polar=polar+sentiment_dict['pos']
        polar=polar*100
        if polar >= 500:
            polarity="Positive"
        if polar < 500:
            polarity="Negative"
        s_row = pd.Series([crypto, polarity], index=export.columns)
        export = export.append(s_row,ignore_index=True)
    export=export.to_json(orient='records')
    print(export)
    return export