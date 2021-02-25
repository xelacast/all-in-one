from selenium import webdriver
from parts.botparts import selectable, clickable, randomSleep, formFiller, clickableWait
from selenium.common.exceptions import WebDriverException
from parts.users import BEST_BUY_USER

import time
import random

#! HUGE SPEED PROBLEM.
# NOTE My response times on the Proxies I have are horrendouse
# NOTE I must find a way to inmprove my resonse time to achieve the highest turnover

#! REMOVE ALL RANDOM SLEEPS FOR PRODUCTION PRODUCT

# create random pool of headers for this bot
# need random fast response time proxy pool for the bot


class BestBuy(object):

    def __init__(self, user, target_url, target_product=None, billing=True):
        # proxy and user agent will be set internally by a random pool of
        # proxies and user agents
        self.proxy = self.proxyPool()
        self.useragent = self.userAgentPool()

        self.driver = ''
        self.product_url = target_url
        self.target_product = target_product
        self.store = 'https://www.bestbuy.com/'
        self.google = 'https://www.google.com/'
        self.billing = billing
        self.setHeader()

        self.shipping_list = [
            ("//input[contains(@id,'firstName')]",
             user['shipping']['firstname'], 'input'),
            ("//input[contains(@id,'lastName')]",
             user['shipping']['lastname'], 'input'),
            ("//input[contains(@id,'street')]",
             user['shipping']['street'], 'input'),
            ("//input[contains(@id,'city')]",
             user['shipping']['city'], 'input'),
            ("//select[contains(@id,'state')]",
             user['shipping']['state'], 'select'),
            ("//input[contains(@id,'zipcode')]",
             user['shipping']['zipcode'], 'input'),
            ("//input[contains(@id,'emailAddress')]",
             user['shipping']['email'], 'input'),
            ("//input[contains(@id,'phone')]",
             user['shipping']['phone'], 'input'),
        ]

        self.payment_list = [
            ("//input[@id='optimized-cc-card-number']",
             user['purchase']['creditCard'], 'input'),
            ("//select[@name='expiration-month']",
             user['purchase']['expMonth'], 'select'),
            ("//select[@name='expiration-year']",
             user['purchase']['expYear'], 'select'),
            ("//input[contains(@id,'cvv')]",
             user['purchase']['cvv'], 'input')
        ]

        self.billing_list = [
            ("//input[contains(@id,'billingAddress.firstName')]",
             user['billing']['firstname'], 'input'),
            ("//input[contains(@id,'billingAddress.lastName')]",
             user['billing']['lastname'], 'input'),
            ("//input[contains(@id,'billingAddress.street')]",
             user['billing']['street'], 'input'),
            ("//input[contains(@id,'billingAddress.city')]",
             user['billing']['city'], 'input'),
            ("//select[contains(@id,'billingAddress.state')]",
             user['billing']['state'], 'select'),
            ("//input[contains(@id,'billingAddress.zipcode')]",
             user['billing']['zipcode'], 'input'),
        ]

    def userAgentPool(self):
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

    def proxyPool(self):
        return ''

    def setHeader(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_argument(
            '--disable-blink-features=AutomationControlled')
        self.option.add_argument("window-size=1280,800")
        self.option.add_argument(f"user-agent={self.useragent}")
        self.option.add_argument(f"proxy-server={self.proxy}")
        self.option.add_argument('--ignore-certificate-errors')
        self.option.add_argument('--ignore-ssl-errors')
        # cacheing
        # self.driver = webdriver.Chrome(
        #     executable_path='C:/Users/Alexander/Desktop/project_bots/BestBuyAIO/botdrivers/chromedriver.exe', options=self.option)

        # # Remove navigator.webdriver Flag using JavaScript
        # self.driver.execute_script(
        #     "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def start(self):
        # driver initialization
        self.driver = webdriver.Chrome(
            executable_path='C:/Users/Alexander/Desktop/project_bots/BestBuyAIO/botdrivers/chromedriver.exe', options=self.option)

        # Remove navigator.webdriver Flag using JavaScript
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        # skip
        self.driver.get(self.google)
        randomSleep('test')
        self.driver.get(self.store)
        randomSleep('test')
        self.driver.get(self.product_url)
        randomSleep('test')
        # add to cart button
        clickable(
            "//div[@class='fulfillment-add-to-cart-button']/div/div/button[contains(@class,'btn-primary')]", self.driver)
        randomSleep('test')
        # go to cart
        self.driver.get('https://www.bestbuy.com/cart')
        randomSleep('test')

        # click shipping in cart
        # API of shopping cart changes periodically between these two clicks
        while True:
            try:
                button = self.driver.find_element_by_xpath(
                    "//input[contains(@id,'fulfillment-shipping')]")
                button.click()
                break
            except WebDriverException:
                try:
                    button = self.driver.find_element_by_xpath(
                        "//input[@id='fulfillment-order-shipping']")
                    button.click()
                    break
                except WebDriverException:
                    pass

        randomSleep('test')

        #! Skips a get request so itll be faster to checkout
        # random selecion of making a url get request and clicking through
        rand_selection = random.randint(0, 1)
        if rand_selection == 0:
            self.driver.get("https://www.bestbuy.com/checkout/r/fulfillment")
            randomSleep('test')
        else:
            # checkout button click
            while True:
                try:
                    checkout = self.driver.find_element_by_xpath(
                        "//div[@class='checkout-buttons']/div[1]/button")
                    checkout.click()
                except WebDriverException:
                    pass  # this will be the other instance of the checkout button location
                    # checkout = self.driver.find_element_by_xpath("")
                    # checkout.click()

            randomSleep('test')
            clickable(
                "//div[@class='cia-guest-content']/div[2]/button", self.driver)

        # fills out shipping and contact info
        formFiller(self.shipping_list, self.driver)
        randomSleep('test')

        # Save this as my billing address is set to True on reg
        if not self.billing:
            clickable(
                "//input[contains(@id,'save-for-billing-address')]", self.driver)

        # click text updates box
        # clickable("//input[@id='text-updates']", self.driver)

        # click continue to payment info
        clickable("//div[@class='button--continue']/button", self.driver)

        # this sequence might or might not happen
        # sometimes your shipping choices are changed and need to reverify
        clickableWait("//div[@class='button--continue']/button", self.driver)
        # fill in purchase and billing info
        #### going to fast to fill out items ####
        formFiller(self.payment_list, self.driver)
        if not self.billing:
            formFiller(self.billing_list, self.driver)

        # place order
        clickable(
            "//div[@class='button--place-order']/button", self.driver)


# need a pool 5-6 random user agents
# need random proxies
# user = BEST_BUY_USER
# # proxy = '216.41.234.25'
# # useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
# target_url = 'https://www.bestbuy.com/site/sony-playstation-5-dualsense-wireless-controller/6430163.p?skuId=6430163'
# # target_product = 'ps5 controller'
# # BestBuy(user, target_url, target_product=None, billing=True)

# bot1 = BestBuy(user, target_url)
# # bot1.setHeader()
# bot1.start()
