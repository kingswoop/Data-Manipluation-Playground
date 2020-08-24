import requests
import bs4
import csv
import pymongo
import pprint
from bson.objectid import ObjectId
import config
import re
from collections import defaultdict

#Declare List
productinfo = []
urlarray = []
crawlerarray = []

PRODUCTARRAY = []
FinalPList = []
difpriceproducts = []
samepriceproducts = []

errorproducts = []
errorcrawlers = []
errorcrawlerproducts = []
priceissues = []


def product_url():


    #####################################
    ########PRODUCT ARRAY FIELDS#########
    #   [0] = _ID of product            #
    #   [1] = URL of product            #
    #   [2] = Brand of product          #
    #   [3] = Price of product          #
    #   [4] = Sale Price of product     #
    #   [5] = CrawlerID for product     #
    #####################################
    
    #####FETCH PRODUCT DETAILS######
    client = pymongo.MongoClient('mongodb+srv://##Removedforsecurity?retryWrites=true&w=majority'.format(config.password), 27017)
    db = client['##Removedforsecurity']
    collection_products = db['##Removedforsecurity']
    
    #query = collection_products.find({"brand":"##insertbrand", "isDelete":"0"}, {"_id":1,"urlString":1,"brand":1,"price":1,"salePrice":1,"crawlerUrlId":1})
    query = collection_products.find({"isDelete":"0"}, {"_id":1,"urlString":1,"brand":1,"price":1,"salePrice":1,"crawlerUrlId":1})
    
    
    ######ONE LINE RESULT############
    #pprint.pprint(query["urlString"])
    
    
    ##COUNT OUTPUT FROM MONGODB###
    #results_count = query.count()
    #print(results_count)

    for x in query:
        productinfo = []
        productinfo.append(x["_id"])
        productinfo.append(x["urlString"])
        productinfo.append(x["brand"])
        productinfo.append(x["price"])
        productinfo.append(x["salePrice"])
        productinfo.append(x["crawlerUrlId"])
        urlarray.append(productinfo)
        
        
            
    #print(urlarray)

    #for i in query:
    #    for j in range(len(results_count)):
    #        productinfo[j].append(i["urlString"])
    #        productinfo[j].append(i["brand"])
        
    #print(productinfo)

        
    #with open('urloutput.csv', 'w', newline='') as file:
    #    writer = csv.writer(file)
    #    writer.writerows(urlarray)

