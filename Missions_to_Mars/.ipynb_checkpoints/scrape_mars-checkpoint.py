#!/usr/bin/env python
# coding: utf-8

# In[45]:


# Dependencies
from bs4 import BeautifulSoup
import requests
from requests import get
import pandas as pd
import numpy as np
import time


# NASA Mars News

# In[2]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'


# In[3]:


# Retrieve page with the requests module
response = requests.get(url)


# In[4]:


# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(response.text, 'html.parser')


# In[5]:


# Examine the results, then determine element that contains sought info
print(soup.prettify())


# In[12]:


#Collect the latest News Title and assign to variable
news_title = soup.find('div', class_='content_title').text.strip()
news_title


# In[22]:


#Collect the latest News Paragraph and assign to variable
news_p = soup.find('div', class_='rollover_description_inner').text.strip()
news_p


# JPL Mars Space Images - Featured Image

# In[9]:


#Dependencies Splinter
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# In[10]:


#Set up splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[19]:


#URL to visit
base_url = 'https://www.jpl.nasa.gov'
url = base_url + '/news/where-should-future-astronauts-land-on-mars-follow-the-water'


# In[20]:


#Connect to browser
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[27]:


#Find link to current JPL Featured Space Image
featured_image_url = soup.find('img', class_="BaseImage object-contain")
featured_image_url['data-src']


# Mars Facts

# In[28]:


url = "https://space-facts.com/mars/"


# In[29]:


#Scrape tables
tables = pd.read_html(url)
tables


# In[30]:


type(tables)


# In[35]:


#Select html tables and convert to pandas df
df = tables[0]
df.head(10)


# In[36]:


#Convert pandas df to html string
html_table = df.to_html()
html_table


# In[37]:


#Strip unwanted newlines to clean up table
html_table.replace('\n', '')


# In[38]:


#Save table to html file
df.to_html('mars_facts_table.html')


# Mars Hemispheres

# In[46]:


#Dependencies Splinter
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# In[47]:


#Set up splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[48]:


#URLs and connect to browser
usgs_url = "https://astrogeology.usgs.gov"
hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

browser.visit(hemi_url)
time.sleep(2)

html = browser.html
soup = BeautifulSoup(html,'html.parser')


# In[49]:


#Create a dictionary to hold hemisphere name and url data
hemi_img_dict = []


# In[50]:


#Retrieve parent tags for each hemisphere
hemi_items = soup.find_all('div', class_="item")


# In[51]:


#Loop through each item in hemi_items[]
for hemisphere in range(len(hemi_items)):
    #Use splinter to click on each hemisphere's link and retrieve data
    hemi_link = browser.find_by_css("a.product-item h3")
    hemi_link[hemisphere].click()
    time.sleep(1)
    
    #Connect to browser
    img_html = browser.html
    img_url = BeautifulSoup(img_html, 'html.parser')
    
    #Find image urls and combine with base url
    hemi_url = img_url.find('img', class_="wide-image")['src']
    hemi_img_url = usgs_url + hemi_url
    
    #Find hemisphere names
    hemi_name = browser.find_by_css('.title').text
    
    #Append dictionary with results
    hemi_img_dict.append({"title": hemi_name, "img_url": hemi_img_url})
    
    #Go back to main page
    browser.back()
    
#Quit browser session
browser.quit()

#View dictionary
hemi_img_dict


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




