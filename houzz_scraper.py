from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep

results = pd.DataFrame(columns=['link', 'rating', 'address', 'phone_number',
'website_url', 'facebook', 'twitter', 'linkedin', 'instagramm'])



def get_links_from_page(df):
    links = driver.find_elements(By.CLASS_NAME, "hz-pro-ctl")
    for link in links:
        link_url = link.get_attribute("href")
        new_row = pd.Series({'link': link_url, 'rating': None, 'address': None, 
        'phone_number': None, 'website_url': None, 'twitter': None, 'linkedin': None, 'instagram': None})
        new_results = pd.concat([df, new_row.to_frame().T], ignore_index=True)
        df = new_results
    return df

def load_next_page(wait):
    next_button = driver.find_element(By.CLASS_NAME, "hz-pagination-next-page")
    wait.until(EC.element_to_be_clickable, next_button)
    next_button.click()
    wait.until(EC.element_to_be_clickable, next_button)

def is_next_button_present():
    sleep(5)
    try:
        nextBtn = driver.find_element(By.CLASS_NAME, "hz-pagination-next-page").is_displayed
        return True
    except:
        return False

def link_handler(element_array):
    if (len(element_array)>0):
        element = element_array[0]
        link = element.get_attribute("href")
    else:
        link = None
    return link

def string_handler(element_array):
    if (len(element_array)>0):
        element = element_array[0]
        value = element.text
    else:
        value = None
    return value  


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = "https://www.houzz.com/professionals/query/?tid=11785&l=Florida"
wait = WebDriverWait(driver, 10)
driver.get(url)
sleep(20)
results = get_links_from_page(results)

while is_next_button_present():
    load_next_page(wait)
    sleep(20)
    results = get_links_from_page(results)

for each in range(len(results)):
    driver.get(results.iloc[each]['link'])
    rating = driver.find_elements(By.CLASS_NAME, "hz-star-rate__rating-number")
    rating = string_handler(rating)
    phone_label = driver.find_elements(By.XPATH, '//h3[text()="Phone Number"]')
    if (len(phone_label)>0):
        phone_label = phone_label[0]
        phone_parent = phone_label.find_element(By.XPATH, '..')
        phone = phone_parent.find_elements(By.XPATH,"p[@class = 'sc-mwxddt-0 cZJFpr']")
        phone = string_handler(phone)
    else:
        phone = None
    
    website  = driver.find_elements(By.CLASS_NAME,"Website__EllipsisText-sc-19fzbgj-0")
    website = string_handler(website)
    address_label = driver.find_elements(By.XPATH, '//h3[text()="Address"]')
    if (len(address_label)>0):
        address_parent = address_label[0].find_element(By.XPATH, "..")
        address = address_parent.find_elements(By.TAG_NAME, 'p')
        address = string_handler(address)
    else:
        address = None
    facebook_link = driver.find_elements(By.XPATH, "a[@aria-label='Find me on Facebook']")
    twitter_link = driver.find_elements(By.XPATH, "a[@aria-label='Find me on Twitter']")
    linkedin_link = driver.find_elements(By.XPATH, "a[@aria-label='Find me on LinkedIn']")
    instagram_link = driver.find_elements(By.XPATH, "a[@aria-label='Find me on Instagram']")
    for s in [facebook_link, twitter_link, linkedin_link, instagram_link]:
        link_handler(s)
    results.at[each, 'rating'] = rating
    results.at[each, 'address'] = address
    results.at[each, 'phone_number'] = phone
    results.at[each, 'website_url'] = website
    results.at[each, 'twitter'] = twitter_link
    results.at[each, 'facebook'] = facebook_link
    results.at[each, 'linkedin'] = linkedin_link
    results.at[each, 'instagram'] = instagram_link

results.to_csv("result.csv")  

