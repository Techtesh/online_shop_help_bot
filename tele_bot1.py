# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 17:37:43 2020

@author: Hitesh
"""
import Ama_DB_manager
import Ama_scrape_try2
from telegram import *
from telegram.ext import *
Bot_KEY="GET YOUR OWN"
bot=Bot(Bot_KEY)
keyword,chatid="",""
#print(bot.get_me())

updater=Updater(Bot_KEY,use_context=True)

dispatcher : Dispatcher =updater.dispatcher

def test1(update:Update , context:CallbackContext):
    keyword=update.message.text.lower()
    greetings=["hi","hello","good morning","good afternoon","good evening","hola"]
    if keyword in greetings:
        bot.sendMessage(chat_id=update.effective_chat.id, text="its a pleasure working for you",parse_mode=ParseMode.HTML)
    if keyword=="alert":
        data=Ama_DB_manager.alert_check()
        for d in data:
            msg,returnid=d
            bot.sendMessage(chat_id=returnid, text=msg,parse_mode=ParseMode.HTML)
            
        
    

def showOpts(update:Update , context:CallbackContext):
    #print("how may i help you today")
    global keyword,chatid
    try:
        keyword=update.message.text
        chatid=update.message.chat_id
    except:
        pass    
    keyboard =[[
        InlineKeyboardButton("get data on a product", callback_data="LINK"),
        InlineKeyboardButton("get data on a query", callback_data="NAME"),
        InlineKeyboardButton("set a Price Alert", callback_data="ALERT")
        ]]
    
    reply_markup=InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please Choose:", reply_markup=reply_markup)
    
def button_click(update:Update , context:CallbackContext):
    global keyword,chatid#new line
    
    query :CallbackQuery=update.callback_query
    
    
    #print("KEYWORD :==============>",keyword)
    if query.data=="LINK":
        name,price,prodid,_=Ama_scrape_try2.get_data_from_link(keyword)
        price=str(price)
        op="name of product is  "+name+"  is currently available for"+price
        if price=="9999999999":op="name of product is"+name+"it is currently unavailable"
        op="name of product is"+name+"it is currently available for"+price
        bot.sendMessage(chat_id=update.effective_chat.id, text=op,parse_mode=ParseMode.HTML)
    
    
    elif query.data=="NAME":
        lstoflinks=Ama_scrape_try2.get_links_from_name(keyword)
        for i,link in enumerate(lstoflinks):
            #print("Getting Page====>",link)
            name,price,prodid,src=Ama_scrape_try2.get_data_from_link(link)
            price=str(price)
            op=str(i)+")"+"name of product is  "+name+"  is currently available for"+price+"link to buy:  "+src
            if price!="9999999999":
                bot.sendMessage(chat_id=update.effective_chat.id, text=op,parse_mode=ParseMode.HTML)
            if i>8:
                break
    elif query.data=="ALERT":
        print(chatid)
        keys=keyword.split(" ")
        keys=[i for i in keys if len(i)>0]
        #print("NEWW :==============>",keys)
        link=keys[0]
        pricetarget=keys[1]
        name,price,prodid,_=Ama_scrape_try2.get_data_from_link(keyword)
        pricetarget=int(pricetarget)
        price=int(price)
        #print(pricetarget,price)
        
        
        if pricetarget>=price:op="You are already at target price for  "+name
        else:op="We will alert you when "+name+"is at or below "+str(pricetarget)
        
        bot.sendMessage(chat_id=update.effective_chat.id, text=op,parse_mode=ParseMode.HTML)
        data=(link,chatid,pricetarget)
        Ama_DB_manager.create_alerts(data)
        
        
    #dispatcher.add_handler(MessageHandler(Filters.text, test1))    
    
dispatcher.add_handler(MessageHandler(Filters.text, test1))
dispatcher.add_handler(MessageHandler(Filters.text, showOpts))
dispatcher.add_handler(CallbackQueryHandler( button_click))

#Ama_scrape_try2.quitdriver()
updater.start_polling()