def crawler_fetch():
    
    #####FETCH PRODUCT DETAILS######
    client = pymongo.MongoClient('mongodb+srv://##Removedforsecurity?retryWrites=true&w=majority'.format(config.password), 27017)
    db = client['##Removedforsecurity']
    collection_products = db['##Removedforsecurity']
    
    #query = collection_products.aggregate([{"$match": {"configName": "##insertconfigname"}},{"$group" :{"_id":"$_id","htmlTagReference" :{"$push" : {"$arrayElemAt": ["$crawlerHTMLTag.htmlTagReference", 2]}},"htmlTagReference1" :{"$push" : {"$arrayElemAt": ["$crawlerHTMLTag.htmlTagReference", 3]}},"htmlAttributeReference" :{"$push" : {"$arrayElemAt": ["$crawlerHTMLTag.htmlAttributeReference", 2]}},"htmlAttributeReference1" :{"$push" : {"$arrayElemAt": ["$crawlerHTMLTag.htmlAttributeReference", 3]}}}},{ "$project": {"items": { "$concatArrays": ["$htmlTagReference", "$htmlTagReference1", "$htmlAttributeReference", "$htmlAttributeReference1"] }}}])
    #query = collection_products.aggregate([{"$match": {"configName": { "$regex": "insertbrandname" }}},{"$group" :{"_id":"$_id","htmlTagReference" :{"$push" : {"$arrayElemAt": ["$crawlerHTMLTag.htmlTagReference", 2]}},"htmlTagReference1" :{"$push" : {"$arrayElemAt": ["$crawlerHTMLTag.htmlTagReference", 3]}},"htmlAttributeReference" :{"$push" : {"$arrayElemAt": ["$crawlerHTMLTag.htmlAttributeReference", 2]}},"htmlAttributeReference1" :{"$push" : {"$arrayElemAt": ["$crawlerHTMLTag.htmlAttributeReference", 3]}}}},{ "$project": {"items": { "$concatArrays": ["$htmlTagReference", "$htmlTagReference1", "$htmlAttributeReference", "$htmlAttributeReference1"] }}}])
    query = collection_products.aggregate([{"$group" :{"_id":"$_id","htmlTagReference" :{"$push" : {"$arrayElemAt": ["$crawlerHTMLTag.htmlTagReference", 2]}},"htmlTagReference1" :{"$push" : {"$arrayElemAt": ["$crawlerHTMLTag.htmlTagReference", 3]}},"htmlAttributeReference" :{"$push" : {"$arrayElemAt": ["$crawlerHTMLTag.htmlAttributeReference", 2]}},"htmlAttributeReference1" :{"$push" : {"$arrayElemAt": ["$crawlerHTMLTag.htmlAttributeReference", 3]}}}},{ "$project": {"items": { "$concatArrays": ["$htmlTagReference", "$htmlTagReference1", "$htmlAttributeReference", "$htmlAttributeReference1"] }}}])


    ###PRINT ONE RESULT
    #for x in query:
    #    print(x)
    
    crawler_config_count = 0
    
    for x in query:
        crawlerset = []
        crawlerinfo = []
        crawlerid = []
        crawlerid.append(x["_id"])
        crawlerinfo.append(x["items"][0])
        crawlerinfo.append(x["items"][1])
        
        ######################################
        ##   ASSIGN FIRST HTML ATT TO LIST  ##
        ######################################
        htmlat1 = x["items"][2]
        #print('Attribute 1 = ' + str(htmlat1))
        if htmlat1 == 0:
            htmlat1 = str(htmlat1).replace(str(htmlat1), '')
            #print('CHANGED - ' + htmlat1)
            crawlerinfo.append(htmlat1)
        elif htmlat1 == 1:
            htmlat1 = str(htmlat1).replace(str(htmlat1), 'Class')
            #print('CHANGED - ' + htmlat1)
            crawlerinfo.append(htmlat1)
        elif htmlat1 == 2:
            htmlat1 = str(htmlat1).replace(str(htmlat1), 'Class;Tag')
            #print('CHANGED - ' + htmlat1)
            crawlerinfo.append(htmlat1)
        elif htmlat1 == 3:
            htmlat1 = str(htmlat1).replace(str(htmlat1), '')
            #print('CHANGED - ' + htmlat1)
            crawlerinfo.append(htmlat1)
        elif htmlat1 == 4:
            htmlat1 = str(htmlat1).replace(str(htmlat1), 'Class;Class')
            #print('CHANGED - ' + htmlat1)
            crawlerinfo.append(htmlat1)
        elif htmlat1 == 5:
            htmlat1 = str(htmlat1).replace(str(htmlat1), 'Id')
            #print('CHANGED - ' + htmlat1)
            crawlerinfo.append(htmlat1)
        elif htmlat1 == 6:
            htmlat1 = str(htmlat1).replace(str(htmlat1), 'Id;Tag')
            #print('CHANGED - ' + htmlat1)
            crawlerinfo.append(htmlat1)
        elif htmlat1 == 7:
            htmlat1 = str(htmlat1).replace(str(htmlat1), 'Id;Class')
            #print('CHANGED - ' + htmlat1)
            crawlerinfo.append(htmlat1)
        elif htmlat1 == 8:
            htmlat1 = str(htmlat1).replace(str(htmlat1), 'Attribute')
            #print('CHANGED - ' + htmlat1)
            crawlerinfo.append(htmlat1)
        elif htmlat1 == 9:
            htmlat1 = str(htmlat1).replace(str(htmlat1), 'Attribute;Value')
            #print('CHANGED - ' + htmlat1)
            crawlerinfo.append(htmlat1)
        elif htmlat1 == 10:
            htmlat1 = str(htmlat1).replace(str(htmlat1), 'Attribute;Value;Tag')
            #print('CHANGED - ' + htmlat1)
            crawlerinfo.append(htmlat1)
        elif htmlat1 == 11:
            htmlat1 = str(htmlat1).replace(str(htmlat1), '')
            #print('CHANGED - ' + htmlat1)
            crawlerinfo.append(htmlat1)
        elif htmlat1 == 12:
            htmlat1 = str(htmlat1).replace(str(htmlat1), 'ParentClass;ChildTagAttribute')
            #print('CHANGED - ' + htmlat1)
            crawlerinfo.append(htmlat1)
        elif htmlat1 == 13:
            htmlat1 = str(htmlat1).replace(str(htmlat1), '')
            #print('CHANGED - ' + htmlat1)
            crawlerinfo.append(htmlat1)
        elif htmlat1 == 14:
            htmlat1 = str(htmlat1).replace(str(htmlat1), 'Attribute;Value;Attribute')
            #print('CHANGED - ' + htmlat1)
            crawlerinfo.append(htmlat1)
        
        
        ######################################
        ##  ASSIGN SECOND HTML ATT TO LIST  ##
        ######################################
        htmlat2 = x["items"][3]
        #print('Attribute 2 = ' + str(htmlat2))
        if htmlat2 == 0:
            htmlat2 = str(htmlat2).replace(str(htmlat2), '')
            #print('CHANGED - ' + htmlat2)
            crawlerinfo.append(htmlat2)
        elif htmlat2 == 1:
            htmlat2 = str(htmlat2).replace(str(htmlat2), 'Class')
            #print('CHANGED - ' + htmlat2)
            crawlerinfo.append(htmlat2)
        elif htmlat2 == 2:
            htmlat2 = str(htmlat2).replace(str(htmlat2), 'Class;Tag')
            #print('CHANGED - ' + htmlat2)
            crawlerinfo.append(htmlat2)
        elif htmlat2 == 3:
            htmlat2 = str(htmlat2).replace(str(htmlat2), '')
            #print('CHANGED - ' + htmlat2)
            crawlerinfo.append(htmlat2)
        elif htmlat2 == 4:
            htmlat2 = str(htmlat2).replace(str(htmlat2), 'Class;Class')
            #print('CHANGED - ' + htmlat2)
            crawlerinfo.append(htmlat2)
        elif htmlat2 == 5:
            htmlat2 = str(htmlat2).replace(str(htmlat2), 'Id')
            #print('CHANGED - ' + htmlat2)
            crawlerinfo.append(htmlat2)
        elif htmlat2 == 6:
            htmlat2 = str(htmlat2).replace(str(htmlat2), 'Id;Tag')
            #print('CHANGED - ' + htmlat2)
            crawlerinfo.append(htmlat2)
        elif htmlat2 == 7:
            htmlat2 = str(htmlat2).replace(str(htmlat2), 'Id;Class')
            #print('CHANGED - ' + htmlat2)
            crawlerinfo.append(htmlat2)
        elif htmlat2 == 8:
            htmlat2 = str(htmlat2).replace(str(htmlat2), 'Attribute')
            #print('CHANGED - ' + htmlat2)
            crawlerinfo.append(htmlat2)
        elif htmlat2 == 9:
            htmlat2 = str(htmlat2).replace(str(htmlat2), 'Attribute;Value')
            #print('CHANGED - ' + htmlat2)
            crawlerinfo.append(htmlat2)
        elif htmlat2 == 10:
            htmlat2 = str(htmlat2).replace(str(htmlat2), 'Attribute;Value;Tag')
            #print('CHANGED - ' + htmlat2)
            crawlerinfo.append(htmlat2)
        elif htmlat2 == 11:
            htmlat2 = str(htmlat2).replace(str(htmlat2), '')
            #print('CHANGED - ' + htmlat2)
            crawlerinfo.append(htmlat2)
        elif htmlat2 == 12:
            htmlat2 = str(htmlat2).replace(str(htmlat2), 'ParentClass;ChildTagAttribute')
            #print('CHANGED - ' + htmlat2)
            crawlerinfo.append(htmlat2)
        elif htmlat2 == 13:
            htmlat2 = str(htmlat2).replace(str(htmlat2), '')
            #print('CHANGED - ' + htmlat2)
            crawlerinfo.append(htmlat2)
        elif htmlat2 == 14:
            htmlat2 = str(htmlat2).replace(str(htmlat2), 'Attribute;Value;Attribute')
            #print('CHANGED - ' + htmlat2)
            crawlerinfo.append(htmlat2)
            
        ### append crawler info the crawler array####
        crawlerset.append(crawlerid)
        crawlerset.append(crawlerinfo)
        crawlerarray.append(crawlerset)
        crawler_config_count += 1
        
        
    ######################################
    ##        PRINT COUNT OF CRAWLS     ##
    ######################################
    print("#####################################################")
    print("TOTAL CRAWLS FETCHED: " + str(crawler_config_count))
    



