from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
      'Cookie':'uuid=3bfbeb56-9f3e-4d0d-cbe3-260b14154476; cityDomain=gy; ganji_uuid=2943330065231720816366; lg=1; antipas=z6683504k93003WPO325643r3; clueSourceCode=%2A%2300; user_city_id=36; sessionid=c1cf6d12-f864-40c1-be6a-689466580011; close_finance_popup=2020-07-27; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%223bfbeb56-9f3e-4d0d-cbe3-260b14154476%22%2C%22ca_city%22%3A%22gy%22%2C%22sessionid%22%3A%22c1cf6d12-f864-40c1-be6a-689466580011%22%7D; Hm_lvt_936a6d5df3f3d309bda39e92da3dd52f=1595389723,1595834426,1595834461; guazitrackersessioncadata=%7B%22ca_kw%22%3A%22-%22%7D; preTime=%7B%22last%22%3A1595835397%2C%22this%22%3A1595389721%2C%22pre%22%3A1595389721%7D; Hm_lpvt_936a6d5df3f3d309bda39e92da3dd52f=1595835398'}


class Website(ABC):

    def __init__(self, city_name):
        self.name = city_name  # 名稱

    @abstractmethod
    def scrape(self):  # 爬取(抽象方法)
        pass



class Klook(Website):

    def scrape(self):

        result = []  # 回傳結果

        if self.name:  # 如果城市名稱非空值

            if self.name=='tesla':
                self.name='tesila'
            
            response = requests.get(
                f"https://www.guazi.com/gy/{self.name}/o1/#bread",headers=headers)
            soup = BeautifulSoup(response.text, "lxml")

            # 取得十個元素
            li_list = soup.find('ul',{'class':'carlist clearfix js-top'}).find_all('li', limit=5)

            for li in li_list:

                # 車名
                title = li.find('h2',{'class':"t"}).get_text()

                # 車連結
                link = "https://www.guazi.com" + li.find('a').get('href')

                    
                # 車資料
                data = li.find('div',{'class':'t-i'}).get_text()
                #上牌年
                year = data.split('|')[0]
                #里程數
                mileage = data.split('|')[1]
                # 錢
                moneyTW =li.find('div',{'class':'t-price'}).find('p').get_text()
                price = int(eval(moneyTW[:-2])*43100) #人民幣換台幣 1:4.31
                price  = format(price,',')#+'元'

                result.append(
                    dict(title=title, link=link, price=price, booking_date=year, star=mileage[:4], source="https://image.guazistatic.com/gz01190923/15/39/f3eebb2bedbd15fc6fb8e3226bf35e44.png"))

        return result



class Kkday(Website):

    def scrape(self):

        result = []  # 回傳結果

        if self.name:  # 如果名稱非空值

            response = requests.get(
                f"https://auctions.yahoo.co.jp/search/search?auccat=26360&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&p={self.name}&x=0&y=0",headers=headers).text

            # 資料
            soup = BeautifulSoup(response,'lxml')
            div_list = soup.find('div',{'class':'inner cf'}).find_all('div',{'class':'bd cf'},limit=10)
            for div in div_list:

                # 名稱
                title = div.find('div',{'class':"a__title"}).get_text()

                # 連結
                link = div.find('a').get('href')

                # 價格
                moneyTW =div.find('dl',{'class':'pri1'}).find('dd').get_text()
                price = int(int(''.join(moneyTW[:-1].split(',')))*0.25)#日幣換台幣 1:0.25
                price  = format(price,',')#+'元'

                res = requests.get(link,headers=headers).text
                sop = BeautifulSoup(res,'lxml')
                Keyaspect = sop.find('div',{'class':"Keyaspect"}).get_text()
                k=Keyaspect.split('/')
                # 上牌年
                year = k[0].split('：')[1]

                # 里程數
                mileage = k[1].split('：')[1]

                result.append(
                    dict(title=title, link=link, price=price, booking_date=year, star=mileage, source='https://s.yimg.jp/images/auc/pc/top/image/2.0.0/logo_yahuoku_01.png'))

        return result
