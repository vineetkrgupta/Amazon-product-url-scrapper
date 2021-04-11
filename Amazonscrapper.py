from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.chrome.options import *

import unittest, time, re
import requests
import json
import time
import pandas as pd

def search_amazon(item ,pincode , page=1 , hid=False): # by default it doesnt run in headless mode
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    # all this stupidiy is required for implementing it on heroku otherwise crash is there
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15')
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--incognito")
    if(hid==True):
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install() , chrome_options=chrome_options)
    
    driver.delete_all_cookies()


    driver.get("https://www.amazon.in/")
    # try:
    driver.implicitly_wait(10)

    try:
        driver.find_element_by_id("glow-ingress-line1").click()
        driver.implicitly_wait(10)
        driver.find_element_by_id("GLUXZipUpdateInput").click()
        driver.implicitly_wait(10)
        driver.find_element_by_id("GLUXZipUpdateInput").clear()
        driver.implicitly_wait(10)
        driver.find_element_by_id("GLUXZipUpdateInput").send_keys(pincode)
        driver.implicitly_wait(10)
        driver.find_element_by_xpath("(//input[@type='submit'])[7]").click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath("(//input[@id='GLUXConfirmClose'])[2]").click()
        driver.implicitly_wait(10)
    except:
        print("couldn't set pincode due to some error procedding further")
        driver.get("https://www.amazon.com/")
        driver.implicitly_wait(10)

    # #driver.find_element_by_id("GLUXZipUpdateInput").send_keys(Keys.ENTER)
    
    # # driver.find_element_by_id("glow-ingress-line1").click()
    # # driver.find_element_by_id("GLUXZipUpdateInput").click()
    # # driver.find_element_by_id("GLUXZipUpdateInput").clear()
    # # driver.find_element_by_id("GLUXZipUpdateInput").send_keys("94023")
    # driver.implicitly_wait(10)






    #driver.implicitly_wait(10)
    driver.find_element_by_id("twotabsearchtextbox").click()
    driver.implicitly_wait(10)
    driver.find_element_by_id("twotabsearchtextbox").clear()
    driver.implicitly_wait(10)
    driver.find_element_by_id("twotabsearchtextbox").send_keys("dog food")
    driver.implicitly_wait(10)
    driver.find_element_by_id("nav-search-bar-form").submit()
    driver.implicitly_wait(10)
    # except:
    #     print("Error occured terminating program.")
    #     exit()

    filetxt= item+".txt"
    f = open(filetxt , "w+")
    # links= driver.execute_script("return document.getElementsByClassName('a-link-normal s-no-outline');")
    # print(links)
    for i in range(page):
        try:
            driver.implicitly_wait(10)
            lin=driver.execute_script("x =document.getElementsByClassName('a-link-normal s-no-outline'); var m =[]; for( var i=0; i<x.length; i++){ m.push(x[i]['href']);} return m;")
            if(i==0):
                line= lin
            else:
                line = line + lin
            print("Scrapped Page no " , i+1)
            driver.implicitly_wait(10)
            driver.find_element_by_link_text(u"Next→").click()
        except:
            pass 

    for x in line: # text file for simplicity 
        f.write(x)
        f.write("\n")
    

    df = pd.DataFrame(line)
    df.to_csv(item+".csv") #csv file writing 

    driver.quit()
    f.close()
    print("Task complete")

#search_amazon("Dog food" ,"94023" , 2 , False)