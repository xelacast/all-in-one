# Automated All In One Bot
## Purpose: To buy products that are being scalped by large scale bots
My intentions were to buy myself a RTX 3080 Graphics card so I could build my own PC. This was back in 2020 when RTX cards were selling for 2 to 3 times market value and I wasn't going to give into it. Unfortunately, I was never successful in getting the right time increments to watch for the restock of the product on the websites; and I couldn't get past the intial bot security wall even with proxies. Bestbuy's website API would change here and then. I dont think the crawlers would be able to get to the HTML classes and tags for it to crawl through. 

EDIT: Aug 4th, 2022
## The process I wanted the bots to take is 
1) Crawl the websites at specified times and collect Information on stock(this would be if the button was clickable or depending on the website)
This would use smart proxies and unique headers for each proxy. This would change on every session of activtions

2) Check the information and see if its able to be purchased. If its able to be purchased activate specific bot for that website and specific user information to fill out.

3) Send notification back when the item was purchased

4) Rinse and repeate

## Fallbacks and Drawbacks:
1 ) websites logged ips/headers/user activity to watch for bots. This was hard to get past but I figured out a way. Although is was inefficient.

2 ) The "database" and schema I was using overwrote data so I never could tell when the items were being restocked to get a good time on when to activate the bots. If I kept the webcrawlers active every 5-10 seconds they would run too much for the bot detection, become flagged, and be blocked from entering the website.

3 ) My knowledge of data intensive application at the time was None. I had no experience in creating a product so It was rough. Comments everywhere not good code. 

Bonus ) If I was to do it differently I would use a differnt proxy type, a headleass browser, better proxy and header configurations and dive deeper into it. AWS for automation so I don't have to keep my computer running a script 24/7. AWS for a database to keep track records of when items were restocked to make my best predictions for future restocks. I would need a form of AI or Machine learning to scrape the websites at variable times, mouse motion, speed, and to find the appropriate data to route to the product wanting to be purchased. The routes of the bots would all have to be different too.

Running? No
In development:
Purchase Bots with puppeteer
Activator adjustments
Sqlite database for our own custom user information for each website

## Components:
### Product Crawler:
This is the scrapy webscraper that targets product data and creates
multiple csv files to later parse

### Activator:
The activator builds a pandas database out of the csv files that were
created by the ProductCrawler and parses the data to view products that
come into stock
When a targeted product restocks it will imediately activate a purchase bot
to buy the product

### Purchase Bots:
These are the bots to purchase our targeted products

### Targeted Websites:
As of February 25th, 2021 we are targeting the following websites:
Walmart:
PS5 Console
PS5 Digital Console

#### BestBuy
PS5 Console
PS5 Digital Console
RTX 30 series Cards

#### Newegg
PS5 Console
PS5 Digital Console
RTX 30 series Cards

#### GameStop
PS5 Console
PS5 Digital Console

EDIT May 31st, 2022:

You can download this file and use it. It probably doesn't work and I am not going to update.

Git clone the repository into the repository/directory of your choice.

Make a python enviroment first __
 `
 python3 -m venv <DIR> 
 `__
Then download the requirements __
 
 ` 
 python -m pip install requirements
 `__
 `
 cd <dir>
 `__
Run
 `
 python activator.py
 `__

This project was never finished or maintained. This was my first major project as a self taught software developer. I created this with intuition and a few vidoes on youtube to learn how to use the software. I was already familiar with HTML, and CSS so crawling through the links on the websites were straight forward. The major problem I ran into was websites blocking my IP address and the headers I was using. To combat this I used a 3rd party service that allowed me to purchase proxies/IP addresses to make my self invisible to the website. I also made a pool of headers to change out.

Looking back I should have made many header and IP combos and chose from there. This would allow invisible consistency to stay hidden from the bot detectors on the websites. I am proud of this project becuase it was the first project I created on my own. Unfortunately I was not intuitive enough to create an automated system with it. I was not advanced enough to do this. If I was to create this again I would AWS servers with an express API that would listen for information from the Python Scrapy Bot. The bot would scrape data from each website with its determined IP/Headers every 5 mins during peak times of website restock. That data would be viewed depending on the status of the color, text, and clickableness of the button; when that criteria is met it would trigger the scalp bot to run and buy the product with the user entered data.
