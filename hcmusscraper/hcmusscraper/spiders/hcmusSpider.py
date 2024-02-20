import scrapy
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from datetime import datetime

from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
# class HcmusspiderSpider(scrapy.Spider):
#     name = "hcmusSpider"
#     #scrapy crawl hcmusSpider -O output.json
#
#     def start_requests(self):
#         url = 'https://www.ctda.hcmus.edu.vn/vi/'
#         yield scrapy.Request(url, callback=self.parse)
#
#     def extract_category_data(self, category):
#         category_data =[
#             {
#                 "tieuDe": title,
#                 "url": url,
#                 "date": date
#             }
#             for title, url, date in zip(
#                 category.css('a::text').getall(),
#                 category.css('a::attr(href)').getall(),
#                 category.css('.date::text').getall()
#             )
#             if datetime.strptime(date, "%d/%m/%Y").year >= 2023
#         ]
#
#         category_data.sort(key=lambda x: datetime.strptime(x['date'], "%d/%m/%Y"),
#                            reverse=True)
#
#         return category_data
#
#     def parse(self, response):
#         thongBao = response.css('div.items_group')[1]
#         yield {
#             "Update time": datetime.now().strftime("%H:%M:%S %d/%m/%Y"),
#             "keHoachHocTap": self.extract_category_data(thongBao.css('ul')[1]),
#             "giaoVu": self.extract_category_data(thongBao.css('ul')[2]),
#             "troLySinhVien": self.extract_category_data(thongBao.css('ul')[3]),
#             "taiChinh": self.extract_category_data(thongBao.css('ul')[4]),
#         }
#
#         # yield {
#         #     "Update time": datetime.now().strftime("%H:%M:%S %d/%m/%Y"),
#         #     "keHoachHocTap": [
#         #         {
#         #             "tieuDe": title,
#         #             "url": url,
#         #             "date": date
#         #         }
#         #         for title, url, date in zip(keHoachHocTap.css('a::text').getall(),
#         #                                     keHoachHocTap.css('a::attr(href)').getall(),
#         #                                     keHoachHocTap.css('.date::text').getall(),)
#         #         if datetime.strptime(date, "%d/%m/%Y").year >= 2023
#         #     ],


def cleanString(s):
    cleanedString = s.strip()
    cleanedString = re.sub(r'[\r\n\t]', ' ', cleanedString)
    cleanedString = re.sub(' +', ' ', cleanedString)
    cleanedString = cleanedString.replace('\"', '\'')
    return cleanedString
class HcmusspiderSpider(scrapy.Spider):
    # scrapy crawl hcmusSpider -O output.json
    name = "hcmusSpider"

    start_urls = [
        'https://www.ctda.hcmus.edu.vn/vi/thong-bao/',
        'https://www.ctda.hcmus.edu.vn/vi/tin-tuc/',
        'https://www.ctda.hcmus.edu.vn/vi/goc-sinh-vien/thong-tin-can-biet/',
        'https://www.ctda.hcmus.edu.vn/vi/goc-sinh-vien/hoat-dong-sinh-vien/',
        'https://www.fit.hcmus.edu.vn/vn/Default.aspx?tabid=36',
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
            self.parseHCMUS1(response)
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
            if((datetime.strptime(date, "%d/%m/%Y").year == 2023 and
               datetime.strptime(date, "%d/%m/%Y").month == 12) or
               (datetime.strptime(date, "%d/%m/%Y").year == 2024) and
                datetime.strptime(date, "%d/%m/%Y").month >= 1):
                item = {
                    "tieuDe": title.css('a::text').get(),
                    "url": title.css('a::attr(href)').get(),
                    "date": date
                }
                self.resultJson[page].append(item)

        buttonURL = response.css('.pager_load_more::attr(href)').get()
        if buttonURL is not None:
            yield scrapy.Request(buttonURL, callback=self.parsePage, cb_kwargs={'page': page}, dont_filter=True)
        # else:
        #     if page == "Hoat dong sinh vien":
        #         yield self.resultJson



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
            item = {
                # "tieuDe": first.css('.post_title a::text').get(),
                "tieuDe": title,
                "url": 'https://www.fit.hcmus.edu.vn/vn/' + first.css('.post_title a::attr(href)').get(),
                "date": date,
            }
            self.resultJson["FIT-Tin tuc"].append(item)

    def parseHCMUS2(self, response, page):
        posts = response.css('.cmsmasters_archive_item_cont_wrap')
        for post in posts:
            title = cleanString(post.css('.cmsmasters_archive_item_title.entry-title >a::text').get())

            # cleanedString = title.strip()
            # cleanedString = re.sub(r'[\r\n\t]', ' ', cleanedString)
            # cleanedString = re.sub(' +', ' ', cleanedString)
            # cleanedString = cleanedString.replace('\"', '\'')

            url = post.css('.cmsmasters_archive_item_title.entry-title >a::attr(href)').get()
            date = post.css('.published::text').get()

            if ((datetime.strptime(date, "%d/%m/%Y").year == 2023 and
                 datetime.strptime(date, "%d/%m/%Y").month == 12) or
                    (datetime.strptime(date, "%d/%m/%Y").year == 2024) and
                    datetime.strptime(date, "%d/%m/%Y").month >= 1):
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
