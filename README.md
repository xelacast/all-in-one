Automated All In One Bot
Purpose: To buy products that are being scalped by large scale bots

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

EDIT 05/31/22:
You can download this file and use it. It probably doesn't work and I am not going to update.

Git clone the repository

Make a python enviroment first
  python3 -m venv <DIR>

Then download the requirements
  python -m pip install requirements


EDIT 05/31/22: This project was never finished or maintained. This was my first major project as a self taught software developer. I created this with intuition and a few vidoes on youtube to learn how to use the software. I was already familiar with HTML, and CSS so crawling through the links on the websites were straight forward. The major problem I ran into was websites blocking my IP address and the headers I was using. To combat this I used a 3rd party service that allowed me to purchase proxies/IP addresses to make my self invisible to the website. I also made a pool of headers to change out.

Looking back I should have made many header and IP combos and chose from there. This would allow invisible consistency to stay hidden from the bot detectors on the websites. I am proud of this project becuase it was the first project I created on my own. Unfortunately I was not intuitive enough to create an automated system with it. I was not advanced enough to do this. If I was to create this again I would AWS servers with an express API that would listen for information from the Python Scrapy Bot. The bot would scrape data from each website with its determined IP/Headers every 5 mins during peak times of website restock. That data would be viewed depending on the status of the color, text, and clickableness of the button; when that criteria is met it would trigger the scalp bot to run and buy the product with the user entered data.
