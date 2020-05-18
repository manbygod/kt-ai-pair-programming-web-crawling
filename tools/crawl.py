from bs4 import BeautifulSoup
import requests, os, base64
from selenium import webdriver
from . import singleton

class CrawlTool(metaclass=singleton.Singleton):
    def __init__(self):
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome('chromedriver', options=options)
        self.driver.implicitly_wait(3)
        
    def getSoupContentFromUrl(self, url, **args):
        
        if type(url) is not str:
            return ""
        
        url += "?"
        
        for k, v in args.items():
            url += f'{k}={v}&'
            
        print(url)
            
        self.driver.get(url)
        
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        return soup
    
    def getDaumNews(self, date):
        
        url = 'https://media.daum.net/ranking/'
        soup = self.getSoupContentFromUrl(url, regDate=date)
        
        soup = soup.select('a.link_txt')
        news = [ dict(news_link = tag.get('href'), news_text = tag.get_text()) for tag in soup if tag.get('href') is not None ]
        
        return news
    
    def getTextNews(self, url):
        
        soup = self.getSoupContentFromUrl(url)
        soup = soup.select('div.article_view > section > p')
        
        text_news = [ article.get_text() for article in soup ]
        text_news = " ".join(text_news)
        
        return text_news
    
    def getGoogleImages(self, keyword):
        url = f'https://www.google.com/search?q={keyword}&rlz=1C1CHBD_koKR896KR896&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiAua_v2rTpAhVUVN4KHdZOBIkQ_AUoAXoECBYQAw&biw=1536&bih=674&dpr=1.25'
        
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        soup = soup.select('img.rg_i')
        img_binary_type = [ tag.get('src') for tag in soup if tag.get('src') is not None ]
        img_binaries = [ base64.b64decode(img_data.split(',')[1]) for img_data in img_binary_type ]
        img_links = [ tag.get('data-src') for tag in soup if tag.get('data-src') is not None ] 
        
        return img_binaries, img_links