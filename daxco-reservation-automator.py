#!/usr/bin/env python
# coding: utf-8

# In[2]:


import credentials
import datetime
import time
from selenium import webdriver

#Initializes username and password from credentials file
user_id = credentials.login['username']
user_password = credentials.login['password']

#Opens up Daxko login page
login_url = "https://operations.daxko.com/online/5010/Security/login.mvc/find_account"
driver = webdriver.Firefox()
driver.get(login_url)

#Enters usename and proceeds to next page 
username = driver.find_element_by_id("user_name")
username.clear()
username.send_keys(user_id)
driver.find_element_by_id("submit_button").click()

#Enters password and proceeds to next page
password = driver.find_element_by_id("password")
password.clear()
password.send_keys(user_password)
driver.find_element_by_id("submit_button").click()

#Gets the current weekday and initalizes the date of reservation; in this case, reservations can only be made two days in advance
weekday = datetime.datetime.today().weekday()
if weekday > 4:
    weekday_code = weekday + 1 - 7 #Ensures that the weekday code ranges from 1-7, inclusive
else:
    weekday_code = weekday + 1
reservation_weekday_code = weekday_code + 2
    
#Initializes start time of reservation; the end time should be a minute after the reservation time to make sure the desired session is the only search result 
start_hour = "12"
if weekday_code > 5: #in this specific example, reservation time for weekends are different than on weekdays
    start_minute = "00" 
else:
    start_minute = "30"
end_hour = "12"
end_minute = "31"

#Initializes the date and time of when the reservation will be booked
target_year = datetime.date.today().year
target_month = datetime.date.today().month
target_day = datetime.date.today().day
target_hour = int(start_hour)
target_minute = int(start_minute)

#Pauses code until reservation opens up
target_time = datetime.datetime(target_year, target_month, target_day, target_hour, target_minute)
print (target_time)
while datetime.datetime.now() < target_time:
    time.sleep(1)
    print ('Running in ' + str(((target_time - datetime.datetime.now()).seconds)) + ' seconds.')
print('Now running the rest of the code')

#Creates search result URL targeted to display the only class available and goes to URL
URL = "https://operations.daxko.com/Online/5010/ProgramsV2/Search.mvc?keywords=&program_id=TMP33192&expanded=categories%2Clocations%2Cdays_offered%2Ctime_ranges&coming_soon=False&category_ids=TAG15347&all_categories=false&location_ids=S621&all_locations=false&days_offered=" + str(reservation_weekday_code) + "&time_range=on&time_ranges%5B0%5D.start=" + start_hour + "%3A" + start_minute + "&time_ranges%5B0%5D.end=" + end_hour + "%3A" + end_minute + "&date_ranges%5B0%5D.start=&date_ranges%5B0%5D.end=&birth_dates="
driver.get(URL)

#Clicks on event page
element = driver.find_element_by_xpath("//a[@class='programResults__offering-name ga-event']")
element.click()

#Clicks register on event page
element = driver.find_element_by_xpath("//input[@type='button']")
element.click()

#Finalizes registration
element = driver.find_element_by_xpath("//button[@type='submit']")
element.click()

