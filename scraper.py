# scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_fanfiction(url, site):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    if site == 'fanfiction.net':
        return extract_story_text_fanfiction(soup)
    elif site == 'ao3':
        return extract_story_text_ao3(soup)
    # Add more elif statements for other sites

def extract_story_text_fanfiction(soup):
    story = soup.find(id='storytextp').get_text(separator='\n')
    return story

def extract_story_text_ao3(soup):
    story = soup.find('div', {'class': 'userstuff'}).get_text(separator='\n')
    return story

# Add similar functions for other sites
