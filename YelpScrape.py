import pandas as pd
from lxml import html
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
 
from selenium import webdriver
from selenium.webdriver import Chrome

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from splinter import Browser
import time

executable_path = {"executable_path": r"C:\Users\Deepak\Desktop\chromedriver.exe"}

#set some chrome options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")

# define browser
b = Browser("chrome", **executable_path, headless=False, options=options)
# driver = Chrome(executable_path=r'C:\Users\Deepak\Desktop\chromedriver.exe')

# set url and visit with browser
url = "https://www.yelp.com/"
b.visit(url)

# find and fill search parameters
search_type = b.find_by_id('find_desc')
search_city = b.find_by_id('dropperText_Mast')
search_button = b.find_by_id('header-search-submit')
time.sleep(5)
search_type.fill('Spa')
search_city.fill('Denver,CO')
search_button.click()

time.sleep(6)
try:
    filter_miles = b.find_by_xpath('//*[@id="wrap"]/div[3]/div[2]/div/div[1]/div[1]/div[1]/div/div[5]/div/div[2]/div[2]/div/label/div/div[1]/input').click()
    print('success for miles')
except:
    print('error') 

time.sleep(11)

# click filter button
def scrape(b):
    print('function called successfully')
    soup = bs(b.html, 'html.parser')

    # find reviews and total
    
    review_count = soup.find_all('span',{'class':'lemon--span__373c0__3997G text__373c0__2Kxyz reviewCount__373c0__2r4xT text-color--black-extra-light__373c0__2OyzO text-align--left__373c0__2XGa-'})

    reviews = []
    total_spa_reviews = 0
    for result in review_count:
        total_spa_reviews = int(result.text) + total_spa_reviews
    print(total_spa_reviews)

    # scrape all names from current page
    names = soup.find_all('a',{'class':'lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE'}) 
    name = []

    # save unique names to list
    for result in names:
        if(len(result.text) > 3):
            print(result.text)
            if result.text not in name:
                name.append(result.text)
scrape(b)

time.sleep(11)
# click next search page link
try:
    next_link = b.find_by_xpath('//*[@id="wrap"]/div[3]/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/div[11]/span/a').click()
    scrape(b)
except:
    b.quit()



