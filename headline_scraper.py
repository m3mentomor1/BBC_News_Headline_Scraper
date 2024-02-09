from bs4 import BeautifulSoup
import requests
from datetime import datetime

# Create a header
headers = {'User-agent': 'Mozilla/5.0'}

# News Source
URL = 'https://www.bbc.com/news'

# Requests the webpage
request = requests.get(URL, headers=headers)
html = request.content

# Create some soup
soup = BeautifulSoup(html, 'html.parser')


def bbc_news_scraper(keyword=None):
    news_list = []

    # Finds all the headers in BBC Home
    for news in soup.findAll('div', class_='gs-c-promo'):
        headline = news.find('h3', class_='gs-c-promo-heading__title')
        date = news.find('time', class_='qa-status-date')
        
        if headline and date:
            news_title = headline.get_text().strip()
            news_date = date.get_text().strip()
            
            if news_title not in news_list:
                if 'bbc' not in news_title:
                    news_list.append((news_title, news_date))

    # Print source and current date & time
    print("Source:", URL)
    print("Date & Time:", datetime.now().strftime("%b %d, %Y | %I:%M %p"))
    print("\nNews Headlines:")

    # Goes through the list and searches for the keyword
    if keyword:
        for i, (title, date) in enumerate(news_list):
            text = ''
            if keyword.lower() in title.lower():
                text = ' <------------ KEYWORD'

            # Separate the relative time from the rest of the title
            time_index = date.find(' ')
            relative_time = date[time_index + 1:]
            print(f"{i + 1}. '{title}' \nPosted: {date[:time_index]} {relative_time} {text}\n")
    else:
        for i, (title, date) in enumerate(news_list):
            # Separate the relative time from the rest of the title
            time_index = date.find(' ')
            relative_time = date[time_index + 1:]
            print(f"{i + 1}. '{title}' \nPosted: {date[:time_index]} {relative_time}\n")

bbc_news_scraper()
