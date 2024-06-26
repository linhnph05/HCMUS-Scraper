import json
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(options=chrome_options)

with open('output.json', 'r') as json_file:
    data = json.load(json_file)

dataList = data[0]

# start_urls = ["https://www.fit.hcmus.edu.vn/vn/Default.aspx?tabid=1185",
#               "https://www.fit.hcmus.edu.vn/vn/Default.aspx?tabid=265",
#               "https://www.fit.hcmus.edu.vn/vn/Default.aspx?tabid=493",
#               "https://www.fit.hcmus.edu.vn/vn/Default.aspx?tabid=1186",
#               "https://www.fit.hcmus.edu.vn/vn/Default.aspx?tabid=57",]
#
# sections = ["FIT-Thong tin hoc bong",
#             "FIT-Thong tin tuyen dung",
#             "FIT-Hoi thao/Hoi Nghi",
#             "FIT-Hoat dong sinh vien",
#             "FIT-Thong bao chung",]

# for url, section in zip(start_urls, sections):
#     driver.get(url)
#     print(url)
#     time.sleep(4)
#
#     print("Page 1")
#     dates = driver.find_elements(By.CSS_SELECTOR, "span.time")
#     urls = driver.find_elements(By.CSS_SELECTOR, "ul.list-posts a")
#     titles = driver.find_elements(By.CSS_SELECTOR, "ul.list-posts a > span")
#
#     for date, link, title in zip(dates, urls, titles):
#         year = datetime.strptime(date.text, "%d/%m/%Y").year
#         month = datetime.strptime(date.text, "%d/%m/%Y").month
#         day = datetime.strptime(date.text, "%d/%m/%Y").day
#         if ((datetime.now() - datetime(year, month, day)).days <= 30):
#             item = {
#                 "tieuDe": title.text,
#                 "url": link.get_attribute("href"),
#                 "date": date.text,
#             }
#             dataList[section].append(item)
#
#     print("Page 2")
#     nextPage = driver.find_elements(By.CSS_SELECTOR, "ul.pagination span")
#     nextPage[2].click()
#     time.sleep(4)
#     dates = driver.find_elements(By.CSS_SELECTOR, "span.time")
#     urls = driver.find_elements(By.CSS_SELECTOR, "ul.list-posts a")
#     titles = driver.find_elements(By.CSS_SELECTOR, "ul.list-posts a > span")
#
#     for date, link, title in zip(dates, urls, titles):
#         year = datetime.strptime(date.text, "%d/%m/%Y").year
#         month = datetime.strptime(date.text, "%d/%m/%Y").month
#         day = datetime.strptime(date.text, "%d/%m/%Y").day
#         if ((datetime.now() - datetime(year, month, day)).days <= 30):
#             item = {
#                 "tieuDe": title.text,
#                 "url": link.get_attribute("href"),
#                 "date": date.text,
#             }
#             dataList[section].append(item)
#
# driver.quit()



def writeMdSection(file, section, sections):
    file.write(f'## [{section.replace("\"", "")}]({sections[section]})\n')
    if len(dataList[section]) == 0:
        file.write("No news in the last 1 month\n")
    else:
        for item in dataList[section]:
            file.write(f"* {item["date"]}: [{item["tieuDe"]}]({item["url"]})\n")

with open('../announcements.md', 'w') as md_file:
    md_file.write(f'# All news in the last 1 month \n_Last update: **{datetime.now(tz=ZoneInfo("Asia/Ho_Chi_Minh")).strftime("%H:%M:%S %d/%m/%Y")}**_\n')
    sections = {
        "Thong Bao": "https://www.ctda.hcmus.edu.vn/vi/thong-bao/",
        "Tin tuc": "https://www.ctda.hcmus.edu.vn/vi/tin-tuc/",
        "Thong tin can biet": "https://www.ctda.hcmus.edu.vn/vi/goc-sinh-vien/thong-tin-can-biet/",
        "Hoat dong sinh vien": "https://www.ctda.hcmus.edu.vn/vi/goc-sinh-vien/hoat-dong-sinh-vien/",
        "FIT-Tin tuc": "https://www.fit.hcmus.edu.vn/vn/Default.aspx?tabid=36",
        "FIT-THÔNG TIN CHUNG": "https://www.fit.hcmus.edu.vn/vn/Default.aspx?tabid=53",
        "FIT-THÔNG TIN HỌC BỔNG": "https://www.fit.hcmus.edu.vn/vn/Default.aspx?tabid=53",
        "FIT-THÔNG TIN HỘI THẢO - HỘI NGHỊ": "https://www.fit.hcmus.edu.vn/vn/Default.aspx?tabid=53",
        "FIT-HOẠT ĐỘNG SINH VIÊN": "https://www.fit.hcmus.edu.vn/vn/Default.aspx?tabid=53",
        "FIT-THÔNG TIN TUYỂN DỤNG": "https://www.fit.hcmus.edu.vn/vn/Default.aspx?tabid=53",
        "HCMUS-Thong tin nguoi hoc": "https://hcmus.edu.vn/thong-tin-danh-cho-nguoi-hoc/",
        "HCMUS-Thong tin sinh vien": "https://hcmus.edu.vn/category/dao-tao/dai-hoc/thong-tin-danh-cho-sinh-vien/",
        "HCMUS-Tuyen dung": "https://hcmus.edu.vn/category/tuyen-dung-viec-lam/",
        "HCMUS-Nguoi hoc": "https://hcmus.edu.vn/category/nguoi-hoc/",
        "HCMUS-Hoc bong dai hoc": "https://hcmus.edu.vn/category/dao-tao/dai-hoc/hoc-bong-dai-hoc/"
    }
    for section in sections:
        writeMdSection(md_file, section, sections)

