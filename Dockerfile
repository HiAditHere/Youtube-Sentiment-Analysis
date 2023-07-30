FROM python:3.10
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -yq wget gnupg unzip

# Install ChromeBrowser
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list
RUN apt-get update --fix-missing && apt-get install -y google-chrome-stable

# Get latest version of chromedriver
RUN LATEST_CHROMEDRIVER=$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget https://chromedriver.storage.googleapis.com/$LATEST_CHROMEDRIVER/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin && \
    rm chromedriver_linux64.zip

# Set environment variables for chrome binary and chrome driver
ENV CHROME_DRIVER /usr/local/bin/chromedriver
ENV CHROME_BINARY /usr/bin/google-chrome-stable

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 3000
CMD python ./app.py