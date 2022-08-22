#!/usr/bin/env python
# coding: utf-8
#pip install selenium
#pip install bs4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import Sehirler
import Odalar

def selectFromDict(options, name):
    index = 0
    indexValidList = []
    print('Lütfen ' + name + ' seçiniz :')
    for optionName in options:
        index = index + 1
        indexValidList.extend([options[optionName]])
        print(str(index) + ') ' + optionName)
    inputValid = False
    while not inputValid:
        inputRaw = input(name + ': ')
        inputNo = int(inputRaw) - 1
        if inputNo > -1 and inputNo < len(indexValidList):
            selected = indexValidList[inputNo]
            # print('Seçilen ' +  name + ': ' + selected)
            inputValid = True
            break
        else:
            print('Lütfen geçerli bir ' + name + ' seçiniz')
    
    return selected

def siteden_icerik_alma():
    s = Service('C:\\Users\\Lenovo\\Python Projects\\chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    sehir=selectFromDict(Sehirler.Sehirler().sehirler, 'şehir')
    oda=selectFromDict(Odalar.Odalar().odalar, 'oda sayısı')    
    url=f'https://www.emlakjet.com/kiralik-daire/{sehir}/?oda_sayisi[]={oda}'
    driver.get(url)
    content = driver.page_source
    return content
    
soup = BeautifulSoup(siteden_icerik_alma(),"lxml")

def sinifa_gore_icerik_temizleme(sinif: str):
    icons=soup.select(sinif)
    for i in icons:
        i.decompose()

sinifa_gore_icerik_temizleme(".material-icons")

def select_html_tag_from_class(sinif: str,tag: str):
    baslik_listesi=[]
    basliklar=soup.select(sinif)
    for i in basliklar:
        baslik=i.find(tag)
        baslik_listesi.append(baslik.text)
    return baslik_listesi
    
baslik_listesi=select_html_tag_from_class(".manJWF","span")
fiyat_listesi=select_html_tag_from_class("._2C5UCT","span")
lokasyon_listesi=select_html_tag_from_class("._2wVG12","span")

#classın içinden birden fazla span almak gerekirse 
def select_multiple_tag_from_class(sinif: str,tag:str,tag_count: int ):
    baslik_listesi=[]
    basliklar=soup.select(sinif)
    for i in basliklar:
        baslik=i.findAll(tag)
        mlist=[]
        for m in range(tag_count):
            mlist.append(baslik[m].text)
            if(m==tag_count-1):
                baslik_listesi.append(mlist)
    return baslik_listesi

dlist=select_multiple_tag_from_class("._2UELHn","span",5)

    
df = pd.DataFrame({'İlan Başlığı':baslik_listesi,'Fiyat':fiyat_listesi,
                   'Lokasyon':lokasyon_listesi,'Özellikler':dlist}) 
df.to_csv('ilanlar.csv', index=False, encoding='utf-16', sep=";")







