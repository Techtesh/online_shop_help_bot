# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 14:47:18 2020

@author: Hitesh
"""
import Ama_scrape_try1# import get_data_from_link

import sqlite3
import datetime
def create_table():
    conn=sqlite3.connect("Amazon.db")
    c = conn.cursor()
    
    
    c.execute('''CREATE TABLE alerts
             (link,chatid,targetprice)''')
    print("table was created")
    conn.commit()
def new_data(data):
    conn=sqlite3.connect("Amazon.db")
    c = conn.cursor()
    
    
    
    data=(list(data))
    name,price,pid,link=data
    pids=c.execute('''SELECT pid FROM stocks''')
    #print(pids)
    ptype=[]
    for p in pids:
        p=list(p)
        ptype.append(p[0])
    #print(ptype)
    
    data.append(price)
    currDate = datetime.datetime.now()
    data.append(currDate)
    
    
    if pid in ptype:
        print("time to update")
        #print(pid)
        cp=pid
        try:
            prevLP=c.execute(''' SELECT lowprice FROM stocks where pid = :key ''',{"key":cp})
            for row in prevLP:
                prev=list(row)[0]
            #print(price,prev)
        except:
            #print("price error")
            prevLP=price
        if price<=(prev):
            newdata=(price,price,currDate)
            #print("new price")
            c.execute('''UPDATE stocks SET lowprice=:price ,currprice=:price2,time =:now WHERE pid=:key ''' ,{"price":price,"price2":price,"now":currDate,"key":cp})
            pass
        else:
            #print("oldprice")
            newdata=(price,currDate)
            c.execute('''UPDATE stocks SET currprice=:price ,time = :now  WHERE pid=:key''',{"price":price,"now":currDate,"key":cp})
            pass
    else:
        
        update=(name,price,currDate,pid,link,price)
        #print("new entry",update)
        c.execute('''INSERT into stocks VALUES(?,?,?,?,?,?) ''',update)
        
    
    conn.commit()
    #print(data)
    #c.execute("INSERT INTO stocks VALUES ")

def get_all_links():
    conn=sqlite3.connect("Amazon.db")
    c = conn.cursor()
    
    raw=c.execute(''' SELECT link FROM stocks ''')
    links=[]
    for row in raw:
        #print(row[0])
        links.append(row[0])
    print(links)

def create_alerts(data):
    conn=sqlite3.connect("Amazon.db")
    c = conn.cursor()
    
    link,price,targetprice=data
    price=int(price)
    update=(link,price,targetprice)
    print("new entry in alerts",update)
    cut1=link.find("/ref")
    link=link[:cut1]
    c.execute('''INSERT into alerts VALUES(?,?,?) ''',update)
    conn.commit()
    


def alert_check():
    conn=sqlite3.connect("Amazon.db")
    c = conn.cursor()
    links=[]
    chatids=[]
    targetprice=[]
    Base=c.execute("""SELECT * FROM alerts""")
    for row in Base:
        print(row)
        l,c,t=row
        links.append(l),chatids.append(c),targetprice.append(t)
    print(links)
    data=[]
    for c,tarP,link in zip(chatids,targetprice,links):
        name,currprice,_,_=Ama_scrape_try1.get_data_from_link(link)
        print(name,currprice,tarP)
        if tarP<=currprice or True:
            msg=name+"is currently available at "+str(currprice)+"  message sent as alert was set for  "+str(tarP)
            temp=(msg,c)
            data.append(temp)
            #print(msg+"  to  "+str(c))    
            
    return data

#alert_check()
#conn=sqlite3.connect("Amazon.db")
#c = conn.cursor()
#data=("one plus 7",21999,"B08877","amazon.in")
#new_data(data)
#get_all_links()
#create_table()

#c.execute(''' DROP Table Stocks''')
#conn.commit()