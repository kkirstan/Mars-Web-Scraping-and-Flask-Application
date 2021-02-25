# Dependencies
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests
import pymongo
#Dependencies Splinter
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars
collection = db.mars_data

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
    
def scrape():
    browser = init_browser()
    collection.drop()

    ### ---------------------------------------NASA Mars News---------------------------------------- ----###
    ## Visit Mars News URL
    url = 'https://mars.nasa.gov/news/page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'lxml')
    
    #Get the latest news headline
    news_title = soup.find('div', class_='content_title').text
    
    #Get the latest news article description
    news_p = soup.find('div', class_='rollover_description_inner').text
    

    ### ------------------------------JPL Mars Space Images - Featured Image -----------------------------###
    ##Visit JPL URL
    base_url = 'https://www.jpl.nasa.gov'
    jpl_url = base_url + '/news/where-should-future-astronauts-land-on-mars-follow-the-water'
    browser.visit(jpl_url)
    
    #Scrape page into Soup
    html_img = browser.html
    soup = bs(html_img, 'html.parser')
    
    #Get the url for the JPL featured image
    featured_img_url = soup.find('img', class_="BaseImage object-contain")['data-src']

    ### ----------------------------------------Mars Facts------------------------------------------------###
    facts_url = "https://space-facts.com/mars/"
    #Scrape tables
    tables = pd.read_html(facts_url)
    
    #Select html tables and convert to pandas df
    df = tables[0]
    
    #Convert pandas df to html string
    html_table = df.to_html()
    html_table = html_table.replace('\n','')
    
    ### -------------------------------------Mars Hemispheres---------------------------------------------###
    
    ##!!
    #URLs and connect to browser
    usgs_url = "https://astrogeology.usgs.gov"
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(hemi_url)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    
    #Create a dictionary to hold hemisphere name and url data
    hemisphere_image_urls = []
    
    #Retrieve parent tags for each hemisphere
    hemi_items = soup.find_all('div', class_="item")
    
    #Loop through each item in hemi_items[]
    for item in hemi_items:
        
        hemi_img_dict = {}
        
        #Extract title
        hem = item.find('div', class_='description')
        title = hem.h3.text
    
        #Extract image url
        hemi_url = hem.a['href']
        hemi_img_url = usgs_url + hemi_url
        browser.visit(hemi_img_url)
    
        time.sleep(1)
    
        html = browser.html
        soup = bs(html,'html.parser')
        img_src = soup.find('li').a['href']
            
        #Create a dictionary and append with the results
        hemi_img_dict = {
            'title': title,
            'image_url':img_src}
        
        hemisphere_image_urls.append(hemi_img_dict)

    browser.quit()

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_img_url": featured_img_url,
        "html_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    collection.insert(mars_data)

    return mars_data