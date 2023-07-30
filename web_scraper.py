from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from time import sleep
import os
import pandas as pd
import boto3

def crawler(link):
    cwd = os.getcwd()

    youtube_link = "https://www.youtube.com/watch?v="+link

    #PATH = cwd + "\ChromeDriver\chromedriver.exe"

    '''PATH = "/usr/local/bin/chromedriver"

    # driver.get does not work all the time. So try except implementation

    driver = None
    new_driver = None

    while driver is None:
        try:
            new_driver = webdriver.Chrome(service=ChromeService(PATH))
            new_driver.get(youtube_link)
            driver = new_driver
        except:
            if new_driver is not None:
                new_driver.quit()
            
    sleep(5)'''

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)
    options.add_argument('--no-sandbox') 

    #PATH = "/usr/local/bin/chromedriver"

    # driver.get does not work all the time. So try except implementation

    driver = None
    new_driver = None

    while driver is None:
        try:
            new_driver = webdriver.Chrome(options = options)
            new_driver.get(youtube_link)
            driver = new_driver
        except:
            if new_driver is not None:
                new_driver.quit()
            
    sleep(5)

    prev_height = 0
    scroll_counter = 100

    # Scroll Down all coments

    while(True):
        height = driver.execute_script('return document.documentElement.scrollHeight')
        driver.execute_script("window.scrollTo(0, " + str(height) + ");")
        
        if prev_height == height:
            scroll_counter-=1
            if scroll_counter == 0:
                break
        else:
            scroll_counter = 100
            
        prev_height = height
        
    # Checking if ad exists and press no thanks

    ad_path = "/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/yt-mealbar-promo-renderer/div/div[2]/yt-button-renderer[1]"

    try:
        ad = driver.find_element("xpath", ad_path)
        ad.click()
    except:
        print("No ad")

    def get_content(comment):
    
        content_text = ''
        
        content = comment.find_element("xpath", ".//yt-formatted-string[@id = 'content-text']")
        #contents = comment.find_elements("xpath", "//*[@id='content-text']/span")
        
        try:
            for sub_content in content.find_element("xpath", "./span"):
                content_text = content_text + sub_content.text + " "
        except:
            content_text += content.text       
        
        return content_text
    
    df = pd.DataFrame(columns = ["Comments"])

    comments_XPATH = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]"
    comments_section = driver.find_element("xpath", comments_XPATH)
    comments = comments_section.find_elements("xpath",'./ytd-comment-thread-renderer')
    print(len(comments))

    # Press all view replies button to comments
    for comment in comments:
        try:
            see_replies = comment.find_element("xpath", './/ytd-button-renderer[@id="more-replies"]')
            see_replies.click()
        except:
            continue
            
    # This is not the same as previous comments
    comments = comments_section.find_elements("xpath",'.//ytd-comment-thread-renderer')

    for comment in comments:
        
        content = get_content(comment)
        df.loc[len(df)] = content
        
        try:
            replies_section = comment.find_element("xpath", ".//ytd-comment-replies-renderer")
            replies = replies_section.find_elements("xpath", ".//ytd-comment-renderer")
            for reply in replies:
                content = get_content(reply)
                df.loc[len(df)] = content
        except:
            continue

    print(df)

    # close the chrome browser convert dataframe to csvMod

    driver.close()
    df.to_csv("new_file.csv")

    s3 = boto3.resource("s3")

    bucket_name = ''

    for bucket in s3.buckets.all():
        bucket_name = bucket.name

    # Uploading the comments in the csv file to our bucket

    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_region = os.environ.get('AWS_DEFAULT_REGION')

    s3_client = boto3.client("s3", aws_secret_access_key = aws_secret_access_key, aws_access_key_id = aws_access_key_id, region_name = aws_region)
    s3_client.upload_file(
        Filename = "new_file.csv",
        Bucket = bucket_name,
        Key = link + ".csv"
    )

    return False