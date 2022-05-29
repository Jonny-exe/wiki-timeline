# Wikipedia timeline
This is a webpage where you can find every [Wikipedia](https://wikipedia.org) article
dated between two dates.

*You can't find every article, only the ones I was able to scrape.*

You can check it out at [jonny.sytes.net/wikipedia](https://jonny.sytes.net/wikipedia)

## How it works
This works by scraping all the possible wikipedia articles and getting their dates. After that, everything else is storing it on a database and looking it up.
The scraping is done by [scraper.py](/app/management/commands/scraper.py).

## Self host
In order to host this webpage yourself: 
 1. Clone this repository: `git clone https://github.com/Jonny-exe/wiki-timeline`
 2. Install all requirements: `pip install -r requirements.txt`
 3. Run the website with: `python3 manage.py runserver 8080`
 4. You will see the website on: [127.0.0.1](http://127.0.0.1)

If you want to use pre-scraped articles, download the sqlite database, in the releases, and move it to the root directory.

## Screenshots
![Screenshot1](screenshots/search.png?raw=true)
![Screenshot1](screenshots/info.png?raw=true)

## Built with
 * Database: sqlite
 * Language: python
 * Web-framework: django


If you are interested in improving or modifying anything, PR's are welcome.