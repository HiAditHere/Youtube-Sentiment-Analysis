# Youtube Sentiment Analysis

This application scrapes comments of social media feeds, stores comments into s3 bucket, performs sentiment analysis and returns overall semtiment associated with a social media post. This application is essentially an API that will be deployed to an EC2 instance.

It is currently under progress. Currently I am attempting to build and run a docker inside the ec2 instance. I am getting some space shortage issues but I am working on that. I am using Github Actions to create CICD pipeline.

If you wish to run this application locally then you can do so easily. This is a flask application

### To run application locally

Go to web_scraper.py and modify the file

- Comment out lines 33-53
- Uncomment out lines 13-31

then run the following command

```sh
python app.py
```

make sure you set up the environment variables **AWS_ACCESS_KEY_ID**, **AWS_SECRET_ACCESS_KEY**, **AWS_DEFAULT_REGION** in your local environment.

You can set these variables from command line as 

```sh
set AWS_DEFAULT_REGION=your_default_aws_region
```

Or you could configure connection with your aws client before hand and remove the additional parameters from the `boto3.client` & `boto3.resource` functions. 

If you want to only see how the webscraper works, you can run the `Web_Scraping.ipynb` file.

> **Note**: This webscraper works as of 31 July 2023 but if there is any change in the UI of the website then the webscraper will not work. That being said, if these changes are minor then the only changes you will have to make are to the XPATH in the Web_Scraping.ipynb or web_scraper.py

Once the application is running, go to localhost and paste in the final part of the youtube video link you want to scrape 

> https://www.youtube.com/watch?v=**VS2ylA4HwG0**

Paste the higlighted part as 

```sh
http://localhost:3000/VS2ylA4HwG0
```

In your browser or postman. If the video has a lot of comments then it will take some time to manually scrape the comments. In the end, a json response will be returned.

### Sentiment Analysis 

The sentiment analysis for the comments is done using **flair** module. This module is different than traditional approaches such as bag of words or big dictionaries. This takes into consideration the context the words are being used. This a pre-trained model that returns the if the comments are **positive** or **negative** with the **confidence** with which these comments have been classified as positive or negative.

While returning the json response, I have made the following assumptions

- If confindence with which comment is classified as positive or negative is greated than 0.5 then they are classified as positive/negative or else the comment will be classified as neutral as of now
- Regarding overall sentiment, if the number of positive or neagtive comments is greater then 40% of the total number of comments and difference in the number of positive/negative comments is more than 20% the total number of comment then the overall sentiment is classified as positive/negative or it is classified as neutral.

I still have some testing to do in this part of the application because as of now when I have tested the application, then I did not get any neutral comments at all. It could be a conincidence or flaw in the logic. I am working on this as of now.

### Docker Image

I have pushed an image of the working application to docker hub. The link is as follows
```https://hub.docker.com/r/hiadithere/youtube-sentiment-analysis```

### Conclusion

I hope you guys like this. I was wishing to make this public after I finished the whole application. But as I troubleshoot deployment issues I thought anyone in public could have a look at the code.s