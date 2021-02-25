Automated All In One Bot
Purpose: purchase the goods we need and to say fuck you to resellers

Running? No
In development:
Purchase Bots with puppeteer
Activator adjustments
Sqlite database for our own custom user information for each website

Components:
Product Crawler:
This is the scrapy webscraper that targets product data and creates
multiple csv files to later parse

Activator:
The activator builds a pandas database out of the csv files that were
created by the ProductCrawler and parses the data to view products that
come into stock
When a targeted product restocks it will imediately activate a purchase bot
to buy the product

Purchase Bots:
These are the bots to purchase our targeted products

Targeted Websites:
As of February 25th, 2021 we are targeting the following websites:
Walmart:
PS5 Console
PS5 Digital Console

BestBuy
PS5 Console
PS5 Digital Console
RTX 30 series Cards

Newegg
PS5 Console
PS5 Digital Console
RTX 30 series Cards

GameStop
PS5 Console
PS5 Digital Console
