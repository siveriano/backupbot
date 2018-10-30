#!/usr/bin/python3
# -*- coding: utf-8 -*-
import telebot
from telebot import types
import datetime
from telegramcalendar import create_calendar

bot = telebot.TeleBot("262576272:AAH4_ojT5js4M-k4pmVarx-BUCUXMN4UUwQ")
current_shown_dates={}

@bot.message_handler(regexp="mamon")
def handle_messageExp(m):
    cid = m.chat.id
    bot.send_message(cid, "eso no se dice")
	

@bot.message_handler(commands=['wtf'])
def command_wtf(m):
    cid = m.chat.id
    cnombre = m.from_user.first_name
    bot.send_message(cid, cnombre +  " dijo What the fuck! ")

    
@bot.message_handler(commands=['repitecabron'])
def command_repite(m):
    cid = m.chat.id
    cnombre = m.from_user.first_name
    bot.send_message(cid, " Pa cabrona la madre de: " + cnombre )

@bot.message_handler(commands=['haha'])
def command_prueba(m):
    cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
    bot.send_photo( cid, open( 'roto2.jpg', 'rb')); # Con la función 'send_photo()'

@bot.message_handler(commands=['t_d_s_p_t_s'])
def command_todas(m):
    cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
    cnombre = m.from_user.first_name
    bot.send_message(cid, " Menos la madre de: " + cnombre )
    bot.send_photo( cid, open( 'putaTwitter.jpg', 'rb')); # Con la función 'send_photo()'
    bot.send_message(cid, " Pd: tu hermana si: " )

@bot.message_handler(commands=['calendar'])
def get_calendar(message):
    now = datetime.datetime.now() #Current date
    chat_id = message.chat.id
    date = (now.year,now.month)
    current_shown_dates[chat_id] = date #Saving the current date in a dict
    markup= create_calendar(now.year,now.month)
    bot.send_message(message.chat.id, "Please, choose a date", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data[0:13] == 'calendar-day-')
def get_day(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        day=call.data[13:]
        date = datetime.datetime(int(saved_date[0]),int(saved_date[1]),int(day),0,0,0)
        bot.send_message(chat_id, str(date))
        bot.answer_callback_query(call.id, text="")
        print (chat_id, str(date))
        
    else:
        #Do something to inform of the error
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'next-month')
def next_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month+=1
        if month>12:
            month=1
            year+=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
        """
        hola
        """
    else:
        #Do something to inform of the error
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'previous-month')
def previous_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month-=1
        if month<1:
            month=12
            year-=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        #Do something to inform of the error
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'ignore')
def ignore(call):
    bot.answer_callback_query(call.id, text="")



        
        
bot.polling(none_stop=True)