def fullstring():
    
    #NEW
    #####################################
    ########PRODUCT ARRAY FIELDS#########
    #   [0] = _ID of product            #
    #   [1] = PRICE HTML FIELD          #
    #   [2] = SALE PRICE HTML FIELD     #
    #   [3] = PRICE ATT                 #
    #   [4] = Sale Price ATT            #
    #   [5] = PRODUCT URL               #
    #   [6] = PRODUCT BRAND             #
    #   [7] = Product Price in DB       #
    #   [8] = Product Sale Price in DB  #
    #   [9] = PRODUCT Crwaler ID        #
    #####################################
    
    fullstring_count = 0
    
    
    ######################################
    ##  DICTIONARY of crawler config    ##
    ######################################
    crawlerDict = dict()
    for line in crawlerarray:
        crawltuple = (line[0] + line[1])
        if crawltuple[0] in crawlerDict:
            continue
            print("Crawler Config (Key) already exists")
        else:

            crawlerDict[crawltuple[0]] = [crawltuple[1]]
            crawlerDict[crawltuple[0]].append(crawltuple[2])
            crawlerDict[crawltuple[0]].append(crawltuple[3])
            crawlerDict[crawltuple[0]].append(crawltuple[4])

    ######################################
    ##     Combine product + crawler    ##
    ######################################
    for key, v1, v2, v3, v4, v5 in urlarray:
        try:
            PCarray = []
            keyobject = (ObjectId(str(v5)))
            crawlervalues = crawlerDict.get(keyobject)
            PCarray.append(keyobject)
            if crawlervalues is not None:
                for j in range(len(crawlervalues)):
                    try:
                        PCarray.append(crawlervalues[j])
                    except LenError:
                        continue
            else:
                continue
            PCarray.append(v1)
            PCarray.append(v2)
            PCarray.append(v3)
            PCarray.append(v4)
            PCarray.append(v5)
            fullstring_count += 1
            PRODUCTARRAY.append(PCarray)
        except KeyError:
            continue  
            
            
    ######################################
    ##      PRINT COUNT OF PRODUCTS     ##
    ######################################        
    print("TOTAL NUMBER OF PRODUCTS FETCHED: " + str(fullstring_count))
    print("#####################################################")
    
    

