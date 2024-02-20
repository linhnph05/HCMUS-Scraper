import json
from datetime import datetime
from zoneinfo import ZoneInfo

with open('output.json', 'r') as json_file:
    data = json.load(json_file)

dataList = data[0]

def writeMdSection(file, section):
    file.write(f'## {section}\n')
    for item in dataList[section]:
        file.write(f"* {item["date"]}: [{item["tieuDe"]}]({item["url"]})\n")

with open('../announcements.md', 'w') as md_file:
    md_file.write(f'# All news\n_Last update: **{datetime.now(tz=ZoneInfo("Asia/Ho_Chi_Minh"))}**_\n')
    sections = ["Thong Bao",
                "Tin tuc",
                "Thong tin can biet",
                "Hoat dong sinh vien",
                "FIT-Tin tuc",
                "HCMUS-Thong tin nguoi hoc",
                "HCMUS-Thong tin sinh vien",
                "HCMUS-Tuyen dung",
                "HCMUS-Nguoi hoc",
                "HCMUS-Hoc bong dai hoc"]
    for section in sections:
        writeMdSection(md_file, section)

