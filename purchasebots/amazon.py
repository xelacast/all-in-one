from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # these are keyboard inputs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.color import Color
from selenium.common.exceptions import WebDriverException, NoSuchElementException, NoSuchAttributeException
import time
import random


#! Amazon account must have one address in it and one card account in it to simplify things


same_billing_address = True
digital = True
user = {
    "login":{
        "email":"uniqrn3@gmail.com",
        "password":"Uniqrn03",
        "username":""
    },
    "shipping" : {
        "firstname":"John",
        "lastname":"Smith",
        "street":"5428 S Valdai St",
        "phone":"3035177516",
        "city":"Centennial",
        "state":"CO",
        "country": "US",
        "zipcode":"80015",
        "email":"castleadagency@gmail.com",
    },
    "billing": {
        "firstname":"John",
        "lastname":"Smith",
        "street":"5428 S Valdai St",
        "phone":"3035177516",
        "city":"Centennial",
        "state":"CO",
        "country": "US",
        "zipcode":"80015",
        "email":"castleadagency@gmail.com",
    },
    "purchase" : {
        "creditCard": "4185123412341234",
        "expMonth": "10",
        "expYear": "24",
        "cvv": "123",
    }
}


def random_sleep(wait_time=None):
    if wait_time == "test":
        sleep = random.randint(13, 15)
        time.sleep(sleep)
    else:
        pass


def clickable(xpath, driver):
    while True:
        try:
            button = driver.find_element_by_xpath(xpath)
            button.send_keys(Keys.RETURN)
            break
        except WebDriverException:
            button = driver.find_element_by_xpath(xpath)
            button.click()
            break
        else:
            print('input was Returned')

def selectable(xpath, select_string, driver):
    count = 0
    while True:
        try:
            select = Select(driver.find_element_by_xpath(xpath))
            select.select_by_value(select_string)
            break
        except WebDriverException as error:
            print(error)
            #### tells me if the xpath is wrong or select_string is wrong
            count += 1
            if count >= 5:
                break

def text_input(xpath, input_string, driver):
    input_text = driver.find_element_by_xpath(xpath)
    input_text.clear()
    for char in input_string:
        input_text.send_keys(char)


#Open Browser
option = webdriver.ChromeOptions()
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_argument("window-size=1280,800")
# option.add_argument('--desktop-window-1080p')
option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
# option.add_argument("proxy-server=192.171.93.40")
# cacheing
# options.add_argument("--profile-directory=<profile>') bestbuybot\botdrivers
driver = webdriver.Chrome(executable_path='websitebots/botdrivers/chromedriver.exe',options=option)

#Remove navigator.webdriver Flag using JavaScript
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


# must go through paths that a user would go through. This triggers bot flags
driver.get('https://www.google.com')
random_sleep('test')
driver.get('https://www.amazon.com')
random_sleep('test')


driver.get('https://www.amazon.com/dp/B01GTQPI64/ref=va_live_carousel?pf_rd_r=ZC1RPRX5KT6FZNBAPCE9&pf_rd_p=5b5d7300-2b45-4fd4-8dfd-5acfae3e5171&pf_rd_m=ATVPDKIKX0DER&pf_rd_t=Gateway&pf_rd_i=desktop&pf_rd_s=desktop-2&linkCode=ilv&tag=tom2-20&pd_rd_i=B01GTQPI64')

random_sleep('test')

##### Add item to cart ######
clickable("//input[@id='add-to-cart-button']", driver)
random_sleep('test')

##### Go to checkout #####
clickable("//span[contains(@class,'checkout-button')]", driver)
random_sleep('test')

##### Login Email #####
text_input("//input[@id='ap_email']", user['login']['email'], driver)
clickable("//span[@id='continue']", driver)
random_sleep('test')

##### Login Password #####
text_input("//input[@id='ap_password']", user['login']['email'], driver)
clickable("//span[@id='auth-signin-button']", driver)
random_sleep('test')

#! This is only for people who have an active account
# NOTE #! NO ACCOUNT CREATION BOT

##### Choose shipping adress #####
# choose shipping address
clickable(f"//span[contains(text(),'{user['shipping']['street'].upper()}')]", driver)
# 'use this address' input #
clickable("//span[@id='orderSummaryPrimaryActionBtn-announce']", driver)
random_sleep('test')

##### Choose credit card #####
# choose credit card #
clickable(f"//span[@class='pmts-cc-detail']/span[contains(text(),{user['purchase']['creditCard'][-4:]})]", driver)
# 'use this payment method' input #
clickable("//span[@id='orderSummaryPrimaryActionBtn']", driver)
random_sleep('test')

##### CHOOSE SHIPPING METHOD #####

##### PLACE YOUR ORDER #####
clickable("//span[@id='bottomSubmitOrderButtonId']", driver)