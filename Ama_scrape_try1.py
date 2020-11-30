# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 08:53:47 2020

@author: Hitesh
"""
import selenium
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def get_data_from_link(src):
    try:
        driver.get(src)
        try:
            name=driver.find_element_by_id("titleSection")#("productTitle")
        except:
            name=driver.find_element_by_id("productTitle")#("title_feature_div")
        #print(name.text)
        sale=1
        try:
            price=driver.find_element_by_id("priceblock_ourprice")
            
        except:
            sale=1
            try:
                price=driver.find_element_by_id("priceblock_saleprice")
            except:
                sale=0
                try:
                    price=driver.find_element_by_id("priceblock_dealprice")
                except:
                    price=9999999999
                    print("Unavailable")
        #print(price.text)
        cut1=src.find("/dp/")+4
        cut2=src.find("/ref")
        productid=src[cut1:cut2]
        try:
            price=price.text
            price=price[1:]
            price=price.split(",")
            price="".join(price)
            price=eval(price)
            price=int(price)
        except:
            pass
        
        return(name.text,price,productid,src)
    except:
        return("",0,"","")


chrome_options = Options()
chrome_options.add_argument("--headless")    
driver=webdriver.Chrome("C:/Users/Hitesh/Downloads/chromedriver",chrome_options=chrome_options)
