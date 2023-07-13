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

    avg_sentiment = df['Sentiment_value'].mean()

    return avg_sentiment