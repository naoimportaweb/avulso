import os, requests, sys, traceback, hashlib, re, base64;

from bs4 import BeautifulSoup
from lxml import etree

class Web:
    def __init__(self):
        self.dom = None;
        headers ={'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'}
        self.session = requests.session()
        self.session.headers = headers       # <-- set default headers here
        pass;
    
    def navegate(self, url):
        soup = BeautifulSoup(self.download(url, backup=False), "html.parser")
        self.dom = etree.HTML(str(soup))
    
    def elements(self, xpath, by=None):
        if by != None:
            return by.xpath(xpath);
        return self.dom.xpath(xpath);

    def element(self, xpath, by=None):
        if by != None:
            return by.xpath(xpath)[0];
        buffer = self.elements(xpath);
        if len(buffer) > 0:
            return buffer[0];
        return None;

    def download(self, url, backup=True):
        page = None;
        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'}
        try:
            r = self.session.get(url);
            print(r.status_code);
            return r.text
        except:
            print("Status code "+ str(page.status_code) +" " + url);
            traceback.print_exc();
        return  None;

w = Web();
w.navegate('https://nicebooks.com/us/search/isbn');
w.navegate("https://nicebooks.com/us/search/isbn?isbn=9788576059240");
if  w.element('//*[@id="isbn-search"]/div[2]/div/div[2]/div/div[2]/div[1]/a') != None:
    w.navegate( "https://nicebooks.com/" + w.element('//*[@id="isbn-search"]/div[2]/div/div[2]/div/div[2]/div[1]/a').get('href'));
    elements = w.elements('//*[@id="book"]/div[2]/div[2]/div[1]/div[2]/div');
    autores = [];
    for element in elements:
        buffer1 = w.element("./a", by=element);
        buffer2 = w.element("./a/span", by=element);
        autores.append({"name" : buffer2.text, "href" : "https://nicebooks.com" + buffer1.get("href")});
    print("Titulo:",  w.element('//*[@id="book"]/div[1]/div/h1/span').text );
    print("Autor:",  autores ); #/a/span

    print("Data:",  w.element('//*[@id="book"]/div[2]/div[2]/div[4]/div[2]').text );
    print("Languae:",  w.element('//*[@id="book"]/div[2]/div[2]/div[5]/div[2]/div').text );
    print("Formato:",  w.element('//*[@id="book"]/div[2]/div[2]/div[6]/div[2]').text );
    print("Pages:",  w.element('//*[@id="book"]/div[2]/div[2]/div[7]/div[2]').text );

    elements = w.elements('//*[@itemprop="isbn"]');
    isbns = [];
    for element in elements:
        isbns.append( re.sub(r'\W', "", element.text ) );
    print("ISBN:", isbns );

