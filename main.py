import os

from datetime import datetime
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
####################################################################################################################################
####################################################################################################################################

class FOMC():
    def __init__(self):
        pass
    
    def get_statements(self):
        dates = [datetime.strptime(file[:10],'%d-%m-%Y') for file in os.listdir('statements')]
        statements = [open('statements/{}'.format(file), mode='r').read().replace('\n', '') for file in os.listdir('statements')]
        self.df = pd.DataFrame({'statement':statements, 'positive':np.nan, 'negative':np.nan, 'neutral':np.nan, 'compound':np.nan}, index=pd.to_datetime(dates))
        self.df.sort_index(inplace=True)

    def get_sentiment(self):
        for date in self.df.index:
            sentiment_score = sia.polarity_scores(self.df.loc[date]['statement'])
            self.df.at[date, 'positive'] = sentiment_score['pos']
            self.df.at[date, 'negative'] = sentiment_score['neg']
            self.df.at[date, 'neutral'] = sentiment_score['neu']
            self.df.at[date, 'compound'] = sentiment_score['compound']

    def plot(self):
        fig, ax = plt.subplots(figsize=(18,10))
        self.df['compound'].plot(kind='bar')
        ax.axhline(0, color='k')
        plt.show()

    def run(self):
        self.get_statements()
        self.get_sentiment()
        self.plot()

if __name__ == '__main__':
    FOMC().run()