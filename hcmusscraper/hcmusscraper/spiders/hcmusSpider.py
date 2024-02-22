import scrapy

from datetime import datetime

import re

def cleanString(s):
    cleanedString = s.strip()
    cleanedString = re.sub(r'[\r\n\t]', ' ', cleanedString)
    cleanedString = re.sub(' +', ' ', cleanedString)
    cleanedString = cleanedString.replace('\"', '\'')
    return cleanedString
class HcmusspiderSpider(scrapy.Spider):
    name = "hcmusSpider"

    start_urls = [
        'https://www.ctda.hcmus.edu.vn/vi/thong-bao/',
        'https://www.ctda.hcmus.edu.vn/vi/tin-tuc/',
        'https://www.ctda.hcmus.edu.vn/vi/goc-sinh-vien/thong-tin-can-biet/',
        'https://www.ctda.hcmus.edu.vn/vi/goc-sinh-vien/hoat-dong-sinh-vien/',
        'https://www.fit.hcmus.edu.vn/vn/Default.aspx?tabid=36',
        'https://hcmus.edu.vn/thong-tin-danh-cho-nguoi-hoc/',
        'https://hcmus.edu.vn/category/dao-tao/dai-hoc/thong-tin-danh-cho-sinh-vien/',
        'https://hcmus.edu.vn/category/tuyen-dung-viec-lam/',
        'https://hcmus.edu.vn/category/nguoi-hoc/',
        'https://hcmus.edu.vn/category/dao-tao/dai-hoc/hoc-bong-dai-hoc/',
    ]

    resultJson = {
        "Update time": datetime.now().strftime("%H:%M:%S %d/%m/%Y"),
        "Thong Bao": [],
        "Tin tuc": [],
        "Thong tin can biet": [],
        "Hoat dong sinh vien": [],
        "FIT-Tin tuc": [],
        "FIT-Thong tin hoc bong": [],
        "FIT-Thong tin tuyen dung": [],
        "FIT-Hoi thao/Hoi Nghi": [],
        "FIT-Hoat dong sinh vien": [],
        "FIT-Thong bao chung": [],
        "HCMUS-Thong tin nguoi hoc": [],
        "HCMUS-Thong tin sinh vien": [],
        "HCMUS-Tuyen dung": [],
        "HCMUS-Nguoi hoc": [],
        "HCMUS-Hoc bong dai hoc": [],
    }

    count = 0
    def parse(self, response):

        if 'https://www.ctda.hcmus.edu.vn/vi/thong-bao/' in response.url:
            yield from self.parsePage(response, "Thong Bao")
        elif 'https://www.ctda.hcmus.edu.vn/vi/tin-tuc/' in response.url:
            yield from self.parsePage(response, "Tin tuc")
        elif 'https://www.ctda.hcmus.edu.vn/vi/goc-sinh-vien/thong-tin-can-biet/' in response.url:
            yield from self.parsePage(response, "Thong tin can biet")
        elif 'https://www.ctda.hcmus.edu.vn/vi/goc-sinh-vien/hoat-dong-sinh-vien/' in response.url:
            yield from self.parsePage(response, "Hoat dong sinh vien")
        elif 'https://www.fit.hcmus.edu.vn/vn/Default.aspx?tabid=36' in response.url:
            self.parseFIT(response)
        elif 'https://hcmus.edu.vn/thong-tin-danh-cho-nguoi-hoc/' in response.url:
            yield from self.parseHCMUS1(response, "HCMUS-Thong tin nguoi hoc")
        elif 'https://hcmus.edu.vn/category/dao-tao/dai-hoc/thong-tin-danh-cho-sinh-vien/' in response.url:
            yield from self.parseHCMUS2(response, "HCMUS-Thong tin sinh vien")
        elif 'https://hcmus.edu.vn/category/tuyen-dung-viec-lam/' in response.url:
            yield from self.parseHCMUS2(response, "HCMUS-Tuyen dung")
        elif 'https://hcmus.edu.vn/category/nguoi-hoc/' in response.url:
            yield from self.parseHCMUS2(response, "HCMUS-Nguoi hoc")
        elif 'https://hcmus.edu.vn/category/dao-tao/dai-hoc/hoc-bong-dai-hoc/' in response.url:
            yield from self.parseHCMUS2(response, "HCMUS-Hoc bong dai hoc")
        else:
            self.log(f"Unhandled URL: {response.url}")

    def parsePage(self, response, page):
        posts = response.css('div.post-desc')
        for post in posts:
            title = post.css('.post-title')
            date = post.css('.post-date::text').get()
            year = datetime.strptime(date, "%d/%m/%Y").year
            month = datetime.strptime(date, "%d/%m/%Y").month
            day = datetime.strptime(date, "%d/%m/%Y").day
            if ((datetime.now() - datetime(year, month, day)).days <= 30):
                item = {
                    "tieuDe": title.css('a::text').get(),
                    "url": title.css('a::attr(href)').get(),
                    "date": date
                }
                self.resultJson[page].append(item)

        buttonURL = response.css('.pager_load_more::attr(href)').get()
        if buttonURL is not None:
            yield scrapy.Request(buttonURL, callback=self.parsePage, cb_kwargs={'page': page}, dont_filter=True)


    def parseFIT(self, response):
        posts = response.css('#dnn_ctr989_ModuleContent > table')
        for post in posts:
            first = post.css('tr:first-child')
            last = post.css('tr:last-child')

            notClean = first.css('.post_title a::text').get()
            day = first.css('.day_month::text').get()
            month = last.css('.day_month::text').get()
            year = first.css('.post_year::text').get()
            title = cleanString(notClean)
            date = cleanString(day) + '/' + cleanString(month) + '/' + cleanString(year)

            year = datetime.strptime(date, "%d/%m/%Y").year
            month = datetime.strptime(date, "%d/%m/%Y").month
            day = datetime.strptime(date, "%d/%m/%Y").day
            if((datetime.now() - datetime(year, month, day)).days <= 30):
                item = {
                    "tieuDe": title,
                    "url": 'https://www.fit.hcmus.edu.vn/vn/' + first.css('.post_title a::attr(href)').get(),
                    "date": date,
                }
                self.resultJson["FIT-Tin tuc"].append(item)

    def parseHCMUS1(self, response, page):
        posts = response.css('.cmsmasters_post_cont_wrap')
        for post in posts:
            title = cleanString(post.css('.cmsmasters_post_title.entry-title > a::text').get())
            url = post.css('.cmsmasters_post_title.entry-title > a::attr(href)').get()
            date = post.css('.published::text').get()

            year = datetime.strptime(date, "%d/%m/%Y").year
            month = datetime.strptime(date, "%d/%m/%Y").month
            day = datetime.strptime(date, "%d/%m/%Y").day

            if ((datetime.now() - datetime(year, month, day)).days <= 30):
                item = {
                    "tieuDe": title,
                    "url": url,
                    "date": date,
                }
                self.resultJson[page].append(item)

        buttonURL = response.css('.next.page-numbers::attr(href)').get()
        if buttonURL is not None:
            yield scrapy.Request(buttonURL, callback=self.parseHCMUS1, cb_kwargs={'page': page}, dont_filter=True)

    def parseHCMUS2(self, response, page):
        posts = response.css('.cmsmasters_archive_item_cont_wrap')
        for post in posts:
            title = cleanString(post.css('.cmsmasters_archive_item_title.entry-title >a::text').get())

            url = post.css('.cmsmasters_archive_item_title.entry-title >a::attr(href)').get()
            date = post.css('.published::text').get()

            year = datetime.strptime(date, "%d/%m/%Y").year
            month = datetime.strptime(date, "%d/%m/%Y").month
            day = datetime.strptime(date, "%d/%m/%Y").day

            if ((datetime.now() - datetime(year, month, day)).days <= 30):
                item = {
                    "tieuDe": title,
                    "url": url,
                    "date": date,
                }
                self.resultJson[page].append(item)

        buttonURL = response.css('.next.page-numbers::attr(href)').get()
        if buttonURL is not None:
            yield scrapy.Request(buttonURL, callback=self.parseHCMUS2, cb_kwargs={'page': page}, dont_filter=True)
        else:
            if page == "HCMUS-Hoc bong dai hoc":
                yield self.resultJson
