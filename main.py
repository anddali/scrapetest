# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 17:19:52 2021

@author: AD
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def scroll_page_down(driver):    
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        try:
            btn = driver.find_element_by_css_selector(".infinite-scroller__show-more-button.infinite-scroller__show-more-button--visible")
            btn.click()      
            time.sleep(2)
        except:
            pass
        if new_height == last_height:
            break
        last_height = new_height
    return driver
    
def main():    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    #data analyst
    #driver.get("https://www.linkedin.com/jobs/search/?geoId=104738515&keywords=data%20analyst&location=Ireland&sortBy=DD&f_TPR=r2592000&f_E=3%2C4&position=1&pageNum=0")
    #data scientist (finds data engineer, ml engineer, etc)
    driver.get("https://www.linkedin.com/jobs/search?keywords=Data%2BScientist&location=Ireland&geoId=104738515&trk=public_jobs_jobs-search-bar_search-submit&sortBy=DD&f_TPR=r2592000&position=1&pageNum=0")
    
    driver = scroll_page_down(driver)
    jobs_list = driver.find_element_by_class_name("jobs-search__results-list")
    jobs = jobs_list.find_elements_by_tag_name("li")
    
    descriptions = []
    location = []  
    seniority = []          
    for i in range(len(jobs)):        
        click_path = f"/html/body/main/div/section[2]/ul/li[{i+1}]/img"
        element = jobs_list.find_element_by_xpath(click_path)
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
        time.sleep(1)
        description_path = "/html/body/main/section/div[2]/section[2]/div"        
        d = driver.find_element_by_xpath(description_path).get_attribute("innerText")        
        d = driver.find_element_by_css_selector(".description__text.description__text--rich").get_attribute("innerText")        
        descriptions.append(d)
        location_path = "/html/body/main/section/div[2]/section[1]/div[1]/div[1]/h3[1]/span[2]"
        l = driver.find_element_by_xpath(location_path).get_attribute("innerText")
        location.append(l)
    
    
    print(len(descriptions))
    print(len(location))
    print(len(seniority))
    
    df = pd.DataFrame({'Location':location, 'Description':descriptions})
    df['Description'] = df['Description'].str.replace('\n','. ')
    df.to_csv('data_scientist.csv', index = 0)


if __name__=="__main__":
    main()
