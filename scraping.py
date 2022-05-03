# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt


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
        "URL_titles": hemisphere_scrape(browser)
    }
    # Stop webdriver and return data
    browser.quit()
    return data

# # Set up Splinter
# executable_path = {'executable_path': ChromeDriverManager().install()}
# browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # slide_elem = news_soup.select_one('div.list_text')

    # slide_elem.find('div', class_='content_title')

    # # Use the parent element to find the first a tag and save it as `news_title`
    # news_title = slide_elem.find('div', class_='content_title').get_text()
    # news_title

    # # Use the parent element to find the paragraph text
    # news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return news_title, news_p

# ## JPL Space Images Featured Image

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

    # # find the relative image url
    # img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    # # img_url_rel

    try:
    # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    # img_url
    return img_url

    # ## Mars Facts

# df = pd.read_html('https://galaxyfacts-mars.com')[0]
# df.head()

# df.columns=['Description', 'Mars', 'Earth']
# df.set_index('Description', inplace=True)
# df

# df.to_html()

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes ='table table-striped' , border=0)
# browser.quit()

def hemisphere_scrape(browser):

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    #initializing soup
    html = browser.html
    url_soup = soup(html, 'html.parser')
    #getting all div with description class
    all_page_URLs = url_soup.find_all('div',class_='description')
    title=[]

    #looping through all findigs
    for prod in all_page_URLs:
        #finding the desired links
        hyperlink = prod.find('a',class_='itemLink product-item')['href']
        #getting the title and removing \n
        title= (prod.find('a',class_='itemLink product-item').text.replace('\n',''))
        
        #creating the absolute URL
        full_URL = url + hyperlink
        
        #going to the new page and setting up Soup again
        browser.visit(full_URL)
        html = browser.html
        page2_soup = soup(html, 'html.parser')
        
        #looping though links to find the desired links
        for link in page2_soup.find_all('a',target='_blank'):
            # added this to avoid reading the links twice. 'Sample' is unique on the page.
            if link.text == 'Sample':
                img_url=(url+  link.get('href'))
        #updating the dictionary        
        hemisphere_image_urls.append({'img_url':img_url,'title':title})
    return hemisphere_image_urls