import scrapy

class post(scrapy.Item):
   update_time = scrapy.Field()
   thong_bao = scrapy.Field()
   tin_tuc = scrapy.Field()
   thong_tin_can_biet = scrapy.Field()
   hoat_dong_sinh_vien = scrapy.Field()
   fit_tin_tuc = scrapy.Field()
   hcmus_thong_tin_sinh_vien = scrapy.Field()
   hcmus_tuyen_dung = scrapy.Field()
   hcmus_nguoi_hoc = scrapy.Field()
   hcmus_hoc_bong_dai_hoc = scrapy.Field()
