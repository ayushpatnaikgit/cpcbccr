##Importing libraries
import re
from datetime import datetime
from datetime import timedelta
import base64
import requests
import dataset
import json
import hashlib 
import time
from selenium import webdriver
import datetime
from datetime import timedelta
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from dateutil.parser import parse
from selenium.webdriver.support.ui import Select

##Settings
options = Options()
options.headless = False
profile = FirefoxProfile()
#Scraping data for one day

url = "https://app.cpcbccr.com/AQI_India/"
driver = webdriver.Firefox(firefox_profile=profile,options=options)
driver.get(url)
time.sleep(5)
stations = []
statesList = Select(driver.find_element_by_id("states"))
states = len(statesList.options) -1
for s in range(1,states):
    statesList.select_by_index(s)
    time.sleep(2)
    citiesList = Select(driver.find_element_by_id("cities"))
    cities = len(citiesList.options)
    for c in range(1,cities): 
        citiesList.select_by_index(c)
        time.sleep(1)
        selector = Select(driver.find_element_by_id("stations"))
        options = selector.options
        for index in range(1, len(options)):
            stations.append([statesList.options[s].text,citiesList.options[c].text,options[index].get_attribute("value"),options[index].text])

print(stations)

db = dataset.connect('sqlite:///../data/db/data.sqlite3')
site_table = db["sites"]
for station in stations:
    row = {}
    row["state"] = station[0]
    row["city"] = station[1]
    row["site"] = station[2]
    row["site_name"] = station[3]
    site_table.insert(row)
