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

item = "ps5"
url = "https://www.gamestop.com/video-games/playstation-5/games/products/call-of-duty-black-ops-cold-war/11103153.html?condition=Pre-Owned"


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


def add_to_cart(xpath, driver):
    while True:
        try:
            add_to_cart = driver.find_element_by_xpath(xpath)
            add_to_cart.send_keys(Keys.RETURN)
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
time.sleep(14)
driver.get('https://www.gamestop.com')
time.sleep(7)

#####? add the bot to navigate through the website to the product instead of gettting it ?#####
##### How much time would this add to the checkout time? #####

# driver.get(url)

###################
###################
###################
###################
##### MIGHT NOT NEED THIS #####
##### CLICK THROUGH API TO GET TO PRODUCT ######
consoles_hardware = driver.find_element_by_xpath("//li[@class='nav-item dropdown'][2]/a/span[contains(text(),'Consoles & Hardware')]")
consoles_hardware.click()
random_sleep()

if item == 'ps5':
    ps5_menu_span = driver.find_element_by_xpath("//ul[@class='menu-list level-2']/li/a/span[contains(text(),'Playstation 5')]")
    ps5_menu_span.click()
random_sleep()
# elif item == 'xbox':
#     xbox_menu_span = driver.find_element_by_xpath("//ul[@class='menu-list level-2']/li/a/span[contains(text(),'Xbox Series X')]")
#     xbox_menu_span.click()

##### DIGITAL EDITION #####
if digital:
    ps5_digital_edition_image = driver.find_element_by_xpath("//div[@class='product-tiles-row']/div[1]/div/div/div")
    ps5_digital_edition_image.click()

##### DISK EDITION #####
else:
    ps5_disk_edition_image = driver.find_element_by_xpath("//div[@class='product-tiles-row']/div[2]/div/div/div")
    ps5_disk_edition_image.click()
#####################
#####################
#####################
#####################


random_sleep()
count = 0
while True:

    try:
        add_to_cart_button = driver.find_element_by_xpath("//button[contains(@class,'add-to-cart btn')]")
        add_to_cart_button.send_keys(Keys.RETURN)
        break
    except WebDriverException:
        count += 1
        print("refresh count = ", count)
        time.sleep(15)
        driver.refresh()

random_sleep

# driver.get("https://www.gamestop.com/cart")
#! you can RETURN or .click() on a attributes
#! THE API KEEPS ON CHANGING EVERYTIME I LOG ON
#####? clicked on add to cart button on pop-up menu ####w
while True:
    try:
        add_to_cart_icon = driver.find_element_by_xpath("//div[@class='addtocartlink']/a")
        add_to_cart_icon.click()
        break
    except WebDriverException:
        try:
            go_to_cart_button = driver.find_element_by_xpath("//a[contains(@class,'goto-cart')]")
            go_to_cart_button.click()
            break
        except WebDriverException:
            driver.get("https://www.gamestop.com/cart")
            break


##### UNDER SEVENTEEN ITEMS CHECK #####
random_sleep()
count = 0
while True:
    try:
        im_seventeen_or_older = driver.find_element_by_xpath("btn btn-outline-primary under-17")
        im_seventeen_or_older.send_keys(Keys.RETURN)
        random_sleep()
        break
    except WebDriverException as error:
        pass

##### CHECKOUT BUTTON CLICK ######

while True:
    try:
        # NOTE DO NOT TAKE OUT SPACE AFTER checkout-btn
        checkout_button = driver.find_element_by_xpath("//div[@class='checkout-and-applepay']/a[@class='mb-2 mx-0 btn btn-primary btn-block checkout-btn ']")
        checkout_button.send_keys(Keys.RETURN)
        print("Returned check out button")
        break
    except WebDriverException:
        pass

random_sleep()

####? RETURING COSUTOMER ?####
####! CUSTOMERS HAVE TO HAVE AN ACCOUNT WITH GAMESTOP !#####
#####?? WILL THIS ALLOW ME TO SKIP BILLING INFO ??##### I HAVE TO TEST IT

