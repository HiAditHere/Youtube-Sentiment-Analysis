from flask import Flask
from flask import jsonify
import web_scraper
import sentiment_analysis
import boto3
import pandas as pd
import os

app = Flask(__name__)

@app.route('/<string:link>')
def scrape_and_analyse(link):

    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_region = os.environ.get('AWS_DEFAULT_REGION')

    s3 = boto3.resource("s3", aws_secret_access_key = aws_secret_access_key, aws_access_key_id = aws_access_key_id, region_name = aws_region)
    
    for bucket in s3.buckets.all():
        bucket_name = bucket.name

    s3_client = boto3.client("s3", aws_secret_access_key = aws_secret_access_key, aws_access_key_id = aws_access_key_id, region_name = aws_region)

    try:
        s3_client.download_file(
            Filename = "new_file.csv",
            Bucket = bucket_name,
            Key = link + ".csv"
        )
    except:
        web_scraper.crawler(link)

    df = pd.read_csv("new_file.csv")

    avg_sentiment = sentiment_analysis.sentiment_analysis(df)

    return jsonify(avg_sentiment)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("3000"), debug=True)