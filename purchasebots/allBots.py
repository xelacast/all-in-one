from selenium import webdriver
from parts.botparts import selectable, clickable, randomSleep, formFiller, clickableWait, textInput
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from parts.users import BESTBUY_USER
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

import time
import random
import asyncio


def getUserAgent():
    userDict = {
        1: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        2: 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        3: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        4: 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        5: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        7: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        8: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        9: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    }

    agent = random.randint(1, 9)
    return userDict[agent]


def getWindowSize():
    rezDict = {
        1: '1536,749',
        2: '1366,768',
        3: '1440,900',
        4: '1536,864',
        5: '1280,800',

    }
    size = random.randint(1, 5)
    return rezDict[size]


class BestBuy(object):
    def __init__(self):
        self.userAgent = ''
        self.windowSize = ''
        self.driver = ''
        self.store = 'https://www.bestbuy.com/'
        self.google = 'https://www.google.com/'

    def setHeader(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_argument(
            '--disable-blink-features=AutomationControlled')
        self.option.add_argument(f"window-size={self.windowSize}")
        self.option.add_argument(f"user-agent={self.userAgent}")
        self.option.add_argument('--ignore-certificate-errors')
        self.option.add_argument('--ignore-ssl-errors')
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.option.add_experimental_option("prefs", prefs)
        self.option.add_experimental_option(
            'excludeSwitches', ['enable-logging'])

    def start(self):
        self.userAgent = getUserAgent()
        self.windowSize = getWindowSize()
        self.setHeader()
        self.driver = webdriver.Chrome(
            executable_path='chromedriver.exe', options=self.option)

        # Remove navigator.webdriver Flag using JavaScript
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        # opens local host to keep driver open
        # self.driver.get('http://127.0.0.1:5500/purchasebots/index.html')

        # self.driver.get(self.google)
        # print('Opened Google')
        # randomSleep('test')
        # self.driver.get(self.store)
        # print('Went to BestBuy')

# i want to create a refresh process where itll refresh a local
# host to be 'active' and then refresh the bestbuy store every so
# often to see if I am still signed in

    def login(self, username, password):
        # email address field
        textInput(
            '//*[@id="fld-e"]', username, self.driver)
        print('Text input email')
        # password
        textInput('//*[@id="fld-p1"]', password, self.driver)
        print('Text input password')

        # MainSignInButton
        clickable(
            "//div[@class='cia-settings-container']/div/div/form/div[3]/button", self.driver)
        print('Logged in')

    def getItem(self, user, product_url):
        # get request to product url
        self.driver.get(product_url)
        time.sleep(15)
        # add to cart button
        add_to_cart_xpath = "//button[contains(@class,'btn-lg btn-block btn-leading-ficon add-to-cart-button')]"
        clickable(
            add_to_cart_xpath, self.driver)
        # //\*[contains(@id,"fulfillment-add-to-cart-button")]/div/div/div/button
        # //\*[contains(@class,"fulfillment-add-to-cart-button")]/div/div/button[contains(@class,'btn-primary')]
        # //div[@class='v-m-top-m v-p-top-m v-border v-border-top']/div[contains(@id,'fulfillment-add-to-cart')]/div/div/div/button
        #! Active product add to cart button //button[contains(@class,'btn-lg btn-block btn-leading-ficon add-to-cart-button')]

        # go to cart
        self.driver.get('https://www.bestbuy.com/cart')
        # randomSleep('test')
        # choose shipping option
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
        # clicks on checkout
        while True:
            try:
                checkout = self.driver.find_element_by_xpath(
                    "//div[@class='checkout-buttons']/div[1]/button")
                checkout.click()
                break
            except WebDriverException:
                break

        # login to bestbuy here after hitting checkout
        self.login(user['login']['email'], user['login']['password'])
        randomSleep('test')

        # since im logged in I only have to input the cvv
        textInput('//*[@id="credit-card-cvv"]',
                  user['purchase']['cvv'], self.driver)

        # place order
        # clickable(
        #     '//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[2]/div/div[4]/div[3]/div/button', self.driver)
        #! checkout fails on two attemps
        count = 0
        while True:
            try:
                complete_order = self.driver.find_element_by_xpath(
                    "//button[contains(@class,'button__fast-track')]")
                complete_order.click()
                break
            except (WebDriverException, NoSuchElementException):
                count += 1
                if count >= 2:
                    print('Made it through!!')
                    exit()


# from allBots import BestBuy
# from parts.users import BESTBUY_USER as user

# url = 'https://www.bestbuy.com/site/lg-24-ips-led-fhd-freesync-monitor-hdmi-vga-black/6362423.p?skuId=6362423'
# bot1 = BestBuy()
# bot1.start()
# bot1.getLocal()
