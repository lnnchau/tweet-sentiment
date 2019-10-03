import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(options=chrome_options)


def get_tweet(kw):
    url = f'https://twitter.com/search?q={kw}'
    browser.get(url)
    time.sleep(1)
    body = browser.find_element_by_tag_name("body")
    tweets = browser.find_elements_by_class_name("tweet-text")

    return [t.text for t in tweets]