def pricepull():
    
    #NEW
    #####################################
    ########PRODUCT ARRAY FIELDS#########
    #   [0] = _ID of product            #
    #   [1] = PRICE HTML FIELD          #
    #   [2] = SALE PRICE HTML FIELD     #
    #   [3] = PRICE ATT                 #
    #   [4] = Sale Price ATT            #
    #   [5] = PRODUCT URL               #
    #   [6] = PRODUCT BRAND             #
    #   [7] = Product Price in DB       #
    #   [8] = Product Sale Price in DB  #
    #   [9] = PRODUCT Crwaler ID        #
    #####################################

    for url in range(len(PRODUCTARRAY)):
        res = requests.get(PRODUCTARRAY[url][5])
        res.text
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        
        ######################################
        ##       ASSIGN HTML ATTRIBUT       ##
        ######################################
        htmla=PRODUCTARRAY[url][3]
        htmla1=PRODUCTARRAY[url][4]
        priceatt1=PRODUCTARRAY[url][1]
        priceatt2=PRODUCTARRAY[url][2]
        print(htmla)
        print(htmla1)
        print(priceatt1)
        print(priceatt2)
        
        
        ######################################
        ##       DECLARE REMOVAL HTML       ##
        ######################################
        htmlPhraseDelete = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']
        
        
        ######################################
        ##    CHECK IF SALES CONFIG EXIST   ##
        ######################################
        print(PRODUCTARRAY[url][5])
        if htmla1 is None or htmla1 == "" or htmla1 == " ":
            price = ""
            saleprice = ""
            try:
                if htmla == 'Class':
                    price = soup.find_all(class_=priceatt1)
                    for x in range(len(price)):
                        price = list( dict.fromkeys(price))
                    for x in range(len(htmlPhraseDelete)):
                        price = str(price).replace(htmlPhraseDelete[x], '')
                    price = re.sub('[^0-9,.]', '', str(price))
                    if "," in price:
                        pricesplit = price.split(',')
                        price = pricesplit[0]
                        saleprice = pricesplit[1]
                    if saleprice == "" or saleprice == " " or saleprice > "0":
                        saleprice = "0"
                    

                elif htmla == 'Class;Tag':
                    if ";" in priceatt1:
                        priceatt1split = priceatt1.split(';')
                        htmlasplit1 = priceatt1split[0]
                        htmlasplit2 = priceatt1split[1]
                        price = soup.find(id=htmlasplit1).find(htmlasplit2)
                        for x in range(len(htmlPhraseDelete)):
                            price = str(price).replace(htmlPhraseDelete[x], '')
                        for x in range(len(price)):
                            price = list( dict.fromkeys(price))
                            price = re.sub('[^0-9,.]', '', str(price))
                            if "," in price:
                                pricesplit = price.split(',')
                                price = pricesplit[0]
                                saleprice = pricesplit[1]
                            if saleprice == "" or saleprice == " " or saleprice > "0":
                                saleprice = "0"
                            

                elif htmla == 'Class;Class':
                    if ";" in priceatt1:
                        priceatt1split = priceatt1.split(';')
                        htmlasplit1 = priceatt1split[0]
                        htmlasplit2 = priceatt1split[1]
                        price = soup.find(class_=htmlasplit1).find(class_=htmlasplit2)
                        for x in range(len(htmlPhraseDelete)):
                            price = str(price).replace(htmlPhraseDelete[x], '')
                        print(price)
                        price = re.sub('[^0-9],.', ' ', str(price))
                        #print(price)
                        price = re.sub("\s+", ",", price.strip())
                        if "," in price:
                            pricesplit = price.split(',')
                            price = pricesplit[0]
                            saleprice = pricesplit[1]
                        if saleprice == "" or saleprice == " " or saleprice > "0":
                            saleprice = "0"
                        #print(price)
                        print('$$$$$$')
                            
                        
                    
                elif htmla == 'Id':
                    price = soup.find(id=priceatt1).text
                    for x in range(len(htmlPhraseDelete)):
                        price = str(price).replace(htmlPhraseDelete[x], '')
                    for x in range(len(price)):
                        price = list( dict.fromkeys(price))
                        price = re.sub('[^0-9,.]', '', str(price))
                        if "," in price:
                            pricesplit = price.split(',')
                            price = pricesplit[0]
                            saleprice = pricesplit[1]
                        if saleprice == "" or saleprice == " " or saleprice > "0":
                            saleprice = "0"
                
                elif htmla == 'Id;Tag':
                    if ";" in priceatt1:
                        priceatt1split = priceatt1.split(';')
                        htmlasplit1 = priceatt1split[0]
                        htmlasplit2 = priceatt1split[1]
                        price = soup.find(id=htmlasplit1).find_all(htmlasplit2)
                        for x in range(len(htmlPhraseDelete)):
                            price = str(price).replace(htmlPhraseDelete[x], '')
                        for x in range(len(price)):
                            price = list( dict.fromkeys(price))
                            price = re.sub('[^0-9,.]', '', str(price))
                            if "," in price:
                                pricesplit = price.split(',')
                                price = pricesplit[0]
                                saleprice = pricesplit[1]
                            if saleprice == "" or saleprice == " " or saleprice > "0":
                                saleprice = "0"
                
                elif htmla == 'Id;Class':
                    if ";" in priceatt1:
                        priceatt1split = priceatt1.split(';')
                        htmlasplit1 = str(priceatt1split[0])
                        htmlasplit2 = str(priceatt1split[1])
                        price = soup.find(id=htmlasplit1).find_all(class_=htmlasplit2)
                        for x in range(len(htmlPhraseDelete)):
                            price = str(price).replace(htmlPhraseDelete[x], '')
                        price = re.sub('[^0-9,.]', '', str(price))
                        i = price.find(".") + 3 
                        price = (f"{price[:i]},{price[i:]}")
                        if "," in price:
                            pricesplit = price.split(',')
                            price = pricesplit[0]
                            saleprice = pricesplit[1]
                        if saleprice == "" or saleprice == " " or saleprice > "0":
                            saleprice = "0"
                                   
                elif htmla == 'Attribute':
                    price = soup.find_all(attrs={priceatt1:True})
                    for x in range(len(price)):
                        price = list( dict.fromkeys(price))
                    for x in range(len(htmlPhraseDelete)):
                        price = str(price).replace(htmlPhraseDelete[x], '')
                    price = re.sub('[^0-9,.]', '', str(price))
                    for x in range(len(price)):
                        price = list( dict.fromkeys(price))
                        price = re.sub('[^0-9,.]', '', str(price))
                        if "," in price:
                            pricesplit = price.split(',')
                            price = pricesplit[0]
                            saleprice = pricesplit[1]
                        if saleprice == "" or saleprice == " " or saleprice > "0":
                            saleprice = "0"
                    
                elif htmla == 'Attribute;Value':
                    if ";" in priceatt1:
                        priceatt1split = priceatt1.split(';')
                        htmlasplit1 = priceatt1split[0]
                        htmlasplit2 = priceatt1split[1]
                        price = soup.find_all(attrs={htmlasplit1:htmlasplit2})
                        for x in range(len(htmlPhraseDelete)):
                            price = str(price).replace(htmlPhraseDelete[x], '')
                        price = list( dict.fromkeys(price))
                        soup = bs4.BeautifulSoup(str(price), 'lxml')
                        price = re.sub('[^0-9,.]', '', str(price))
                        if "," in price:
                            pricesplit = price.split(',')
                            price = pricesplit[0]
                            saleprice = pricesplit[1]
                        if saleprice == "" or saleprice == " " or saleprice > "0":
                            saleprice = "0"
                    
                elif htmla == 'Attribute;Value;Tag':
                    if ";" in priceatt1:
                        priceatt1split = priceatt1.split(';')
                        htmlasplit1 = priceatt1split[0]
                        htmlasplit2 = priceatt1split[1]
                        htmlasplit3 = priceatt1split[2]
                        price = soup.find_all(attrs={htmlasplit1:htmlasplit2})
                        for x in range(len(price)):
                            price = soup.find(htmlasplit3)
                            price = list( dict.fromkeys(price))
                            soup = bs4.BeautifulSoup(str(price), 'lxml')
                            price = re.sub('[^0-9,.]', '', str(price)) 
                            if "," in price:
                                pricesplit = price.split(',')
                                price = pricesplit[0]
                                saleprice = pricesplit[1]
                            if saleprice == "" or saleprice == " " or saleprice > "0":
                                saleprice = "0"
                
                elif htmla == 'ParentClass;ChildTagAttribute':
                    err = []
                    err.append('ParentClass;ChildTagAttribute Error')
                    err.append(PRODUCTARRAY[url][0])
                    err.append(PRODUCTARRAY[url][5])
                    err.append(PRODUCTARRAY[url][3])
                    err.append(PRODUCTARRAY[url][4])
                    errorproducts.append(err)     
                    
                elif htmla == 'Attribute;Value;Attribute':
                    if ";" in priceatt1:
                        priceatt1split = priceatt1.split(';')
                        htmlasplit1 = priceatt1split[0]
                        htmlasplit2 = priceatt1split[1]
                        price = soup.find_all(attrs={htmlasplit1:htmlasplit2})
                        for x in range(len(price)):
                            price = list( dict.fromkeys(price))
                            soup = bs4.BeautifulSoup(str(price), 'lxml')
                            price = re.sub('[^0-9,.]', '', str(price))
                            if "," in price:
                                pricesplit = price.split(',')
                                price = pricesplit[0]
                                saleprice = pricesplit[1]
                            if saleprice == "" or saleprice == " " or saleprice > "0":
                                saleprice = "0"
                        
                        
                        
       
            except ValueError:
                err = []
                err.append('SOLO CONFIG Price Config Error')
                err.append(PRODUCTARRAY[url][0])
                err.append(PRODUCTARRAY[url][5])
                err.append(PRODUCTARRAY[url][3])
                err.append(PRODUCTARRAY[url][4])
                errorproducts.append(err)     
                print("Could not fetch data")
        
        
        
        else:
            ######################################
            ##           PRICE FETCH            ##
            ######################################
            price = ""
            try:
                if htmla == 'Class':
                    price = soup.find(class_=priceatt1)
                    for x in range(len(htmlPhraseDelete)):
                        price = str(price).replace(htmlPhraseDelete[x], '')

                elif htmla == 'Class;Tag':
                    if ";" in priceatt1:
                        priceatt1split = priceatt1.split(';')
                        htmlasplit1 = priceatt1split[0]
                        htmlasplit2 = priceatt1split[1]
                        price = soup.find(id=htmlasplit1).find(htmlasplit2).text
                        
                        

                elif htmla == 'Class;Class':
                    if ";" in priceatt1:
                        priceatt1split = priceatt1.split(';')
                        htmlasplit1 = priceatt1split[0]
                        htmlasplit2 = priceatt1split[1]
                        price = soup.find(class_=htmlasplit1).find(class_=htmlasplit2)
                        for x in range(len(htmlPhraseDelete)):
                            price = str(price).replace(htmlPhraseDelete[x], '')
                        price = re.sub('[^0-9,.]', '', str(price))
                        print('^^^^^^')
                        
                    
                elif htmla == 'Id':
                    price = soup.find(id=priceatt1).text
                
                elif htmla == 'Id;Tag':
                    if ";" in priceatt1:
                        priceatt1split = priceatt1.split(';')
                        htmlasplit1 = priceatt1split[0]
                        htmlasplit2 = priceatt1split[1]
                        price = soup.find(id=htmlasplit1).find_all(htmlasplit2)
                
                elif htmla == 'Id;Class':
                    if ";" in priceatt1:
                        priceatt1split = priceatt1.split(';')
                        htmlasplit1 = priceatt1split[0]
                        htmlasplit2 = priceatt1split[1]
                        price = soup.find(id=htmlasplit1).find_all(class_=htmlasplit2)
                        for x in range(len(htmlPhraseDelete)):
                            price = str(price).replace(htmlPhraseDelete[x], '')
                        price = re.sub('[^0-9,.]', '', str(price))
                        
                                   
                elif htmla == 'Attribute':
                    price = soup.find_all(attrs={htmla:True})
                    for x in range(len(price)):
                        price = list( dict.fromkeys(price))
                    price = re.sub('[^0-9,.]', '', str(price))
                    
                elif htmla == 'Attribute;Value':
                    if ";" in priceatt1:
                        priceatt1split = priceatt1.split(';')
                        htmlasplit1 = priceatt1split[0]
                        htmlasplit2 = priceatt1split[1]
                        price = soup.find_all(attrs={htmlasplit1:htmlasplit2})
                        price = list( dict.fromkeys(price))
                        soup = bs4.BeautifulSoup(str(price), 'lxml')
                        price = re.sub('[^0-9,.]', '', str(price))               
                    
                elif htmla == 'Attribute;Value;Tag':
                    if ";" in priceatt1:
                        priceatt1split = priceatt1.split(';')
                        htmlasplit1 = priceatt1split[0]
                        htmlasplit2 = priceatt1split[1]
                        htmlasplit3 = priceatt1split[2]
                        price = soup.find_all(attrs={htmlasplit1:htmlasplit2})
                        for x in range(len(price)):
                            price = soup.find(htmlasplit3)
                            price = list( dict.fromkeys(price))
                            soup = bs4.BeautifulSoup(str(price), 'lxml')
                            price = re.sub('[^0-9,.]', '', str(price))
                
                elif htmla == 'ParentClass;ChildTagAttribute':
                    err = []
                    err.append('ParentClass;ChildTagAttribute Error')
                    err.append(PRODUCTARRAY[url][0])
                    err.append(PRODUCTARRAY[url][1])
                    err.append(PRODUCTARRAY[url][7])
                    err.append(PRODUCTARRAY[url][8])
                    err.append(PRODUCTARRAY[url][9])
                    err.append(PRODUCTARRAY[url][10])
                    errorproducts.append(err)     
                    
                elif htmla == 'Attribute;Value;Attribute':
                    if ";" in priceatt1:
                        priceatt1split = priceatt1.split(';')
                        htmlasplit1 = priceatt1split[0]
                        htmlasplit2 = priceatt1split[1]
                        price = soup.find_all(attrs={htmlasplit1:htmlasplit2})
                        for x in range(len(price)):
                            price = list( dict.fromkeys(price))
                            soup = bs4.BeautifulSoup(str(price), 'lxml')
                            price = re.sub('[^0-9,.]', '', str(price))
                        
       
            except ValueError:
                err = []
                err.append('Price Config Error')
                err.append(PRODUCTARRAY[url][0])
                err.append(PRODUCTARRAY[url][5])
                err.append(PRODUCTARRAY[url][3])
                err.append(PRODUCTARRAY[url][4])
                errorproducts.append(err)     
                print("Could not fetch data")
                
            ######################################
            ##        SALES PRICE FETCH         ##
            ######################################
            saleprice = ""
            try:
                if htmla1 == 'Class':
                    saleprice = soup.find(class_=priceatt2)
                    if str(saleprice) == "" or str(saleprice) == " " or str(saleprice) > "0":
                        saleprice = "0"

                elif htmla1 == 'Class;Tag':
                    if ";" in priceatt2:
                        priceatt2split = priceatt2.split(';')
                        htmlasplit1 = priceatt2split[0]
                        htmlasplit2 = priceatt2split[1]
                        saleprice = soup.find(id=htmlasplit1).find(htmlasplit2).text
                        if str(saleprice) == "" or str(saleprice) == " " or str(saleprice) > "0":
                            saleprice = "0"

                elif htmla1 == 'Class;Class':
                    if ";" in priceatt2:
                        priceatt1split = priceatt2.split(';')
                        htmlasplit1 = priceatt1split[0]
                        htmlasplit2 = priceatt1split[1]
                        saleprice = soup.find(class_=htmlasplit1).find(class_=htmlasplit2)
                        for x in range(len(htmlPhraseDelete)):
                            saleprice = str(saleprice).replace(htmlPhraseDelete[x], '')
                        saleprice = re.sub('[^0-9,.]', '', str(saleprice))
                        if str(saleprice) == "" or str(saleprice) == " " or str(saleprice) > "0":
                            saleprice = "0"
                        print('-------')
                            
                elif htmla1 == 'Id':
                    saleprice = soup.find(id=priceatt2).text
                    if str(saleprice) == "" or str(saleprice) == " " or str(saleprice) > "0":
                        saleprice = "0"
                
                elif htmla1 == 'Id;Tag':
                    if ";" in priceatt2:
                        priceatt2split = priceatt2.split(';')
                        htmlasplit1 = priceatt2split[0]
                        htmlasplit2 = priceatt2split[1]
                        saleprice = soup.find(id=htmlasplit1).find_all(htmlasplit2)
                        if saleprice == "" or saleprice == " " or saleprice > "0":
                            saleprice = "0"
                
                elif htmla1 == 'Id;Class':
                    if ";" in priceatt1:
                        priceatt1split = priceatt1.split(';')
                        htmlasplit1 = priceatt1split[0]
                        htmlasplit2 = priceatt1split[1]
                        saleprice = soup.find(id=htmlasplit1).find_all(class_=htmlasplit2)
                        for x in range(len(htmlPhraseDelete)):
                            saleprice = str(saleprice).replace(htmlPhraseDelete[x], '')
                        saleprice = re.sub('[^0-9,.]', '', str(saleprice))
                        if str(saleprice) == "" or str(saleprice) == " " or str(saleprice) > "0":
                            saleprice = "0"
                                   
                elif htmla1 == 'Attribute':
                    saleprice = soup.find_all(attrs={priceatt2:True})
                    for x in range(len(saleprice)):
                        saleprice = list( dict.fromkeys(saleprice))
                    saleprice = re.sub('[^0-9,.]', '', str(saleprice))
                    if str(saleprice) == "" or str(saleprice) == " " or str(saleprice) > "0":
                            saleprice = "0"
                    
                elif htmla1 == 'Attribute;Value':
                    if ";" in priceatt2:
                        priceatt2split = priceatt2.split(';')
                        htmlasplit1 = priceatt2split[0]
                        htmlasplit2 = priceatt2split[1]
                        saleprice = soup.find_all(attrs={htmlasplit1:htmlasplit2})
                        saleprice = list( dict.fromkeys(saleprice))
                        soup = bs4.BeautifulSoup(str(saleprice), 'lxml')
                        saleprice = re.sub('[^0-9,.]', '', str(saleprice))
                        if str(saleprice) == "" or str(saleprice) == " " or str(saleprice) > "0":
                            saleprice = "0"
                        
                    
                elif htmla1 == 'Attribute;Value;Tag':
                    if ";" in priceatt2:
                        priceatt2split = priceatt2.split(';')
                        htmlasplit1 = priceatt2split[0]
                        htmlasplit2 = priceatt2split[1]
                        htmlasplit3 = priceatt2split[2]
                        saleprice = soup.find_all(attrs={htmlasplit1:htmlasplit2})
                        for x in range(len(saleprice)):
                            saleprice = soup.find(htmlasplit3)
                            saleprice = list( dict.fromkeys(saleprice))
                            soup = bs4.BeautifulSoup(str(saleprice), 'lxml')
                            saleprice = re.sub('[^0-9,.]', '', str(saleprice))
                            if str(saleprice) == "" or str(saleprice) == " " or str(saleprice) > "0":
                                saleprice = "0"
                
                elif htmla1 == 'ParentClass;ChildTagAttribute':
                    err = []
                    err.append('ParentClass;ChildTagAttribute Error')
                    err.append(PRODUCTARRAY[url][0])
                    err.append(PRODUCTARRAY[url][1])
                    err.append(PRODUCTARRAY[url][7])
                    err.append(PRODUCTARRAY[url][8])
                    err.append(PRODUCTARRAY[url][9])
                    err.append(PRODUCTARRAY[url][10])
                    errorproducts.append(err)     
                    
                elif htmla1 == 'Attribute;Value;Attribute':
                    if ";" in priceatt2:
                        priceatt2split = priceatt2.split(';')
                        htmlasplit1 = priceatt2split[0]
                        htmlasplit2 = priceatt2split[1]
                        saleprice = soup.find_all(attrs={htmlasplit1:htmlasplit2})
                        for x in range(len(saleprice)):
                            saleprice = list( dict.fromkeys(saleprice))
                            soup = bs4.BeautifulSoup(str(saleprice), 'lxml')
                            saleprice = re.sub('[^0-9,.]', '', str(saleprice))
                            if str(saleprice) == "" or str(saleprice) == " " or str(saleprice) > "0":
                                saleprice = "0"
                        
       
            except ValueError:
                err = []
                err.append('saleprice Config Error')
                err.append(PRODUCTARRAY[url][0])
                err.append(PRODUCTARRAY[url][5])
                err.append(PRODUCTARRAY[url][3])
                err.append(PRODUCTARRAY[url][4])
                errorproducts.append(err)     
                print("Could not fetch data")
            
            
        
        #######################################
        ## WRITE PRODUCT POLL ERRORS TO FILE ##
        #######################################
        with open('errors.csv','w') as error_file:
                wr = csv.writer(error_file, dialect='excel')
                for a in range(len(errorproducts)):
                    wr.writerow(errorproducts[a])
        
        

        ######################################
        ##    REMOVE SYMBOLS FROM PRICES    ##
        ######################################
        b = "AUD$USDGBP"
        try:
            for char in b:
                price = price.replace(char,"")
                saleprice = saleprice.replace(char,"")
        except: 
            continue
            
        price = price.strip()
        saleprice = saleprice.strip()
        
        
        
        ######################################
        ##        CHECK FOR 0 Value         ##
        ######################################
        if str(price) == '' or str(price) == '0' or str(price) == '0.0' or str(price) == '0.00':
            price = '0.0'
        if str(saleprice) == '' or str(saleprice) == '0' or str(saleprice) == '0.0' or  str(saleprice) == '0.00':
            saleprice = '0.0'
            
        print(price)
        print(saleprice)
        
        
        ######################################
        ##       PRICE POSITIONING          ##
        ######################################
        if price < saleprice:
            varprice = price
            varsaleprice = saleprice
            saleprice = varprice
            price = varsaleprice
            
            
        ######################################
        ##  CONVERT STRING TO FLOAT INT's   ##
        ######################################
        try:
            price = float(price)
            saleprice = float(saleprice)
        except:
            continue
        

        
        
        #####################################
        #######FinalPList ARRAY FIELDS#######
        #   [0] = _ID of product            #
        #   [1] = Fetch Price               #
        #   [2] = Fetch SalePrice           #
        #   [3] = Price on                  #
        #   [4] = Sale Price                #
        #   [5] = PRODUCT URL               #
        #####################################
        fetchprices = []
        fetchprices.append(PRODUCTARRAY[url][0])
        fetchprices.append(price)
        fetchprices.append(saleprice)
        fetchprices.append(PRODUCTARRAY[url][7])
        fetchprices.append(PRODUCTARRAY[url][8])
        fetchprices.append(PRODUCTARRAY[url][5])
        print(fetchprices)

        FinalPList.append(fetchprices)  


        
    ######################################
    ##      WRITE TO FILE FOR RECORD    ##
    ######################################
    with open('output.csv','w') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        for m in range(len(FinalPList)):
            wr.writerow(FinalPList[m])

    


