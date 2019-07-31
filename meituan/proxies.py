from lxml import etree
import requests
import random
import pandas as pd
import numpy as np

class Proxies:

    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"}
        self.url = "https://www.xicidaili.com/nn/"

    def parse_url(self):
        response = requests.get(self.url, headers=self.headers)
        response = response.content.decode()
        html = etree.HTML(response)
        pro_div = html.xpath("//table[@id='ip_list']//tr")
        pro_list = []
        for div in pro_div[1:]:
            pro = div.xpath("./td[2]/text()")
            pro = "".join(pro)
            pro_1 = div.xpath("./td[3]/text()")
            pro_1 = "".join(pro_1)
            pro_2 = div.xpath("./td[6]/text()")
            pro_2 = "".join(pro_2)
            pro_list.append(pro_2 + '://' + pro + ':' + pro_1)
        self.save(pro_list)


    def get_ip(self):
        # 读取指定列索引字段的数据
        csv_data = pd.read_csv("./ip.csv", )
        train_data = np.array(csv_data)  # np.ndarray()
        train_data = train_data.tolist()
        proxy_ip = random.choice(train_data)
        proxy_ip = "".join(proxy_ip)
        proxies = {'http': proxy_ip}
        return proxies

    def save(self, details):
        file = "./ip.csv"
        dataframe = pd.DataFrame(details)
        dataframe.to_csv(file, index=False, sep=',', encoding="utf_8_sig",mode='w', header=False)

if __name__ == '__main__':
    p = Proxies()
    a = p.parse_url()
    c = p.get_ip()
    print(c)
#     print(a)
    # file = "ip.csv"
    # dataframe = pd.DataFrame(a,)
    # dataframe.to_csv(file, index=False, sep=',', encoding="utf_8_sig", mode='a', header=True)




















