#!/usr/bin/env python
# coding: utf-8

# In[1]:


import telebot
from telebot import types
from datetime import datetime
import mysql.connector


# In[2]:


token ='1709240275:AAFbKItOnk7gwFsO59uXyYcQXzsrMClYuwI'
bot = telebot.TeleBot(token)


# In[3]:


@bot.message_handler(commands=['start'])
def start(message):
    keyboardmain = types.InlineKeyboardMarkup(row_width=2)
    upcoming = types.InlineKeyboardButton(text="Upcoming FILM", callback_data="upcoming")
    bioskop = types.InlineKeyboardButton(text="Jadwal FILM", callback_data="bioskop")
    keyboardmain.add(upcoming, bioskop)
    bot.send_message(message.chat.id, "===> Selamat Datang di Pencarian FILM di BALI <===", reply_markup=keyboardmain)


# In[4]:


@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    if call.data == "mainmenu":
        menu(call)
    elif call.data == "bioskop":
        daftarBioskop(call)
    elif call.data == "upcoming":
        upcoming(call)
    elif call.data == "cinepolis":
        cinepolis(call)
    elif call.data == "21cineplex":
        cineplex21(call)
    elif call.data == "dpscineplex":
        dpscineplex(call)


# In[5]:


def menu(call):
    keyboardmain = types.InlineKeyboardMarkup(row_width=2)
    upcoming = types.InlineKeyboardButton(text="Upcoming FILM", callback_data="upcoming")
    bioskop = types.InlineKeyboardButton(text="Jadwal FILM", callback_data="bioskop")
    backbutton = types.InlineKeyboardButton(text="Back", callback_data="mainmenu")
    keyboardmain.add(upcoming, bioskop)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text= "===> Selamat Datang di Pencarian FILM di BALI <===", reply_markup=keyboardmain)


# In[6]:


def daftarBioskop(call):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    bioskop1 = types.InlineKeyboardButton(text="Cinepolis", callback_data="cinepolis")
    bioskop2 = types.InlineKeyboardButton(text="21Cineplex", callback_data="21cineplex")
    bioskop3 = types.InlineKeyboardButton(text="Denapasar Cineplex", callback_data="dpscineplex")
    backbutton = types.InlineKeyboardButton(text="Back", callback_data="mainmenu")
    keyboard.add(bioskop1, bioskop2, bioskop3,backbutton)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="===========> Pilihlah Daftar Jadwal Bioskop <===========",reply_markup=keyboard)


# In[7]:


#Membuat Fungsi Waktu Sekarang
def parseTimeDatabase():
    current = datetime.now()
    tahun = current.year
    bulan = current.month
    hari = current.day
    now = ('{}-{}-{}').format(tahun, bulan, hari)
    return now


# In[8]:


#Membuat Fungsi Waktu Sekarang
def parseTime():
    current = datetime.now()
    tahun = current.year
    bulan = current.month
    hari = current.day
    now = ('{}-{}-{}').format(hari, bulan,tahun)
    return now


# In[9]:


def upcoming(call):
    mydb = mysql.connector.connect(
            host="us-cdbr-east-03.cleardb.com",
            user="b86bf40d7a0a5e",
            password="5b88fc4d",
            database="heroku_116ec58047c2dc4"
        ) 
    
    mycursor = mydb.cursor()
    sql = "SELECT * FROM upcoming WHERE tanggal = %s"
    adr = (parseTimeDatabase(), )
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()

    listJadwal = ''
    for x in myresult:
        judul =  x[1]
        katagori = x[2]
        waktu =  x[3]
        tahun =  x[4]
        director =  x[5]
        actor =   x[6]
        listJadwal = listJadwal+'\n' + 'Judul    : '+judul+'\n'+'Katagori : '+katagori+'\n'+'Durasi   :'+waktu+'\n'+'Tahun    : '+tahun+'\n'+'Director : "'+director+'\n'
    pesan = '==> Jadwal Bioskop Tanggal '+parseTime()+' di Cinepolis<==\n'+listJadwal
    bot.send_message(chat_id=call.message.chat.id,text=pesan)