def outcome():
        
    
    
    for t in range(len(FinalPList)):
        pricecomparison = []
        pissues = []
        
        if FinalPList[t][1] != FinalPList[t][3] or FinalPList[t][2] != FinalPList[t][4]:
            pricecomparison.append(FinalPList[t][0])
            pricecomparison.append(FinalPList[t][1])
            pricecomparison.append(FinalPList[t][2])
            pricecomparison.append(FinalPList[t][3])
            pricecomparison.append(FinalPList[t][4])
            pricecomparison.append(FinalPList[t][5])
            difpriceproducts.append(pricecomparison)
        elif (FinalPList[t][1] == 0.0 and FinalPList[t][2] == 0.0) or (FinalPList[t][1] == 0.0 and FinalPList[t][2] != 0.0):
            pissues.append(FinalPList[t][0])
            pissues.append(FinalPList[t][1])
            pissues.append(FinalPList[t][2])
            pissues.append(FinalPList[t][3])
            pissues.append(FinalPList[t][4])
            pissues.append(FinalPList[t][5])
            priceissues.append(pissues)
        else:
            pricecomparison.append(FinalPList[t][0])
            pricecomparison.append(FinalPList[t][1])
            pricecomparison.append(FinalPList[t][2])
            pricecomparison.append(FinalPList[t][3])
            pricecomparison.append(FinalPList[t][4])
            pricecomparison.append(FinalPList[t][5])
            samepriceproducts.append(pricecomparison)
            
    with open('difpriceproducts.csv','w') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        for a in range(len(difpriceproducts)):
            wr.writerow(difpriceproducts[a])

    with open('samepriceproducts.csv','w') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        for b in range(len(samepriceproducts)):
            wr.writerow(samepriceproducts[b])
    
    with open('priceissues.csv','w') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        for c in range(len(priceissues)):
            wr.writerow(priceissues[c])

        
    
    print('Final DIF')
    print(difpriceproducts)
    #print(samepriceproducts)
    
    
