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
        "name": "Alexander Castillo"
    }
}


def random_sleep(wait_time=None):
    if wait_time == "test":
        sleep = random.randint(13, 15)
        time.sleep(sleep)
    else:
        pass


### will click the button or span or input
### breaks on 5 unsuccessful attempts
def clickable(xpath, driver):
    count = 0
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
            print('Input was RETURNED')
        finally:
            count += 1
            if count >= 5:
                print("Tried 5 times with failure, now stopping script")
                exit()
    random_sleep('test')

### selects givin string from a select tag
def selectable(xpath, select_string, driver):
    count = 0
    while True:
        try:
            select = Select(driver.find_element_by_xpath(xpath))
            select.select_by_value(select_string)
            break
        except WebDriverException as error:
            print(error)
            count += 1
            #### tells me if the xpath is wrong or select_string is wrong
        finally:
            if count >= 5:
                print("Tried 5 times with failure, now stopping script")
                exit()

### types text to an input tage
### 5 second render to response error
def text_input(xpath, input_string, driver):
    count = 0
    while True:
        try:
            input_text = driver.find_element_by_xpath(xpath)
            input_text.clear()
            for char in input_string:
                input_text.send_keys(char)
        except WebDriverException:
            if count > 5:
                exit()
            count += 1
            time.sleep(1)



def form_filler(data_dict, driver):
    for xpath, user_input in data_dict.items():
        if user_input[1] == 'select':
            selectable(xpath, user_input[0], driver)
        else:
            text_input(xpath, user_input[0], driver)


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
driver.get('https://www.newegg.com')
random_sleep('test')

driver.get('https://www.newegg.com/xpg-32gb-288-pin-ddr4-sdram/p/0RN-003P-001H1?Item=9SIAJNUBUM3271&cm_sp=Homepage_SS-_-P0_9SIAJNUBUM3271-_-02062021&quicklink=true')
random_sleep('test')


#### ADD TO CART ####
clickable("//div[@id='ProductBuy']/div/div[2]/button", driver)

##### PROTECTION PLAN POPUP #####
clickable("//button[@class='btn'][contains(text(),'No, thanks')]", driver)

##### VIEW CART AND CHECKOUT POP OUT MENU #####
clickable("//button[contains(text(),'View')]",driver)

#############################################
############ CART PAGE ######################
#############################################

##### CLOSE CART POPUP IF APPLICABLE #####
clickable("//button[@class='close']", driver)

##### SECURE CHECKOUT #####
clickable("//button[contains(@class,'btn-primary')][contains(text(),'Secure Checkout')]", driver)

#############################################
######## PAGE BTWN CHECKOUT AND CART ########
#############################################
##### GUEST CHECKOUT #####
clickable("//button[contains(@class,'btn')][contains(text(),'Guest')]", driver)

#############################################
######## SHIPPING ADDRESS PAGE ##############
#############################################
##### ADD NEW ADDRESS #####

clickable("//div[contains(@class,'card-add-new')]", driver)
##### SHIPPING ADDRESS INPUT #####
shipping_dict = {
    "//input[@name='FirstName']":[user['shipping']['firstname'], 'input'],
    "//input[@name='LastName']":[user['shipping']['lastname'], 'input'],
    "//input[@name='Address1']":[user['shipping']['street'], 'input'],
    "//input[@name='City']":[user['shipping']['city'], 'input'],
    "//select[@name='State']": [user['shipping']['state'], 'select'],
    "//input[@name='ZipCode']":[user['shipping']['zipcode'], 'input'],
    "//input[@name='Phone']":[user['shipping']['phone'], 'input'],
    "//input[@name='Email']":[user['shipping']['email'], 'input'],
}

# FILLS OUT SHIPPING ADDRESS #
form_filler(shipping_dict, driver)

# SAVES SHIPPING ADDRESS #
clickable("//button[contains(text(),'Save')]", driver)

##### CONTINUE IF EMAIL ADDRESS IN USE POPUP#####
clickable("//button[contains(@class,'btn-primary')][contains(text(),'Guest')]", driver)

##### CORRECT ADDRESS? POPUP #####
clickable("//button[contains(@class,'btn')][contains(text(),'Entered')]", driver)

##### SUGGESTED ADDRESS POPUP #####
### SUGGESTED ADDRESS xpath //div[@class='modal-body']/div[2]/div/div
clickable("//div[@class='modal-body']/div/div/div", driver)
## USE ADDRESS BUTTON ##
clickable("//div[@class='modal-content']/div[3]/button[2]", driver)

##### CONTINUE TO DELIVERY #####
clickable("//button[contains(@class,'btn-primary')][contains(text(),'delivery')]", driver)

################################
######## CHECKOUT PAGE #########
################################
##### SHIPPING CHOICE #####
# NOTE onlt the next day has a ID of NeweggNextDay
# if regular:
# CONTINUE TO PAYMENT #
clickable("//div[contains(@class,'checkout-step-action')]/button[contains(text(),'Continue')]", driver)

##### PAYMENT #####
# CLICK ADD NEW CREDIT CARD #
clickable("//div[@class='card card-add-new']", driver)
# PURCHASE DICTIONARY #
purchase_card_billing_dict = {
    "//div[@class='modal-content']/div[2]/div/div[1]/input": [user['purchase']['name'], 'input'],
    "//div[@class='modal-content']/div[2]/div/div[2]/input": [user['purchase']['creditCard'], 'input'],
    "//div[@class='modal-content']/div[2]/div/div[4]/label[2]/select": [user['purchase']['expMonth'], 'select'],
    "//div[@class='modal-content']/div[2]/div/div[5]/label/select": [user['purchase']['expYear'], 'select'],
    "//div[@class='modal-content']/div[2]/div[2]/div/div/div[1]/input": [user['billing']['street'], 'input'],
    "//div[@class='modal-content']/div[2]/div[2]/div/div/div[3]/input": [user['billing']['city'], 'input'],
    "//div[@class='modal-content']/div[2]/div[2]/div/div/div[4]/label[2]/select": [user['billing']['state'], 'select'],
    "//div[@class='modal-content']/div[2]/div[2]/div/div/div[5]/input": [user['billing']['zipcode'], 'input'],
    "//div[@class='modal-content']/div[2]/div[2]/div/div/div[6]/input": [user['billing']['phone'], 'input'],
}

## FILL OUT CARD NUMBER AND BILLING ADDRESS POPUP ##
form_filler(purchase_card_billing_dict, driver)

## ENTER CVV AFTER FILLING IN PURCHASE INFO ##
text_input("//div[@class='retype-security-code']", user['purchase']['cvv'], driver)

# REVIEW ORDER #
clickable("//button[contains(@class,'checkout-step-action-done')][contains(text(),'Review your order')]", driver)

#### IS THIS THE CORRECT ADDRESS #####
try:
    use_address = driver.find_element_by_xpath("//button[@class='btn'][contains(text(),'Use Address as Entered')]")
    use_address.click()
except WebDriverException:
    pass
##############################
######## REVIEW PAGE #########
##############################
clickable("//button[@id='btnCreditCard']", driver)