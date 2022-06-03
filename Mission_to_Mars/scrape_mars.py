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
    
    #Create empty dictionary to store data
    mars_info = {}

    #-------------------------------------------------------------------------------
    #PART 1: NASA Mars News
    #-------------------------------------------------------------------------------
    
    #URL of the page to be scraped
    url_news = 'https://redplanetscience.com/'
    browser.visit(url_news)

    html_news = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html_news, 'html.parser')

    #Select the container with the news data
    news_container = soup.select_one('div', class_='list_text')

    #Save title and body in to data dictionary
    mars_info["news_title"] = news_container.find('div', class_='content_title').text
    mars_info["news_body"] = news_container.find('div', class_='article_teaser_body').text

    #-------------------------------------------------------------------------------
    #PART 2 - JPL Mars Space Images - Featured Image
    #-------------------------------------------------------------------------------

    #URL of the page to be scraped
    url_image = 'https://spaceimages-mars.com/'
    browser.visit(url_image)

    browser.links.find_by_partial_text('FULL IMAGE').click()

    html_image = browser.html
    
    # Create BeautifulSoup object; parse with 'html.parser'
    image_soup = BeautifulSoup(html_image, 'html.parser')

    #Use sopu to select the image required
    featured_image = image_soup.find('img', class_='fancybox-image')['src']
    
    #Save url in to data dictionary
    mars_info["featured_image_url"] = url_image + featured_image

    #-------------------------------------------------------------------------------
    #PART 3 - Mars Facts table
    #-------------------------------------------------------------------------------
    
    #URL of the page to be scraped
    url_facts = 'https://galaxyfacts-mars.com/'
    browser.visit(url_facts)
    
    #Use Pandas to read the html of web page
    tables = pd.read_html(url_facts)

    #Create a dataframe from the tables read from html
    df = tables[0]
    
    #Edit the dataframe to contain only rows required
    df.columns = df.iloc[0]
    df = df[1:]

    #Save dataframe as html
    df.to_html('table.html')

    #-------------------------------------------------------------------------------
    #PART 4 - Mars Hemispheres
    #-------------------------------------------------------------------------------

    #URL of the page to be scraped
    hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(hemisphere_url)

    #Create empty list to store scraped data
    hemisphere_image_urls = []

    #Use for loop to click through each hemisphere and store data to list
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
     
    #Close the browser   
    browser.quit()
    
    #Return the dictionary to app
    return mars_info