import pandas as pd
import re
import os

#! users will come out of sqlite database
# * first intentions is to create my self as a user and then scale from there

# best buy data frame
# ps5s and rtx 30 series graphics cards
bbdf = pd.read_csv(
    "C:/Users/Alexander/Desktop/project_bots/BestBuyAIO/BestBuy/BestBuy/spiders/data/bestbuy.csv")
# gamestop dataframe
# ps5s only
gsdf = pd.read_csv(
    "C:/Users/Alexander/Desktop/project_bots/BestBuyAIO/BestBuy/BestBuy/spiders/data/gamestop.csv")
# newegg dataframe
# rtx 3080 graphics cards only
nwdf = pd.read_csv(
    "C:/Users/Alexander/Desktop/project_bots/BestBuyAIO/BestBuy/BestBuy/spiders/data/newegg.csv")
# walmart dataframe
# ps5s only
wmdf = pd.read_csv(
    "C:/Users/Alexander/Desktop/project_bots/BestBuyAIO/BestBuy/BestBuy/spiders/data/walmart.csv")

# merged dataframes of all websites

alldf = pd.concat([bbdf, wmdf, nwdf, gsdf])

# this is where I need to
product_brand = 'EVGA'
product = '3080 FTW3 ULTRA'
brand_df = alldf.loc[alldf.product_brand == product_brand]

#! search first by product brand then by title keywords
#! i think the best thing to do would a drop down menu with all product with search criteria
# * figure out how to get the exact product you want and exactly what you need to get that info
# * figure out when to delete these files because scrapy does not like files that are already created

# if product words in bbdf data pull that data
url = brand_df[brand_df.product_description.str.contains(
    product)].product_url.iloc[0]
product_site = brand_df[brand_df.product_url == url].product_site.iloc[0]
product_status = brand_df[brand_df.product_url ==
                          url].product_status.iloc[0].lower()
#! chooses which bot it is based on the product_site on the row of url

# * this works!
# ? how can I get it to work with product Sites?
# if product_status in ['see details', 'add to cart']:
# activate bot based on the website
# just like this psuedo code
# if product_site == 'bestbuy':
#     scalpBot = BestBuy(info here)
#     scalpBot.start()
# elif product_site == 'gamestop':
#     scalpBot = GameStop(info here)
#     scalpBot.start()
# elif product_site == 'newegg':
#     scalpBot = Newegg(info here)
#     scalpBot.start()
# else:
#     scalpBot = Walmart(info here)
#     scalpBot.start()

# bot activations
# testBot = BestBuy(BEST_BUY_USER, url)
# testBot.start()


class Activator(object):
    def __init__(self, user):
        self.user = user
    # best buy data frame
    # ps5s and rtx 30 series graphics cards
    bbdf = pd.read_csv(
        "C:/Users/Alexander/Desktop/project_bots/BestBuyAIO/BestBuy/BestBuy/spiders/data/bestbuy.csv")
    # gamestop dataframe
    # ps5s only
    gsdf = pd.read_csv(
        "C:/Users/Alexander/Desktop/project_bots/BestBuyAIO/BestBuy/BestBuy/spiders/data/gamestop.csv")
    # newegg dataframe
    # rtx 3080 graphics cards only
    nwdf = pd.read_csv(
        "C:/Users/Alexander/Desktop/project_bots/BestBuyAIO/BestBuy/BestBuy/spiders/data/newegg.csv")
    # walmart dataframe
    # ps5s only
    wmdf = pd.read_csv(
        "C:/Users/Alexander/Desktop/project_bots/BestBuyAIO/BestBuy/BestBuy/spiders/data/walmart.csv")

    # merged dataframes of all websites
    alldf = pd.concat([bbdf, wmdf, nwdf, gsdf])
    #! recreate filtering method

    def filter(self, target_prod):
        targ_list = target_prod.split(" ")
        break_down_df = self.alldf.reset_index()
        for word in targ_list:
            break_down_df = break_down_df[break_down_df.product_description.str.contains(
                word)]
        if len(break_down_df) == 1:
            product_site = break_down_df.product_site.iloc[0]
            product_url = break_down_df.product_url.iloc[0]
            product_status = break_down_df.product_status.iloc[0].lower()
            print('filtered')
            if product_status in ['add to cart', 'see details']:
                self.activate(product_site, product_url)

    def activate(self, product_site, product_url):

        if product_site == 'bestbuy':
            print(product_site)
        elif product_site == 'newegg':
            print(product_site)
        elif product_site == 'walmart':
            print(product_site)
        elif product_site == 'gamestop':
            print(product_site)
        elif product_site == 'amazon':
            print(product_site)
        elif product_site == 'target':
            print(product_site)
        elif product_site == 'b&h':
            print(product_site)
        else:
            print("That product site is not in the database")
            print(product_site)
            quit()

    def print_df(self):
        print(self.alldf)
        return self.alldf

# Activator.filter('target_prod')
# y = Activator('Hello')
# y.filter('ASUS 3080 TUF')
