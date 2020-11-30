
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 14:47:18 2020

@author: Hitesh
"""
import Ama_DB_manager
import selenium
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options



def get_links_from_name(src):
    
    product="https://www.amazon.in/s?k="+("+".join(src.split(" ")))
    #print(product)
    
    driver.get(product)
    
    indexes=driver.find_elements_by_class_name("sg-col-inner")#("rush-component")
    
    alllinks=driver.find_elements_by_tag_name("a")
    alllinks=[i.get_attribute("href") for i in alllinks]
    alllinks3=[]
    for i in alllinks:
        try:
            if "/dp/"in i:
                alllinks3.append(i)
        except:
            pass
    alllinks3=tuple(set(alllinks3))
    alllinks3=[i for i in alllinks3]
    finallinks=[]
    for link in alllinks3 :
        cut1=link.index("/ref")
        link=link[:cut1]
        finallinks.append(link)
    finallinks=[i for i in tuple(set(finallinks))]
     
    return finallinks     
      
    
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
    pass

def quitdriver():
    driver.quit()

chrome_options = Options()
chrome_options.add_argument("--headless")    
driver=webdriver.Chrome("C:/Users/Hitesh/Downloads/chromedriver",chrome_options=chrome_options)


if __name__=="__main__":
    
    print("enter product name")
    src=input()#"OnePlus 8"#
    if "amazon.in" in src:
        data=get_data_from_link(src)
        print(data)
        _,p,_,_=data
        if p==0:
            print("error")
        else:
            Ama_DB_manager.new_data(data)
    else:
        links=get_links_from_name(src)
        #print(links)
        for i,link in enumerate(links):
            data=get_data_from_link(link)
            print("Data for DB=",i,"off",len(links),"==============",data)
            _,p,_,_=data
            if p==0:
                print("error")
            else:
                Ama_DB_manager.new_data(data)
            
            #Ama_DB_manager.new_data(data)
            
    driver.quit()
