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

item = "ps5"
url = "https://www.target.com/p/playstation-5-digital-edition-console/-/A-81114596"
same_billing_address = True
digital = True
user = {
    "login":{
        "email":"cinema_333@live.com",
        "password":"RichPuss$2145",
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
        "zipCode":"80015",
        "email":"castleadagency@gmail.com",
    },
    "purchase" : {
        "creditCard": "4185123412341234",
        "expDate":"10/24",
        "expMonth": "10",
        "expYear": "24",
        "cvv": "123",
        "cardName": "Alexander J Castillo"
    }
}

#! target needs a target account
## FORM FOR LOOP ##
def input_keys(a_string, a_element):
    # add a random wait time to this function so all input types are types at diffrent speeds
    # wait_time = random.random() * .1
    a_element.clear()
    for char in a_string:
        a_element.send_keys(char)


def random_sleep(wait_time="standard"):
    if wait_time == "standard":
        sleep = random.randint(13, 15)
        time.sleep(sleep)


def add_to_cart(xpath, driver, tag='button'):
    while True:
        try:
            add_to_cart = driver.find_element_by_xpath(xpath)
            if tag == 'button':
                add_to_cart.send_keys(Keys.RETURN)
            else:
                add_to_cart.click()
            break
        except NoSuchElementException as error:
            print(error)
            time.sleep(15)
            driver.refresh()
        except NoSuchAttributeException as error:
            print(error)
            time.sleep(15)
            driver.refresh()
        except WebDriverException as error:
            print(error)
            time.sleep(15)
            driver.refresh()


#Open Browser
option = webdriver.ChromeOptions()
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_argument("window-size=1280,800")
option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
option.add_argument("proxy-server=156.248.69.24")
# cacheing
# options.add_argument("--profile-directory=<profile>') bestbuybot\botdrivers
driver = webdriver.Chrome(executable_path='websitebots/botdrivers/chromedriver.exe',options=option)

#Remove navigator.webdriver Flag using JavaScript
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


# must go through paths that a user would go through. This triggers bot flags
driver.get('https://www.google.com')
time.sleep(14)
driver.get('https://www.target.com')
time.sleep(14)

driver.get(url)

random_sleep()

# pick_it_up_button = driver.find_element_by_xpath("//*[contains(text(), 'Pick it up')]")
# pick_it_up_button.send_keys()
add_to_cart("//*[contains(text(), 'Pick it up')]", driver)


##### INCASE THE "PROTECT YOUR PURCHASE" POPS UP #####
try:
    decline_coverage_popup = driver.find_element_by_xpath("//button[contains(text(),'Decline coverage')]")
    decline_coverage_popup.send_keys(Keys.RETURN)
except WebDriverException:
    pass

random_sleep()

#### VIEW CART AFTER IN POPUP ####
while True:
    try:
        view_cart_button = driver.find_element_by_xpath("//*[contains(text(),'View cart & checkout')]")
        view_cart_button.send_keys(Keys.RETURN)
        break
    except WebDriverException as error:
        print(error)
        random_sleep()
random_sleep()


##### JUMP STRAIGHT TO CART ######
driver.get('https://www.target.com/co-cart')


while True:
    try:
        checkout_button = driver.find_element_by_xpath("//*[contains(text(), 'ready to check out')]")
        checkout_button.send_keys(Keys.RETURN)
        break
    except WebDriverException as error:
        print(error)


##### LOGIN IS REQUIRED FOR TARGET CHECKOUT #####
username = driver.find_element_by_xpath("//input[@id='username']")
input_keys(user['login']['username'], username)

password = driver.find_element_by_xpath("//input[@id='password']")
input_keys(user['login']['password'], password)


###### PURCHASEING CONSOLES ONLY AND ITS ONLY FOR PICKUP #######
###### BILLING ADDRESS AND CREDIT CARD INFO #######
###### PURCHASE ######
purchase_credit_card = driver.find_element_by_xpath("//input[@id='creditCardInput-cardNumber']")
input_keys(user['purchase']['creditCard'], purchase_credit_card)

purchase_exp_date = driver.find_element_by_xpath("//input[contains(@id,'expiration')]")
input_keys(user['purchase']['expDate'],purchase_exp_date)

purchase_cvv = driver.find_element_by_xpath("//input[contains(@id,'cvv')]")
input_keys(user['purchase']['cvv'], purchase_cvv)

purchase_card_name = driver.find_element_by_xpath("//input[contains(@id,'cardName')]")
input_keys(user['purchase']['cardName'], purchase_card_name)


###### BILLING ######
billing_street_address = driver.find_element_by_xpath("//input[contains(@id,'addressLine1')]")
input_keys(user['billing']['street'], billing_street_address)

billing_zipcode = driver.find_element_by_xpath("//input[contains(@id,'zipCode')]")
input_keys(user['billing']['zipCode'], billing_zipcode)

billing_city = driver.find_element_by_xpath("//input[contains(@id,'city')]")
input_keys(user['billing']['city'], billing_city)

billing_state = Select(driver.find_element_by_xpath("//select[contains(@id,'state')]"))
billing_state.select_by_value(user['billing']['state'])

billing_phone = driver.find_element_by_xpath("//input[contains(@id,'mobile')]")
input_keys(user['shipping']['phone'], billing_phone)


##### SAVE AND CONTINUE BUTTON #####
save_and_continue_button = driver.find_element_by_xpath("//button[contains(text(),'Save and continue')]")
save_and_continue_button.send_keys(Keys.RETURN)


##### PLACE YOUR ORDER #####
place_order_button = driver.find_element_by_xpath("//button[contains(text(),'Place your order')]")
place_order_button.send_keys(Keys.RETURN)