# In[10]:


##SELECT CINEPOLIS
def cinepolis(call):
    ##Koneksi Database
    mydb = mysql.connector.connect(
            host="us-cdbr-east-03.cleardb.com",
            user="b86bf40d7a0a5e",
            password="5b88fc4d",
            database="heroku_116ec58047c2dc4"
        )

    mycursor = mydb.cursor()
    sql = "SELECT * FROM cinepolis WHERE tanggal = %s"
    adr = (parseTimeDatabase(), )
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()

    listJadwal = ''
    for x in myresult:
        bioskop =  x[1]
        judul =   x[2]
        katagori =  x [3]
        waktu =  x[4]
        harga =   x[5]
        listJadwal = listJadwal+'\n' + 'Bioskop    : '+bioskop+'\n'+'Judul Film : '+judul+'\n'+'Katagori   : '+katagori+'\n'+'Jam Tayang : '+waktu+'\n'+'Harga      : Rp.'+harga+'\n'
    pesan = '==> Jadwal Bioskop Tanggal '+parseTime()+' di Cinepolis<==\n'+listJadwal
    bot.send_message(chat_id=call.message.chat.id,text=pesan)
    


# In[11]:


##SELECT 21CINEPLEX
def cineplex21(call):
    ##Koneksi Database
    mydb = mysql.connector.connect(
            host="us-cdbr-east-03.cleardb.com",
            user="b86bf40d7a0a5e",
            password="5b88fc4d",
            database="heroku_116ec58047c2dc4"
        )
    
    mycursor = mydb.cursor()
    sql = "SELECT * FROM 21cineplex WHERE tanggal = %s"
    adr = (parseTimeDatabase(), )
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()

    listJadwal = ''
    for x in myresult:
        judulKatagori = x[1]
        katagoriJamtayang = x[2]
        harga = x[3].replace('Harga tiket masuk ', '')
        waktu = x[4]
        listJadwal = listJadwal+'\n'+'Judul & Katagori : '+judulKatagori+'\n'+'Katagori & Menit : '+katagoriJamtayang+'\n'+'Harga            : '+harga+'\n'+'Jam Tayang       : '+waktu+'\n'
    pesan = '==> Jadwal Bioskop Tanggal '+parseTime()+' di 21Cineplex<==\n'+listJadwal
    bot.send_message(chat_id=call.message.chat.id,text=pesan)
    


# In[12]:


##SELECT DPSCINEPLEX
def dpscineplex(call):
    ##Koneksi Database
    mydb = mysql.connector.connect(
            host="us-cdbr-east-03.cleardb.com",
            user="b86bf40d7a0a5e",
            password="5b88fc4d",
            database="heroku_116ec58047c2dc4"
        )
    
    mycursor = mydb.cursor()
    sql = "SELECT * FROM dpscineplex WHERE tanggal = %s"
    adr = (parseTimeDatabase(), )
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()

    listJadwal = ''
    for x in myresult:
        judulKatagori = x[1]
        katagoriJamtayang = x[2]
        harga = x[3].replace('Harga tiket masuk ', '')
        waktu = x[4]
        listJadwal = listJadwal+'\n'+'Judul & Katagori : '+judulKatagori+'\n'+'Katagori & Durasi : '+katagoriJamtayang+'\n'+'Harga            : '+harga+'\n'+'Jam Tayang       : '+waktu+'\n'
    pesan = '==> Jadwal Bioskop Tanggal '+parseTime()+' di 21Cineplex<==\n'+listJadwal
    bot.send_message(chat_id=call.message.chat.id,text=pesan)
    


# In[ ]:


if __name__ == "__main__":
    bot.polling(none_stop=True)


# In[ ]:





# In[ ]:




