# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import numpy as np
import re
import json
from .create_food_token import MakeToken, Info
from fake_useragent import UserAgent
from meituan.items import MeituanItem
from .cookies import Cookies
import random


class CitysSpider(scrapy.Spider):
    name = 'citys'
    allowed_domains = ['meituan.com']
    # start_urls = ['https://www.meituan.com/changecity/']

    def start_requests(self):
        info = Info()
        b = info.get_info()
        for i in b:
            
            areaId, cityName, originUrl, page = info.pre(i)
            token = MakeToken(areaId, cityName, originUrl, page)
            a = token.join_token
            USER_AGENT = self.headers()
            url = "https://www.meituan.com/meishi/" + str(areaId) + "/"
            yield scrapy.Request(url=url,
                                 headers={"User-Agent": USER_AGENT},
                                 callback=self.parse,
                                 cookies={"Cookie": self.get_cookies()},
                                 meta={
                                     'dont_redirect': True,
                                     'handle_httpstatus_list': [302]}
                                 )

    def parse(self, response):
        response_str = response.body_as_unicode()
        detail_info = re.search(
            r'"detailInfo":\{"poiId":(\d+),"name":"(.*?)","avgScore":(.*?),"address":"(.*?)","phone":"(.*?)","openTime":"(.*?)","extraInfos":\[(.*?)\],"hasFoodSafeInfo":(.*?),"longitude":(.*?),"latitude":(.*?),"avgPrice":(\d+),"brandId":(\d+),"brandName":"(.*?)",".*?photos":{"frontImgUrl":"(.*?)","albumImgUrls":(.*?)},"recommended":(.*?),"crumbNav":(.*?),"prefer',
            response_str)
        if detail_info:
            poiId = detail_info.group(1)
            name = detail_info.group(2)
            avgScore = detail_info.group(3)
            address = detail_info.group(4)
            phone = detail_info.group(5)
            openTime = detail_info.group(6)
            extraInfos = detail_info.group(7)
            hasFoodSafeInfo = detail_info.group(8)
            longitude = detail_info.group(9)
            latitude = detail_info.group(10)
            avgPrice = detail_info.group(11)
            brandId = detail_info.group(12)
            brandName = detail_info.group(13)
            frontImgUrl = detail_info.group(14)
            albumImgUrls = detail_info.group(15)
            # 其他信息解析
            if extraInfos:
                items = json.loads("[" + extraInfos + "]")
                extraInfos = ''
                for item_1 in items:
                    extraInfos = item_1.get('text') + '  ' + extraInfos
            # 推荐菜处理
            recommended = json.loads(detail_info.group(16))
            #     # 打印推荐菜
            global recommend_name
            global recommend_price
            global recommend_img
            for item_1 in list(recommended):
                # recommend_id = item['id']  # 推荐菜id
                recommend_name = item_1['name']  # 推荐菜名
                recommend_price = item_1['price']  # 菜品价格
                recommend_img = item_1['frontImgUrl']  # 菜品图片
                # print(recommend_name, end=' ')

            # 面包屑抽离
            crumbNav = json.loads(detail_info.group(17))
            area = crumbNav[0].get('title')[:-2]
            food_type = crumbNav[2].get('title')[len(area):]
            item = MeituanItem()
            item['area'] = area,
            item['food_type'] = food_type,
            item['poiId'] = poiId,
            item['name'] = name,
            item['avgScore'] = avgScore,
            item['address'] = address,
            item['phone'] = phone,
            item['openTime'] = openTime,
            item['extraInfos'] = extraInfos,
            item['hasFoodSafeInfo'] = hasFoodSafeInfo,
            item['longitude'] = longitude,
            item['latitude'] = latitude,
            item['avgPrice'] = avgPrice,
            item['brandId'] = brandId,
            item['brandName'] = brandName,
            item['frontImgUrl'] = frontImgUrl,
            item['albumImgUrls'] = albumImgUrls,
            item['recommend_name'] = recommend_name,
            item['recommend_price'] = recommend_price,
            item['recommend_img'] = recommend_img,
            yield item

    def read(self, num):
        # 读取指定列索引字段的数据
        csv_data = pd.read_csv("./test.csv", usecols=[num])
        train_data = np.array(csv_data)  # np.ndarray()
        return train_data.tolist()  # list

    def headers(self):
        ua = UserAgent()
        user_agent = ua.random
        return user_agent

    def get_cookies(self):
        cookie = Cookies[random.randint(0, len(Cookies) - 1)]
        return cookie





