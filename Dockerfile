FROM python:3.8-slim-buster

#install gnupg2, wget and curl
RUN apt-get update && apt-get install -y gnupg2 && apt-get install -y curl && apt-get install -y wget

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN apt-get install -yqq unzip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# install psycopg2 dependencies
RUN apt-get -y install libpq-dev gcc

COPY . . 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "ukc_scraper.py"]