#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from datetime import datetime
import json
import time
import mysql.connector


# In[2]:


#Membuat Fungsi Waktu Sekarang
def parseTime():
    current = datetime.now()

    tahun = current.year
    bulan = current.month
    hari = current.day

    now = ('{}/{}/{}').format(hari, bulan, tahun)
    return now


# In[3]:


def parseTimeDatabase():
    current = datetime.now()

    tahun = current.year
    bulan = current.month
    hari = current.day

    now = ('{}/{}/{}').format(tahun, bulan, hari)
    return now


# In[4]:


##Fungsi buat Nyimpen ke Database
def simpanDatabase(data):
    mydb = mysql.connector.connect(
      host="us-cdbr-east-03.cleardb.com",
      user="b86bf40d7a0a5e",
      password="5b88fc4d",
      database="heroku_116ec58047c2dc4"
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO cinepolis (bioskop, judul,katagori,waktu,harga,tanggal) VALUES (%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql, data)
    mydb.commit()
    return


# In[5]:


def scrapingData(List):
    for i in List:
        bioskop = i['Title']
        jenis = i['MovieTimeList']
        for i in jenis:
            judul = i['Title']
            katagori = i['Ratings']
            dataHarga = i['ClassShowTimePriceList']
            for i in dataHarga:
                typeB = i['Title']
                dataJam = i['ShowTimePriceList']
                jam = ''
                for i in dataJam:
                    jam =  jam +  '--->' + i['ShowTime']
                    dataUang = i['PriceList']
                for i in dataUang:
                    harga = i['PriceInt']
                data = (bioskop,judul,katagori+typeB,jam,harga,parseTimeDatabase())
                
                simpanDatabase(data)


# In[6]:


def main():
    r = requests.post('https://cinepolis.co.id/Schedule.aspx/GetSchCinemaMovieData', json = {'cityCode':'BAL', 'dateValue':parseTime()})
    page_json = r.json()

    # data = json.loads(page_json)
    page = json.dumps(page_json)
    data = json.loads(page)
    test = data['d']['List']
    page = json.dumps(test)
    data2 = json.loads(page)

    page_json = r.json()
    List = page_json['d']['List']
    scrapingData(List)
    print("data Berhasil dimasukan ke database")


# In[ ]:


##Scraping Otomatis saat jam 9
import schedule
import time


schedule.every().day.at("02:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute


# In[ ]:





# In[ ]:





# In[ ]:




