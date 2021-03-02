from selenium import webdriver
from parts.botparts import selectable, clickable, randomSleep, formFiller, clickableWait
from selenium.common.exceptions import WebDriverException
from parts.users import WALMART_USER

import time
import random


#! REMOVE ALL RANDOM SLEEPS FOR PRODUCTION PRODUCT
class Walmart(object):

    def __init__(self, user, proxy, useragent, target_url, target_product, billing=True):
        self.proxy = proxy
        self.useragent = useragent
        self.driver = ''
        self.product_url = target_url
        self.target_product = target_product
        self.store = 'https://www.walmart.com/'
        self.store_cart = 'https://www.walmart.com/cart'
        self.google = 'https://www.google.com/'
        self.billing = billing

        self.shipping_list = [
            ("//input[@name='firstName']",
             user['shipping']['firstname'], 'input'),
            ("//input[@name='lastName']",
             user['shipping']['lastname'], 'input'),
            ("//input[@name='phone']",
             user['shipping']['phone'], 'input'),
            ("//input[@name='email']",
             user['shipping']['email'], 'input'),
            ("//input[@name='addressLineOne']",
             user['shipping']['street'], 'input'),
            ("//input[@name='city']",
             user['shipping']['city'], 'input'),
            ("//select[@name='state']",
             user['shipping']['state'], 'select'),
            ("//input[@name='postalCode']",
             user['shipping']['zipcode'], 'input'),
        ]
        self.payment_list = [
            ("//input[@name='creditCard']",
             user['purchase']['creditCard'], 'input'),
            ("//select[@name='month-chooser']",
             user['purchase']['expMonth'], 'select'),
            ("//select[@name='year-chooser']",
             user['purchase']['expYear'], 'select'),
            ("//input[@name='cvv']",
             user['billing']['street'], 'input'),
        ]
        self.billing_list = [
            ("//input[@name='firstName']",
             user['billing']['firstname'], 'input'),
            ("//input[@name='lastName']",
             user['billing']['lastname'], 'input'),
            ("//input[@name='addressLineOne']",
             user['billing']['street'], 'input'),
            ("//input[@name='city']",
             user['billing']['city'], 'input'),
            ("//select[@name='state']",
             user['billing']['state'], 'select'),
            ("//input[@name='postalCode']",
             user['billing']['zipcode'], 'input'),
        ]

    def setHeader(self):
        option = webdriver.ChromeOptions()
        option.add_argument('--disable-blink-features=AutomationControlled')
        option.add_argument("window-size=1280,800")
        option.add_argument('--ignore-certificate-errors')
        option.add_argument('--ignore-ssl-errors')
        option.add_argument(f"user-agent={self.useragent}")
        option.add_argument(f"proxy-server={self.proxy}")
        # cacheing
        self.driver = webdriver.Chrome(
            executable_path='purchase_bots/botdrivers/chromedriver.exe', options=option)

        # Remove navigator.webdriver Flag using JavaScript
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def crawl(self):

        self.driver.get(self.google)
        randomSleep('test')
        self.driver.get(self.store)
        randomSleep('test')
        self.driver.get(self.product_url)
        randomSleep('test')

        # add to cart button
        clickable(
            "//div[contains(@class, 'add-to-cart')]/button[contains(@class,'button--primary')]", self.driver)
        randomSleep('test')
        # go to cart
        self.driver.get(self.store_cart)
        randomSleep('test')
        # click checkout
        clickable(
            "//div[contains(@class,'cart-pos-checkout-button')]/div/div/button[contains(@class,'checkoutBtn')]", self.driver)
        randomSleep('test')
        # continue as guest
        clickable(
            "//section[@class='WelcomeMat-secondary']/section/div/button", self.driver)
        randomSleep('test')
        # 1. delivery and pickup options continue button
        clickable(
            "//div[@class='CXO_fulfillment_continue']/button", self.driver)
        randomSleep('test')
        # fill out shipping form
        formFiller(self.shipping_list, self.driver)
        # unclick email sign up
        clickable("//input[@name='marketingEmailPref']", self.driver)
        randomSleep('test')
        # continue from shipping form
        clickable(
            "//div[@class='arrange']/div[contains(@class,'fill')]/button", self.driver)
        # continue_with_this_address popup click
        # popup occurs with my Arizona Address
        clickableWait(
            "//div[@class='address-validation-buttons']/button", self.driver)
        randomSleep('test')
        print('first clickablewait')
        # changing shipping adress will change the delivery options
        # NOTE goes back to the 1. delivery and pickup options continue button
        clickableWait(
            "//div[@class='CXO_fulfillment_continue']/button", self.driver)
        print('second clickablewait')

        randomSleep('test')
        # fill out purchase form and billing form if needed
        # NOTE self.billing is type boolean
        if self.billing:
            formFiller(self.payment_list, self.driver)
        else:
            # activates different billing address
            clickable(
                "//div[@class='checkout-credit-card-address-form-same-as']/div/div/label/input", self.driver)
            formFiller(self.billing_list, self.driver)
        randomSleep('test')
        # review order button
        clickable("//div[@class='edit-form-actions']/div/button", self.driver)
        randomSleep('test')
        # place order
        clickable(
            "//div[1]/div/div[1]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/form/div/button", self.driver)
        print(f"Your {self.target_product} has been purchased")


user = WALMART_USER
proxy = '104.168.2.142'
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
target_url = 'https://www.walmart.com/ip/Sharpie-Permanent-Markers-Fine-Point-Black-5-Count/14922696'
target_product = 'sharpies'
billing = True


bot1 = Walmart(user, proxy, useragent, target_url, target_product, billing)
bot1.setHeader()
bot1.crawl()