def update():
    
    client = pymongo.MongoClient('mongodb+srv://##Removedforsecurity?retryWrites=true&w=majority'.format(config.password), 27017)
    db = client['##Removedforsecurity']
    collection_products = db['##Removedforsecurity']
    
    for v in range(len(difpriceproducts)):
        #print(difpriceproducts[v])
        #print(difpriceproducts[v][1])
        #print(difpriceproducts[v][2])
        #print(difpriceproducts[v][3])
        #print(difpriceproducts[v][4])
        #print(difpriceproducts[v][5])
        # Update Price and Date
        query = collection_products.update_one({"_id":difpriceproducts[v][0], "urlString":difpriceproducts[v][5]}, { "$set" : {"price":difpriceproducts[v][1], "salePrice":difpriceproducts[v][2]}, "$currentDate": {"createdOn": True}},upsert=True)

        
    for l in range(len(samepriceproducts)):
        #print(difpriceproducts[v])
        #print(difpriceproducts[v][1])
        #print(difpriceproducts[v][2])
        #print(difpriceproducts[v][3])
        #print(difpriceproducts[v][4])
        #print(difpriceproducts[v][5])
        #Update Date
        query = collection_products.update_one({"_id":samepriceproducts[l][0], "urlString":samepriceproducts[l][5]}, {"$currentDate": {"createdOn": True}},upsert=True)


    


