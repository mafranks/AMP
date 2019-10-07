#!/usr/bin/env python3
import requests
import time 
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
except:
    print("Please install selenium, install the chrome driver and try again.\npip install -U selenium\nhttps://sites.google.com/a/chromium.org/chromedriver/downloads")
    exit()
from creds import tg_username, tg_password

tg_url = "https://panacea.threatgrid.com/login"

### Change the CHROME DRIVER location or this will not work!!!###
chromedriver_location = '/Users/mafranks/Desktop/Python/Avg_Analysis_Time_TG/chromedriver'
options = webdriver.ChromeOptions()
options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
driver = webdriver.Chrome(chromedriver_location, chrome_options=options)
driver.get(tg_url)
time.sleep(2)
username_field = driver.find_element_by_name('login')
username_field.send_keys(tg_username)
password_field = driver.find_element_by_name('password')
password_field.send_keys(tg_password)
time.sleep(1)
password_field.send_keys(u'\ue007')
time.sleep(10)
avg_time = driver.find_elements_by_xpath('//*[@id="mask-dashboard-content"]/div[1]/div/div/div[1]/div/table/tbody/tr[2]/td')
diff = driver.find_elements_by_xpath('//*[@id="mask-dashboard-content"]/div[1]/div/div/div[1]/div/table/tbody/tr[3]/td')
print("Average Analysis Time: {}\nDifference: {}".format(avg_time[0].text, diff[0].text))
driver.quit()
