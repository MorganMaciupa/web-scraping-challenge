#DEPENDENCIES
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

def scrape_info():
    #Initiate browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    mars_info = {}

    #URL of the page to be scraped
    url_news = 'https://redplanetscience.com/'
    browser.visit(url_news)

    html_news = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html_news, 'html.parser')

    news_container = soup.select_one('div', class_='list_text')

    mars_info["news_title"] = news_container.find('div', class_='content_title').text
    mars_info["news_body"] = news_container.find('div', class_='article_teaser_body').text

    #PART 2
    #JPL Mars Space Images - Featured Image

    url_image = 'https://spaceimages-mars.com/'
    browser.visit(url_image)

    browser.links.find_by_partial_text('FULL IMAGE').click()

    html_image = browser.html
    image_soup = BeautifulSoup(html_image, 'html.parser')

    featured_image = image_soup.find('img', class_='fancybox-image')['src']
    mars_info["featured_image_url"] = url_image + featured_image

    #PART 3
    #Mars Facts
    url_facts = 'https://galaxyfacts-mars.com/'
    browser.visit(url_facts)
    tables = pd.read_html(url_facts)

    df = tables[0]
    df.columns = df.iloc[0]
    df = df[1:]

    df.to_html('table.html')

    #Mars Hemispheres
    # executable_path = {'executable_path': ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=False)

    hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(hemisphere_url)

    hemisphere_image_urls = []

    for x in range(0, 4):
        browser.find_by_css('img.thumb')[x].click()
        
        hemisphere_soup = BeautifulSoup(browser.html, 'html.parser')

        hemisphere_image = hemisphere_soup.find('img', class_='wide-image')['src']
        hemisphere_image_url = hemisphere_url + hemisphere_image
        
        hemisphere_title = hemisphere_soup.find('h2', class_='title').text
        
        title_and_url = {"title": hemisphere_title, 
                        "img_url": hemisphere_image_url}
        
        hemisphere_image_urls.append(title_and_url)
        
        browser.links.find_by_partial_text('Back').click()
    
    mars_info["hemisphere_image_urls"] = hemisphere_image_urls
        
    browser.quit()
    
    return mars_info