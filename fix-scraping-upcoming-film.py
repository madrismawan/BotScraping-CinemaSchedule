#!/usr/bin/env python
# coding: utf-8

# In[1]:


import urllib3
from bs4 import BeautifulSoup
from datetime import datetime
import mysql.connector


# In[2]:


URL = 'https://jadwalnonton.com/comingsoon/'
http = urllib3.PoolManager()
r = http.request('GET', URL)
soup = BeautifulSoup(r.data, 'html.parser')
page = soup.findAll('div','paggingcont')


# In[3]:


##Get Page FILM
data = []
data.clear()
for x in page:
    test = x.findAll('a', href=True)
    for x in test:
        test = x.get('href')
        data.append(test)


# In[4]:


##Get Data Page Film URL
data.append("https://jadwalnonton.com/comingsoon/")
del data [0]
del data [0]
print (data)


# In[5]:


def getContent(url):
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    r.status
    soup = BeautifulSoup(r.data, 'html.parser')
    allData = soup.findAll('div','row clearfix mvlist')
    scrapingData(allData)


# In[6]:


def parseTime():
    current = datetime.now()

    tahun = current.year
    bulan = current.month
    hari = current.day

    now = ('{}/{}/{}').format(tahun, bulan, hari)
    return now


# In[7]:


def simpanDatabase(data):
    mydb = mysql.connector.connect(
        host="us-cdbr-east-03.cleardb.com",
        user="b86bf40d7a0a5e",
        password="5b88fc4d",
        database="heroku_116ec58047c2dc4"
#         host="localhost",
#         user="root",
#         password="",
#         database="db-bioskop"  
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO upcoming (judul,katagori,menit,tahun,director,actor,tanggal) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql, data)
    mydb.commit()


# In[8]:


def scrapingData(allData):
    for x in allData:
        dataList = x.findAll('div','col-xs-6 moside')
        for x in dataList:
            judul = x.find('a')
            jenis = judul.find_next('span')
            menit = jenis.find_next('span')
            tahun = menit.find_next('span')
            an = tahun.find_next('span')
            director = an.find_next('span')
            un = director.find_next('span')
            pemeran = un.find_next('span')
            data = (judul.text,jenis.text,menit.text,tahun.text,director.text,pemeran.text,parseTime())        
            simpanDatabase(data)


# In[9]:


def main(data):
    for url in data:
        getContent(url)
        parseTime()
        print("data berhasil disimpan")


# In[ ]:


##Scraping Otomatis saat jam 9
import schedule
import time

schedule.every().day.at("02:25").do(main,data)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute


# In[ ]:




