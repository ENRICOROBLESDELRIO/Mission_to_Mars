#!/usr/bin/env python
# coding: utf-8

# In[70]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[71]:


# Set up Splinter
# With these two lines of code, we are creating an instance of a Splinter browser. 
# This means that we're prepping our automated browser.
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[72]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[73]:


# set up the HTML parser:
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[74]:


# We'll want to assign the title and summary text to variables we'll reference later.
slide_elem.find('div', class_='content_title')


# In[75]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[76]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Images

# In[77]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[78]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[79]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[80]:


# We'll use the image tag and class (<img />and fancybox-img) to build the URL to the full-size image.
# Find the relative image url
# An img tag is nested within this HTML, so we've included it.
# .get('src') pulls the link to the image.
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[81]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ## Mars Facts

# In[82]:


# Scrapping a table 
# Instead of scraping each row, or the data in each <td />, 
# we're going to scrape the entire table with Pandas' .read_html() function.
# By specifying an index of 0, we're telling Pandas to pull only the first table it encounters
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[83]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# In[165]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[166]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemisphere_soup = soup(html, 'html.parser')

hemisphere_description = hemisphere_soup.find_all('div', class_='description')

for x in hemisphere_description:
    title = x.find('h3').text
    link = f'https://marshemispheres.com/{x.find("a")["href"]}'
    print(title)
    # print(link) just for testing and see the link
    
    # Visit the link to the next page with full description to get img url.
    browser.visit(link)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    
    # Parse the resulting html with soup
    html = browser.html
    img_url = soup(html, 'html.parser')
    
    # Find the url for the img in .jpg
    img_div = img_url.find('div', class_='downloads')
    img_jpg = f'https://marshemispheres.com/{img_div.find("a")["href"]}'
    print(img_jpg)
    
    # Dictionary to holds links and titles
    hemisphere_dic = {}
    hemisphere_dic["title"] = title
    hemisphere_dic["url"] = img_jpg
    
    hemisphere_image_urls.append(hemisphere_dic)


# In[167]:


print(img_div)


# In[168]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[169]:


# 5. Quit the browser
browser.quit()


# In[ ]:




