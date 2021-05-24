#!/usr/bin/env python
# coding: utf-8

# In[1]:


import urllib3
from bs4 import BeautifulSoup
from datetime import datetime
import mysql.connector


# In[2]:


def main():
    URL = 'https://jadwalnonton.com/bioskop/di-bali/tsm-xxi-bali.html'
    http = urllib3.PoolManager()
    r = http.request('GET', URL)
    r.status
    soup = BeautifulSoup(r.data, 'html.parser')
    allData = soup.findAll('div','item')
    print("==== Bioskop ====")
    tanggal = soup.find('span','right')
    print(tanggal.text)
    print(soup.h1.text)
    parseTime()
    scrapingData(allData)
    print("Data Berhasil dimasukan ke database")


# In[3]:


def parseTime():
    current = datetime.now()

    tahun = current.year
    bulan = current.month
    hari = current.day

    now = ('{}/{}/{}').format(tahun, bulan, hari)
    return now


# In[4]:


def simpanData(data):
    mydb = mysql.connector.connect(
      host="us-cdbr-east-03.cleardb.com",
      user="b86bf40d7a0a5e",
      password="5b88fc4d",
      database="heroku_116ec58047c2dc4"
    )
    mycursor = mydb.cursor()

    sql = "INSERT INTO 21cineplex (judul, genre,harga,waktu,tanggal) VALUES (%s, %s,%s, %s, %s)"
    mycursor.execute(sql, data)
    mydb.commit()


# In[5]:


def scrapingData(allData):
    hasil = ''
    for item in allData:
        output = ''
        test = item.find('div','col-sm-2')
        if(test != None):
            hallo = test.a.img
            src = hallo.get('src')
        name = item.find('h2')
        if(name != None):
            name = name.text
            showtime = item.find('ul','usch')
            harga = item.find('p','htm')
            genre = item.find('p')
            output = ''
            for data in showtime :
                output =  output +  '--->' + data.text

            data = (name,genre.text,harga.text,output,parseTime())
            simpanData(data)


# In[ ]:


##Scraping Otomatis saat jam 9
import schedule
import time

schedule.every().day.at("02:25").do(main)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute


# In[ ]:




