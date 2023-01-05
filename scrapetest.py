from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("--log-level=3")

def scroll_page_down(driver):    
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")        
        if new_height == last_height:
            break
        last_height = new_height
    return driver

def scrape_articles(link_list):    
    for article_link in link_list:
        try:
            time.sleep(2)
            driver = webdriver.Chrome("chromedriver",chrome_options=options)            
            driver.get(article_link)
            print("Got page!")
            article_subtitle = driver.find_element(By.CLASS_NAME,"subtitle").text
            article_text = driver.find_element(By.CLASS_NAME,"available-content").text            
            with open(f"results/{article_link.split('/')[-1]}.txt", "w") as f:
                f.write(f"{article_subtitle}\n\n{article_text}")
            driver.close()                         
        except:
            print(f"Failed to get link {article_link}")
            driver.close()
            pass


if __name__=="__main__":    
    driver = webdriver.Chrome("chromedriver",chrome_options=options)    
    driver.get("https://www.deeplearningweekly.com/archive")
    driver = scroll_page_down(driver)
    link_list = driver.find_elements(By.CLASS_NAME,"post-preview-description")
    link_list = [elem.get_attribute('href') for elem in link_list]
    driver.close()
    print(f"No of links found: {len(link_list)}")    
    scrape_articles(link_list[0:6])
    