##DEV FUNCTION
def test():
    #res = requests.get('https://jaggerandstone.com/collections/bottoms-1/products/the-tayla-trousers-b-w-tartan')
    res = requests.get('https://australia.lilybod.com/collections/activewear/products/top-marley-phantom-jet')
    #res = requests.get('https://www.emperorapparel.com/collections/jeans/products/spray-jeans-indigo-ripped?variant=29285041766493')
    res.text
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    #priceatt1 = "product-price;money"
    priceatt1 = "seven columns omega;modal_price"
    htmlPhraseDelete = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']
    saleprice = ""
    if ";" in priceatt1:
        priceatt1split = priceatt1.split(';')
        htmlasplit1 = priceatt1split[0]
        htmlasplit2 = priceatt1split[1]
        print(htmlasplit1)
        print(htmlasplit2)
        price = soup.find(class_=htmlasplit1).find(class_=htmlasplit2)
        print(price)
        for x in range(len(htmlPhraseDelete)):
            price = str(price).replace(htmlPhraseDelete[x], '')
        price = re.sub('[^0-9],', ' ', str(price))
        print('$$')
        print(price)
        price = ','.join(re.findall('(?<!\d)(\d{2}.00)(?!\d)',price)) 
        print(price)
        price = re.sub("\s+", ",", price.strip())
        if "," in price:
            pricesplit = price.split(',')
            price = pricesplit[0]
            saleprice = pricesplit[1]
        if saleprice == "" or saleprice == " " or saleprice > "0":
            saleprice = "0"
        print(price)
        print(saleprice)

####MAIN FUNCTIONS####
product_url()
crawler_fetch()
fullstring()
pricepull()
outcome()
update()
#test()


print('end script')

