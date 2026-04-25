from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_score(comment) :
    sia = SentimentIntensityAnalyzer() 
    sentiment_dict = sia.polarity_scores(comment)
        
    compound = sentiment_dict['compound']
    if compound > 0.5:
        sentiment_dict['Sentiment'] = "Positive"
        
   
    elif compound < -0.5:
        sentiment_dict['Sentiment'] = "Negative"
    
    elif compound <= 0.5 and compound >= -0.5 :
        sentiment_dict['Sentiment'] = "Neutral"
        
    return sentiment_dict