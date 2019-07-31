# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    areaId = scrapy.Field()
    cityName = scrapy.Field()
    originUrl = scrapy.Field()
    page = scrapy.Field()
    area = scrapy.Field()
    food_type = scrapy.Field()
    poiId = scrapy.Field()
    name = scrapy.Field()
    avgScore = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    openTime = scrapy.Field()
    extraInfos = scrapy.Field()
    hasFoodSafeInfo = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    avgPrice = scrapy.Field()
    brandId = scrapy.Field()
    brandName = scrapy.Field()
    frontImgUrl = scrapy.Field()
    albumImgUrls = scrapy.Field()
    recommend_name = scrapy.Field()
    recommend_price = scrapy.Field()
    recommend_img = scrapy.Field()
