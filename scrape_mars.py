from bs4 import BeautifulSoup
import requests as req
import pymongo
import pandas as pd
from splinter import Browser
import time
import numpy as numpy
from selenium import webdriver



#initialize splinter browser object
def initBrowser():
    return Browser("chrome", headless=False)
    time.sleep(10)

def closeBrowser(browser):
    browser.quit()
    time.sleep(10)

def scrape():
    mars_data = {}
    mars_data["news_data"] = marsData()
    mars_data["featured_image_url"] = marsFeaturedImageURL()
    mars_data["tweet_weather"] = marsWeather()
    mars_data["mars_facts"] = marsFacts()
    mars_data["mars_img"] = marsHemishphereURL()

    return mars_data

def marsData():

    news_data = {}
    paragraph_text = []
    
    base_url = "https://mars.nasa.gov/"
    url = "https://mars.nasa.gov/news/"

    #browser.visit(url)
    #html=browser.html
    #soup = BeautifulSoup(html,'html.parser')
    response = req.get(url)
    time.sleep(5)

    news_title = response.find('div', class_='content_title').text
    news_p=response.find('div',class_='article_teaser_body').text

    news_data["news_title"] = news_title
    news_data["paragraph"]=news_p

    return news_data

def marsFeaturedImageURL():

    browser = initBrowser()

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    mars_full_size="https://www.jpl.nasa.gov/spaceimages/images/wallpaper/"
    browser.visit(url)
    html2 = browser.html
    bs_soup = BeautifulSoup(html2, 'html.parser')
    time.sleep(5)

    mars_image = []

    for img in bs_soup.find_all('div', class_="img"):
        mars_image.append(img.find('img').get('src'))

    featured_image = mars_image[0]
    split2 = featured_image.split('/')
    featured_image_url = mars_full_size + split2[-1]

    featured_image_url

    closeBrowser(browser)

    return featured_image_url


def marsWeather():

    browser = initBrowser()

    tweet = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet)
    tweet_html = browser.html
    bs_soup = BeautifulSoup(tweet_html, 'html.parser')
    time.sleep(5)

    mars_tweet_weather = []

    for mars_tweet in bs_soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
        mars_tweet_weather.append(mars_tweet.text.strip())

    for value in reversed(mars_tweet_weather):
        if value[:3]=='Sol':
            tweet_weather = value

    tweet_weather

    closeBrowser(browser)

    return tweet_weather

def marsFacts():
    mars_facts = 'https://space-facts.com/mars/'
    mars_list = pd.read_html(mars_facts)
    mars_df = mars_list[0]
    mars_table = mars_df.to_html(header=False, index = False)

    return mars_table


def marsHemishphereURL():
    browser = initBrowser()

    astro_url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astro_url)
    time.sleep(5)

    astro_html = browser.html
    astro_soup = BeautifulSoup(astro_html,'html.parser')
    time.sleep(5)

    mars_img = []

    products = astro_soup.find('div', class_='result-list')
    hemispheres = products.find_all('div', class_='item')

    for hemisphere in hemispheres:
    
        title = hemisphere.find('div', class_='description')
        
        clean_text = title.a.text
        clean_text = clean_text.replace(' Enhanced', '')
        browser.click_link_by_partial_text(clean_text)
        
        astro_html = browser.html
        astro_soup = BeautifulSoup(astro_html, 'html.parser')
     
        image = astro_soup.find('div', class_='downloads').find('ul').find('li')
        img_url = image.a['href']
     
        mars_img.append({'title': clean_text, 'img_url':img_url})
        
        browser.click_link_by_partial_text('Back')

    closeBrowser(browser)

    return mars_img

if __name__ =="__main__":
    print(scrape())