###### SIGN IN ######
login_email = driver.find_element_by_xpath("//input[@id='login-form-email']")
input_keys(user["login"]["email"], login_email)

login_password = driver.find_element_by_xpath("//input[@id='login-form-password']")
input_keys(user["login"]["password"], login_password)

sign_in_button = driver.find_element_by_xpath("//div[contains(@class,'login-form')]/form/button")
sign_in_button.click()


random_sleep()

#!############!#
# NOTE: This needs to be variables from an input field with a GUI


#####? Shipping ?#####
#! gamestops api for shipping and checkout keep changing on me.
# I can continue as guest sometimes but most the time I have to sign in.
add_new_address = driver.find_element_by_xpath("//span[contains(text(),'Add New Address')]")
add_new_address.click()

def shipping_info(user):
    shipping_first_name = driver.find_element_by_xpath("//div[@class='single-shipping address-card']/div/div/form/div[2]/div/fieldset[2]/div[1]/div[1]/div/input")
    input_keys(user["shipping"]["firstname"], shipping_first_name)

    shipping_last_name = driver.find_element_by_xpath("//div[@class='single-shipping address-card']/div/div/form/div[2]/div/fieldset[2]/div[1]/div[2]/div/input")
    input_keys(user["shipping"]["lastname"], shipping_last_name)

    shipping_address = driver.find_element_by_xpath("//div[@class='single-shipping address-card']/div/div/form/div[2]/div/fieldset[2]/div[2]/div[1]/div/input")
    input_keys(user["shipping"]["street"], shipping_address)

    #NOTE THERE IS NO EMAIL BLOCK FOR USERS WHO ARE SIGNED IN
    # input_email = driver.find_element_by_xpath("//input[contains(@id,'shipping-email')]")
    # input_keys(user["shipping"]["email"], input_email)

    shipping_state = Select(driver.find_element_by_xpath("//div[@class='single-shipping address-card']/div/div/form/div[2]/div/fieldset[2]/div[3]/div[2]/div/select"))
    shipping_state.select_by_value(user["shipping"]["state"])

    shipping_city = driver.find_element_by_xpath("//div[@class='single-shipping address-card']/div/div/form/div[2]/div/fieldset[2]/div[4]/div[1]/div/input")
    input_keys(user["shipping"]["city"], shipping_city)

    shipping_zip = driver.find_element_by_xpath("//div[@class='single-shipping address-card']/div/div/form/div[2]/div/fieldset[2]/div[4]/div[2]/div/input")
    input_keys(user["shipping"]["zipcode"], shipping_zip)

    shipping_phone = driver.find_element_by_xpath("//div[@class='single-shipping address-card']/div/div/form/div[2]/div/fieldset[2]/div[5]/div[1]/div/input")
    input_keys(user["shipping"]["phone"], shipping_phone)

shipping_info(user)

random_sleep()

##### CONTINUE TO PAYMENT #####
continue_to_payment_button = driver.find_element_by_xpath("//div[@class='card']/div[@class='next-step-summary-button']/button[1]")
continue_to_payment_button.send_keys(Keys.RETURN)

######! SHIPPING ADDRESS BECOMONES THE BILLING ADDRESS ON GAMESTOP API ######
random_sleep()

##### BILLING #####
##### THIS IS FOR ADDRESSES THAT HAVE NOT BEEN VERFIED BY THE SYSTEM ######
##### HAPPENS WITH NEW ADDRESSES
##### NOTE THIS ACTS AS A POPUP #####
try:
    use_original_address = driver.find_element_by_xpath("//button[contains(text(),'Use Original Address')]")
    use_original_address.send_keys(Keys.RETURN)
    random_sleep()
except WebDriverException as error:
    use_original_address.click()
    print(error)

####? BILLING ADDRESS ?####

