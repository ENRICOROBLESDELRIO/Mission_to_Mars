# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# This function will:
## - Initialize the browser.
## - Create a data dictionary.
## - End the WebDriver and return the scraped data.
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_data(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # # Convert the browser html to a soup object and then quit the browser
    # set up the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None    

    return news_title, news_p    

# ### JPL Space Images Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try: 
        # We'll use the image tag and class (<img />and fancybox-img) to build the URL to the full-size image.
        # Find the relative image url
        # An img tag is nested within this HTML, so we've included it.
        # .get('src') pulls the link to the image.
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## Mars Facts

def mars_facts():

    # Add try/except for error handling
    try: 
        # Scrapping a table 
        # Use 'read_html' to scrape the facts table into a dataframe
        # Instead of scraping each row, or the data in each <td />, 
        # we're going to scrape the entire table with Pandas' .read_html() function.
        # By specifying an index of 0, we're telling Pandas to pull only the first table it encounters
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
      return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)  

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-hover")

def hemisphere_data(browser):

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')

    hemisphere_description = hemisphere_soup.find_all('div', class_='description')
    
    # Iterate through div class descrption to get the titles and links to full jpg in next page
    for x in hemisphere_description:
        title = x.find('h3').text
        link = f'https://marshemispheres.com/{x.find("a")["href"]}'
    
    
        # Visit the link to the next page with full description to get img url.
        browser.visit(link)
        # Optional delay for loading the page
        browser.is_element_present_by_css('div.list_text', wait_time=1)
    
        # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')
    
        # Find the url for the img in .jpg
        img_div = img_soup.find('div', class_='downloads')
        img_url = f'https://marshemispheres.com/{img_div.find("a")["href"]}'
        print(img_url)
    
         # Dictionary to holds links and titles
        hemispheres = {}
        hemispheres["title"] = title
        hemispheres["url"] = img_url
    
        hemisphere_image_urls.append(hemispheres)

    return hemisphere_image_urls

# This last block of code tells Flask that our script is complete and ready for action. 
# The print statement will print out the results of our scraping to our terminal after executing the code.
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())