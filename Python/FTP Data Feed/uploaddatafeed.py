import numpy as np
import pandas as pd
import csv
import os
import pymongo
import config
from bson.objectid import ObjectId
from categorisation import findCat



###LISTS
productlist = []
productlist1 = []
parentCaterrors = []
result = []
subcaterrors = []
unwantedcat = ("Footwear","Accessories","Bags","Shoes")

filedir = "FTP/00_upload/importfiles"

###create a list of all the avaliable csv files 
###output - all txt files from each brand of all products
enteries  = os.listdir("FTP/00_upload/importfiles")



def removeDuplicates(duplicate): 
    tracker = []
    final_list = []
    for num in duplicate:
        if num[1] not in tracker: 
            tracker.append(num[1])
            final_list.append(num)
    return final_list 
        
        
 
    
    
def upload(products):
    #####FETCH PRODUCT DETAILS######
    
    #STAG
    client = pymongo.MongoClient("mongodb+srv://##Removedforsecurity?retryWrites=true&w=majority".format(config.password), 27017)
    db = client["##Removedforsecurity"]
    collection_products = db["##Removedforsecurity"]
    
    #query = collection_products.find({"brand":"##insertbrand", "isDelete":"0"}, {"_id":1,"urlString":1,"brand":1,"price":1,"salePrice":1,"crawlerUrlId":1})
    
    for i in products:
        product = []
        product.append(i[0])
        product.append(i[1])
        product.append(i[2])
        product.append(i[3])
        product.append(i[4])
        product.append(i[5])
        product.append(i[6])
        product.append(i[7])
        product.append(i[8])
        product.append(i[9])
        product.append(i[10])
        product.append(i[11])
        
        
        #product.append(productId)0
        #product.append(skuId)1
        #product.append(productName)2
        #product.append(primaryCat)3
        #product.append(secondaryCat)4
        #product.append(productUrl)5
        #product.append(imgUrl)6
        #product.append(gender)7
        #product.append(pricesale)8
        #product.append(price)9
        #product.append(color)10
        #product.append(brand)11
        
        
        #query = collection_products.insert_one(   insert here    )


        #print(i[1])


##LOOP THROUGH TXT FILES
def fetchdata():
    for i in enteries:
        filename = (filedir + "/" + i)
        
        ##READ TXT PRODUCT FILES AND ASSIGN TO DATAFRAME
        df = pd.read_csv(filename, sep = "|", header=None,error_bad_lines=False,low_memory=False)
        
        
        ## ASSIGN COLUMN HEADER FOR FULL FILES (TODO FOR DELTA FILES)
        df.columns = [
                "PRODUCT ID", 
                "PRODUCT NAME", 
                "SKU NUMBER", 
                "PRIMARY CAT", 
                "SECONDARY CAT", 
                "PRODUCT URL", 
                "IMG URL", 
                "BUY URL", 
                "SHORT DESCRIPTION", 
                "LONG PRODUCT DESCRIPTION", 
                "DISCOUNT", 
                "DISCOUNT TYPE", 
                "SALE PRICE", 
                "RETAIL PRICE", 
                "BEGIN DATE", 
                "END DATE", 
                "BRAND", 
                "SHIPPING", 
                "KEYWORDS", 
                "MANUFACTURER PART", 
                "MANUFACTURER NAME", 
                "SHIPPING INFO", 
                "AVALIABILITY", 
                "UPC", 
                "CLASS ID", 
                "CURRENCY", 
                "M1", 
                "PIXEL", 
                "ATT 1", 
                "ATT 2", 
                "ATT 3", 
                "ATT 4", 
                "ATT 5", 
                "ATT 6",
                "ATT 7",
                "ATT 8",
                "ATT 9",
                "ATT 10"
                ]
                
        ##DROP LAST TRAILER ROW     
        df.drop(df.tail(1).index,inplace=True)
        
        ##ITERATE THROUGH EACH DF [File]
        for index, row in df.iterrows():
            
            ##REMOVE UNWANTED CATEGORIES
            if row["PRIMARY CAT"] not in unwantedcat:
                ##DECLARE PRODUCT LIST
                product = []
                ##ASSIGN VALUES FOR EACH PRODUCT
                productId = row["PRODUCT ID"]
                skuId = row["SKU NUMBER"]
                productName = row["PRODUCT NAME"]
                primaryCat = row["PRIMARY CAT"]
                secondaryCat = row["SECONDARY CAT"]
                productUrl = row["PRODUCT URL"]
                imgUrl = row["IMG URL"]
                gender = row["ATT 6"]
                salePrice = row["SALE PRICE"]
                price = row["RETAIL PRICE"]
                colour = row["ATT 5"]
                brand = row["BRAND"]
                manufactpart = row["MANUFACTURER PART"]
                
                
                
                ##REMOVE SIZE FROM SKU 
                #print(skuId)
                #try:
                #    splitsku = skuId.split("-")
                #    skuId = (splitsku[0] + "-" + splitsku[1])
                #except:
                #    skuId = skuId
                    
                print(manufactpart)
                


                ##Working Products List
                product.append(productId)
                product.append(skuId)
                product.append(productName)
                product.append(primaryCat)
                product.append(secondaryCat)
                product.append(productUrl)
                product.append(imgUrl)
                product.append(gender)
                product.append(salePrice)
                product.append(price)
                product.append(colour)
                product.append(brand)
                product.append(manufactpart)
                productlist.append(product)
                
                
            
           
        ##REMOVE DUPLICATES - CALL func removeDuplicates
        productlist1 = removeDuplicates(productlist)
    
        
        
        ##Categorise results
        
        for x in productlist1:
            pcaterr = []
            tempresult = []
            
            ##Categorise
            categoryassign = x[4]
            productname = x[2]
            productid = x[0]
            Brand = x[11]
            print(Brand)
            Gender = x[7]
            categories = findCat(categoryassign,productname,Gender)
            
            ##Split Categories into primary and sub
            if categories != 'Error':
                parentCat = (categories[0])
                subCat = (categories[1])
                tempresult.append(productid)
                tempresult.append(Brand)
                tempresult.append(productname)
                tempresult.append(categoryassign)
                tempresult.append(Gender)
                tempresult.append(parentCat)
                tempresult.append(subCat)
                result.append(tempresult)
            ##Handle products which havent found a category, write them to a report
            elif categories == 'Error':
                pcaterr.append(productid)
                pcaterr.append(Brand)
                pcaterr.append(productname)
                pcaterr.append(categoryassign)
                pcaterr.append(Gender)
                parentCaterrors.append(pcaterr)


        ##FIX FILE NAME
        filenmtemp = os.path.splitext(i)[0]
        filenm = ("log/" + filenmtemp + ".csv")

        ##WRITE TO LOG CSV FILE
        with open(filenm,"w") as output_file:
            wr = csv.writer(output_file, dialect="excel")
            for a in range(len(productlist1)):
                wr.writerow(productlist1[a])
        

        
    
        ##PUSH PRODUCTS TO DB
        upload(productlist)
    
    
    ###Print all errors from categorisation across all brands
    if parentCaterrors is not None:
        with open('parentCaterros.csv',"w") as error_file:
            wr = csv.writer(error_file, dialect="excel")
            for b in range(len(parentCaterrors)):
                wr.writerow(parentCaterrors[b])
    
    
    ##Print all errors from categorisation across all brands
    if result is not None:
        with open('output.csv',"w") as result_file:
            wr = csv.writer(result_file, dialect="excel")
            for b in range(len(result)):
                wr.writerow(result[b])


    

####MAIN FUNCTIONS####
fetchdata()
update()
#test()
