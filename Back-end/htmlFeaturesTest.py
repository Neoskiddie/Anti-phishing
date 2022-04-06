from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
#driver = webdriver.Chrome()
opts = Options()
# uncomment this if you don't want to see the Chrome

opts.add_argument(" --headless")
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), chrome_options=opts)


def get_website(url):
    """
    Gets content of the website and return it as BeautifulSoup object
    """
    driver.get(url)
    return BeautifulSoup(driver.page_source, 'html.parser')


print(get_website('https://scrolller.com/').encode('utf-8'))
driver.quit()
