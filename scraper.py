import requests
from bs4 import BeautifulSoup
import datetime
import os
import json

URL = "https://www.soa.ac.in/iter-news-and-events"
DATABASE = "./notices.json"
TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_notices():
    if (os.path.exists(DATABASE)):
        with open(DATABASE, 'r') as f:
            return json.load(f) 

def save_notices(notices):
    with open(DATABASE, 'w') as f:
        json.dump(notices, f)

def get_notices():
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    h1_tags = soup.find_all('h1', class_='blog-title')

    notices = []

    for h1 in h1_tags:
        a_tag = h1.find('a')  
        if a_tag:
            h1_content = a_tag.text.strip()  
            link = a_tag['href'] 
            notices.append([h1_content, link])

    return notices


         