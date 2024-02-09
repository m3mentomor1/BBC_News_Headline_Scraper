from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
import os

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

    # Store news headlines in a DataFrame
    news_df = pd.DataFrame(news_list, columns=['Headline', 'Posted'])

    # Goes through the list and searches for the keyword
    if keyword:
        for i, (title, date) in enumerate(news_list):
            if keyword.lower() in title.lower():
                news_df.loc[i, 'Keyword'] = keyword

    return news_df

# Display source and current date & time
print("Source:", URL)
print("Date & Time:", datetime.now().strftime("%b %d, %Y | %I:%M %p\n"))

# Call the function without specifying a keyword
news_dataframe = bbc_news_scraper()

# Display headlines in console output
print(news_dataframe)

# Ask user for file path and save the DataFrame to a CSV file
file_path = r'C:\Visual Studio Code (Workspace)\Web\bbc_news_headlines.csv'

if os.path.exists(file_path):
    os.remove(file_path)  # Delete existing file if it exists

news_dataframe.to_csv(file_path, index=False)

if os.path.exists(file_path):
    print(f"\nThe scraped data is saved to '{file_path}'.")
else:
    print("\nScraped data was not saved.")
