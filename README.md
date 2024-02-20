# HCMUS-News Scraper: a web scraper that crawl news from my university websites
## Inspired from this [github repo](https://github.com/huytrinhm/hcmus-news-crawler)
## How to use:

### Clone the repo, activate the virtual environment and install necessary requirements
```
git clone https://github.com/linhnph05/HCMUS-Scraper.git
python3 -m venv venv
```

### If you are on Windows:
```
.\venv\Scripts\activate
```

### If you are on Mac:
```
source venv/bin/activate
```

### Then install necessary package
```
pip3 install -r requirements.txt
```

### Then go to main directory and this line to create a json file from 1/12/2023 to 2024
```
cd hcmusscraper
scrapy crawl hcmusSpider -O output.json
```

### Websites list that I scraping from:
* https://www.ctda.hcmus.edu.vn/
* https://www.fit.hcmus.edu.vn/vn/
* https://hcmus.edu.vn/

### Technology: Scrapy

### What I have learned: 
Scaping STATIC content with following next page link
