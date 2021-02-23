# Dependencies
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests
#Dependencies Splinter
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
def scrape():
    browser = init_browser()
    
    ### NASA Mars News
    ## Visit Mars News URL
    url = 'https://mars.nasa.gov/news/page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    
    #Get the latest news headline
    news_title = soup.find('div', class_='content_title').text.strip()
    
    #Get the latest news article description
    news_p = soup.find('div', class_='rollover_description_inner').text.strip()
    

    ### JPL Mars Space Images - Featured Image
    ##Visit JPL URL
    base_url = 'https://www.jpl.nasa.gov'
    jpl_url = base_url + '/news/where-should-future-astronauts-land-on-mars-follow-the-water'
    browser.visit(jpl_url)
    
    #Scrape page into Soup
    html_img = browser.html
    soup = bs(html_img, 'html.parser')
    
    #Get the url for the JPL featured image
    featured_image_url = soup.find('img', class_="BaseImage object-contain")['data-src']

    ### Mars Facts
    facts_url = "https://space-facts.com/mars/"
    #Scrape tables
    tables = pd.read_html(facts_url)
    
    #Select html tables and convert to pandas df
    df = tables[0]
    
    #Convert pandas df to html string
    html_table = df.to_html()

    ### Mars Hemispheres
    #Visit USGS URL
    usgs_url = "https://astrogeology.usgs.gov"
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    
    #Scrape page into Soup
    hemi_html = browser.html
    soup = bs(hemi_html,'html.parser')
    
    #Create an empty list for the titles and urls
    hemi_img_dict = []
    hemi_items = soup.find_all('div', class_="item")
    
    for i in hemi_items:
        #Store the title of each hemisphere
        hemi_name = i.find('h3').text
    
        #Find image urls and combine with base url
        partial_hemi_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(usgs_url + partial_hemi_url)
        partial_hemi_html = browser.html
        
        soup = bs(partial_hemi_html, 'html.parser')
        
        full_hemi_url = usgs_url + soup.find('img', class_="wide-image")['src']
        
        #Append dictionary with results
        hemi_img_dict.append({"title": hemi_name, 
            "img_url": full_hemi_url})
        
    data = {
        "News_Header": news_title,
        "News_Description": news_p,
        "JPL Image": featured_img_url,
        "Mars_Facts": html_table,
        "Hemispheres": hemi_img_dict
    }
        
    #Quit browser session
    browser.quit()
    
    return data