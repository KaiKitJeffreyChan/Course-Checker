from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client
from decouple import config
import keys
import time
import os

USER = config('USER_ID')
PASS = config('PASS')
TARGET_NUM = config('TARGET_NUMBER')
AUTH = config('AUTH')

driver = webdriver.Chrome(executable_path="Drivers/chromedriver")

driver.get(
    "https://epprd.mcmaster.ca/psp/prepprd/?cmd=login&languageCd=ENG&")

driver.implicitly_wait(10)
username = driver.find_element_by_id("userid")
username.send_keys(USER)

password = driver.find_element_by_id("pwd")
password.send_keys(PASS)

driver.find_element_by_name('Submit').click()

driver.find_element_by_xpath('//*[@id="MCM_IMG_CLASS$10"]').click()

# press enroll top left
frame = driver.find_element_by_xpath('//*[@id="ptifrmtgtframe"]')
driver.switch_to.frame(frame)
driver.find_element_by_id('DERIVED_SSS_SCR_SSS_LINK_ANCHOR3').click()

# uncomment line 40 and comment line 42 if your course is in winter semester
# although you might need to check the other ID's as they may be different

# driver.find_element_by_id('SSR_DUMMY_RECV1$sels$2$$0').click()

driver.find_element_by_id('SSR_DUMMY_RECV1$sels$1$$0').click()
driver.find_element_by_id('DERIVED_SSS_SCT_SSR_PB_GO').click()

while True:
    driver.find_element_by_id('DERIVED_REGFRM1_LINK_ADD_ENRL$82$').click()

    try:
        driver.find_element_by_id('DERIVED_REGFRM1_SSR_PB_SUBMIT').click()
    except:
        driver.switch_to.default_content
        driver.find_element_by_id('DERIVED_REGFRM1_SSR_PB_SUBMIT').click()

    message = driver.find_element_by_xpath(
        '//*[@id="win0divDERIVED_REGFRM1_SS_MESSAGE_LONG$0"]/div').text
    if message != "Error: Available seats are reserved and you do not meet the reserve capacity criteria.":
        client = Client(keys.account_sid, AUTH)

        message = client.messages.create(
            body="Your course has been selected!",
            from_=keys.twilio_number,
            to=TARGET_NUM
        )
        print(message.body)
        driver.quit()
    else:
        driver.find_element_by_xpath('//*[@id="selectedtab"]/a').click()
    print("Tried")
    # checks every 5 min
    time.sleep(300)
