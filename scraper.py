from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time
import random

def open_browser_and_navigate(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--remote-debugging-port=9222')
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    input("Please solve the CAPTCHA in the browser window that just opened and press Enter here to continue...")
    
    # Save cookies after manually solving CAPTCHA
    save_cookies(driver, 'cookies.pkl')
    print("Cookies saved. You can close the browser now.")
    driver.quit()

def save_cookies(driver, path):
    with open(path, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def scrape_fanfiction_net(url, start_chapter, end_chapter):
    chapters = []
    options = webdriver.ChromeOptions()
    options.add_argument('--remote-debugging-port=9222')
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    driver = webdriver.Chrome(options=options)
    
    # Load cookies if available
    try:
        load_cookies(driver, 'cookies.pkl', ".fanfiction.net")
    except FileNotFoundError:
        pass

    driver.get(url)

    for chapter_number in range(start_chapter, end_chapter + 1):
        chapter_url = url.replace('/1/', f'/{chapter_number}/')
        print(f"Fetching {chapter_url}")
        driver.get(chapter_url)

        time.sleep(random.randint(3, 5))
        
        try:
            story_text_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'storytext'))
            )
            story_text = story_text_element.text
            chapters.append(story_text)
        except Exception as e:
            print(f"Error: Story text element not found for chapter {chapter_number}. Exception: {e}")
            continue

    driver.quit()
    return chapters

def load_cookies(driver, path, domain):
    with open(path, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            if domain in cookie['domain']:
                try:
                    driver.add_cookie(cookie)
                except Exception as e:
                    print(f"Error adding cookie: {cookie}, Exception: {e}")

def scrape_fanfiction(url, site, start_chapter, end_chapter):
    if site == "fanfiction.net":
        return scrape_fanfiction_net(url, start_chapter, end_chapter)
    else:
        raise ValueError("Unsupported site")

if __name__ == "__main__":
    url = "https://www.fanfiction.net/s/13798560/1/Valkyrie-s-Shadow"
    open_browser_and_navigate(url)
