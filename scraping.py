
#import splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #initalize headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = True)

    news_title, news_paragraph = mars_news(browser)

    #run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "mars_facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "titles_and_img_urls": mars_urls(browser)
    }

    browser.quit()

    return data 


def mars_news(browser):

    #visit the mars nasa new site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    #try and except for error handling in case webpage can't be scraped 
    try:
        slide_elem = news_soup.select_one('div.list_text') # div class = 'list_text' contains both title and description

        slide_elem.find('div', class_= 'content_title')

        #use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_= 'content_title').get_text()

        #use the parent element to find the paragraph text 
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p


### Featured Images

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    #find and click the full image button 
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #parse the resulting html with soup 
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_url_rel
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    img_url

    return img_url


def mars_facts():

    try: 
        #pd.read_html reads html tables into a list of dataframe objects 
        #the table needed here is the first element in that list so it
        #gets accessed with [0]
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    return df.to_html(classes="table table-striped")

def mars_urls(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    new_soup = soup(html, "html.parser")

    all_elements = new_soup.find('div', class_="collapsible results")
    element = all_elements.find_all('div', class_="item")

    for hemi in element:
        hemispheres = {}
        href = hemi.h3.text #also the title 
        print(href)
        browser.click_link_by_partial_text(href)
        new_page = browser.html
        new_soup_again = soup(new_page, "html.parser")
        img_url = new_soup_again.find('img', class_="wide-image").get("src")
        print(img_url)
        img_url_1 = url+img_url
        img_url_1
        hemispheres['img_url'] = img_url_1
        hemispheres['title'] = href
        hemisphere_image_urls.append(hemispheres)
        browser.back()
    
    return hemisphere_image_urls


if __name__ == "__main__":
    #if running as a script, print scraped data 
    print(scrape_all()) #prints to terminal


