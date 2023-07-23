from flair.models import TextClassifier
from flair.data import Sentence

flair_sentiment = TextClassifier.load('en-sentiment')

def sentiment_analysis(df):
    df.drop(columns = ["Unnamed: 0"], inplace = True)

    def sentiment_analyzer(sentence):
        sent = Sentence(sentence)
        flair_sentiment.predict(sent)
        value = sent.labels[0].to_dict()["value"]
        confidence = sent.labels[0].to_dict()["confidence"]
        
        if value == 'POSITIVE':
            return confidence
        else:
            return (-1*confidence)
        
    df['Sentiment_value'] = df["Comments"].apply(lambda x: sentiment_analyzer(x))

    dic = {
        "pos": {
            "conf":0,
            "count":0
        }, 

        "neg": {
            "conf":0,
            "count":0
        },
    }

    for i in range(len(df['Sentiment_value'])):
        if df['Sentiment_value'][i] >= 0.50:
            dic["pos"]['conf'] += df['Sentiment_value'][i]
            dic["pos"]['count'] += 1
        if df['Sentiment_value'][i] <= -0.50:
            dic["neg"]['conf'] += df['Sentiment_value'][i]
            dic["neg"]['count'] += 1

    overall_sentiment = ''
    avg_positive_sentiment_confidence = 0
    avg_negative_sentiment_confidence = 0
    
    if dic["pos"]["count"] > dic["neg"]["count"]:
        if dic["pos"]["count"] >= 0.4*df.shape[0] and dic["pos"]["count"] - dic["neg"]["count"] >= 0.2*df.shape[0]:
            overall_sentiment = "Positive"
        else:
            overall_sentiment = "Neutral"
    elif dic["pos"]["count"] < dic["neg"]["count"]:
        if dic["neg"]["count"] >= 0.4*df.shape[0] and dic["neg"]["count"] - dic["pos"]["count"] >= 0.2*df.shape[0]:
            overall_sentiment = "Negative"
        else:
            overall_sentiment = "Neutral"
    else:
        overall_sentiment = "Neutral"

    if dic["neg"]["count"] == 0:
        avg_negative_sentiment_confidence = 0
    else:
        avg_negative_sentiment_confidence = dic["neg"]["conf"]/dic["neg"]["count"]

    if dic["pos"]["count"] == 0:
        avg_positive_sentiment_confidence = 0
    else:
        avg_positive_sentiment_confidence = dic["pos"]["conf"]/dic["pos"]["count"]
 

    return {
        "overall_sentiment": overall_sentiment,
        "avg_negative_sentiment_confidence": avg_negative_sentiment_confidence,
        "avg_positve_sentiment_confidence": avg_positive_sentiment_confidence,
        "no_positive_comments": dic["pos"]["count"],
        "no_negative_comments": dic["neg"]["count"],
        "no_neutral_comments": df.shape[0] - (dic["pos"]["count"] + dic["neg"]["count"])
    }