if not same_billing_address:
    update_address_span = driver.find_element_by_xpath("//div[contains(@class,'shipping-address-options')]/span[@id='updateAddressbtn']")
    update_address_span.click()

    billing_first_name = driver.find_element_by_xpath("//div[@class='card payment-form']/div[2]/div/form/fieldset/div/fieldset/div/div[1]/div[1]/div/input")
    input_keys(user["billing"]["firstname"], billing_first_name)

    billing_last_name = driver.find_element_by_xpath("//div[@class='card payment-form']/div[2]/div/form/fieldset/div/fieldset/div/div[1]/div[2]/div/input")
    input_keys(user["billing"]["lastname"], billing_last_name)

    billing_street = driver.find_element_by_xpath("//div[@class='card payment-form']/div[2]/div/form/fieldset/div/fieldset/div/div[2]/div[1]/div/input")
    input_keys(user["billing"]["street"], billing_street)

    billing_state = Select(driver.find_element_by_xpath("//div[@class='card payment-form']/div[2]/div/form/fieldset/div/fieldset/div/div[4]/div[2]/div/select"))
    billing_state.select_by_value(user['billing']['state'])

    billing_city = driver.find_element_by_xpath("//div[@class='card payment-form']/div[2]/div/form/fieldset/div/fieldset/div/div[5]/div[1]/div/input")
    input_keys(user['billing']['city'], billing_city)

    billing_zip = driver.find_element_by_xpath("//div[@class='card payment-form']/div[2]/div/form/fieldset/div/fieldset/div/div[5]/div[2]/div/input")
    input_keys(user["billing"]["zipcode"], billing_zip)

    billing_email = driver.find_element_by_xpath("//div[@class='card payment-form']/div[2]/div/form/fieldset/div/fieldset/div/div[6]/div[1]/div/input")
    input_keys(user["billing"]["email"], billing_email)

    billing_phone = driver.find_element_by_xpath("//div[@class='card payment-form']/div[2]/div/form/fieldset/div/fieldset/div/div[6]/div[2]/div/input")
    input_keys(user["billing"]["phone"], billing_phone)


    random_sleep()

#####? PURCHASE INFO ?#####

purchase_credit_card = driver.find_element_by_xpath("//input[@id='cardNumber']")
input_keys(user["purchase"]["creditCard"], purchase_credit_card)

purchase_exp_month = Select(driver.find_element_by_xpath("//select[@id='expirationMonth']"))
purchase_exp_month.select_by_value(user["purchase"]["expMonth"])

purchase_exp_year = driver.find_element_by_xpath("//select[@id='expirationYear']")
purchase_exp_year.select_by_value(user["purchase"]["expYear"])

purchase_cvv = driver.find_element_by_xpath("//input[@id='securityCode']")
input_keys(user["purchase"]["cvv"], purchase_cvv)

random_sleep()


####! This step will cause an error unless the credit card info is correct !####
while True:
    try:
        continue_to_order_preview = driver.find_element_by_xpath("//div[@class='card-body order-total-summary']/div[@class='next-step-summary-button']/button[contains(@class,'submit-payment')]")
        continue_to_order_preview.send_keys(Keys.RETURN)
        print("Continue to order Review was RETURNED")
        break
    except WebDriverException:
        continue_to_order_preview.click()
        print("Continue to order Review was CLICKED")
        break

random_sleep()

try:
    use_original_address = driver.find_element_by_xpath("//*[contains(text(),'Use Original Address')]")
    use_original_address.send_keys(Keys.RETURN)
    print("Use original address was RETURNED")
except WebDriverException as error:
    use_original_address.click()
    print(error)
    print("Use original address was CLICKED")

while True:
    try:
        place_order_button = driver.find_element_by_xpath("//form[contains(@class,'place-order')]/button[contains(@class,'place-order')]")
        place_order_button.send_keys(Keys.RETURN)
    except WebDriverException:
        count += 1
        if count >= 5:
            break
