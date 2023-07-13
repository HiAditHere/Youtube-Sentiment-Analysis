from flask import Flask
import web_scraper
import sentiment_analysis
import boto3
import pandas as pd

app = Flask(__name__)

@app.route('/string:title/string:link/')
def scrape_and_analyse(title, link):

    s3 = boto3.resource("s3")
    
    for bucket in s3.buckets,all():
        bucket_name = bucket.name

    s3_client = boto3.client("s3")

    try:
        s3_client.download_file(
            Filename = "new_file.csv",
            Bucket = bucket_name,
            Key = title + ".csv"
        )
    except:
        web_scraper.crawler(link)

    df = pd.read_csv("new_file.csv")

    avg_sentiment = sentiment_analysis(df)

    return avg_sentiment