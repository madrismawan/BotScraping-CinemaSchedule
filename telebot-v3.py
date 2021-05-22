#!/usr/bin/env python
# coding: utf-8

# In[1]:


import telebot
from telebot import types
from datetime import datetime


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
        upcoming(call)
    elif call.data == "dpscineplex":
        upcoming(call)
    elif call.data == "test":
        testing(call)


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
    bioskop2 = types.InlineKeyboardButton(text="21Cineplex", callback_data="3")
    bioskop3 = types.InlineKeyboardButton(text="Denapasar Cineplex", callback_data="1")
    backbutton = types.InlineKeyboardButton(text="Back", callback_data="mainmenu")
    keyboard.add(bioskop1, bioskop2, bioskop3,backbutton)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Pilihlah Daftar Bioskop",reply_markup=keyboard)


# In[7]:


def upcoming(call):
    keyboard = types.InlineKeyboardMarkup()
    bioskop1 = types.InlineKeyboardButton(text="Cinepolis", callback_data="cinepolis")
    backbutton = types.InlineKeyboardButton(text="Back", callback_data="mainmenu")
    keyboard.add(bioskop1,backbutton)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="replaced text",reply_markup=keyboard)


# In[8]:


def testing(call):
    bot.send_message(chat_id=call.message.chat.id,text= "===> Selamat Datang di Pencarian FILM di BALI <===")


# In[9]:


#Membuat Fungsi Waktu Sekarang
def parseTimeDatabase():
    current = datetime.now()

    tahun = current.year
    bulan = current.month
    hari = current.day

    now = ('{}-{}-{}').format(tahun, bulan, hari)
    return now


# In[10]:


import mysql.connector


# In[11]:


##Koneksi Database
mydb = mysql.connector.connect(
      host="us-cdbr-east-03.cleardb.com",
      user="b86bf40d7a0a5e",
      password="5b88fc4d",
      database="heroku_116ec58047c2dc4"
    )


# In[12]:


parseTimeDatabase()


# In[13]:


def cinepolis(call):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM cinepolis WHERE tanggal=%s"
    adr = (parseTimeDatabase(), )
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()
    
    for x in myresult:
        bioskop = "Bioskop :" + x[1]
        judul =  "Film :" + x[2]
        katagori =  "Katagori :" +x [3]
        waktu = "Jam Tayang :" + x[4]
        harga =  "Harga :" + x[5]
        data = (bioskop+" |=| "+judul+" |=| "+katagori+" |=| "+waktu+" |=| "+harga)
        bot.send_message(chat_id=call.message.chat.id,text= data)
                
    


# In[ ]:


if __name__ == "__main__":
    bot.polling(none_stop=True)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


#  mycursor = mydb.cursor()
# sql = "SELECT * FROM cinepolis WHERE tanggal=%s"
# adr = (parseTimeDatabase(), )
# mycursor.execute(sql, adr)
# myresult = mycursor.fetchall()

# output = ''
# for x in myresult:
#     bioskop = "Bioskop :" + x[1]
#     judul =  "Film :" + x[2]
#     katagori =  "Katagori :" +x [3]
#     waktu = "Jam Tayang :" + x[4]
#     harga =  "Harga :" + x[5]
#     data = (bioskop+" |=| "+judul+" |=| "+katagori+" |=| "+waktu+" |=| "+harga)

#     print (data)

